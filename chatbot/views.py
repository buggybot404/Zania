from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain import hub
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from .exception.chatbot_exception import ChatbotException
from .factory.embeddings_factory import EmbeddingsFactory
from .utils.constants import PDF_FILE_EXTENSION, JSON_FILE_EXTENSION, RECURSIVE_CHARACTER_TEXT_SPLITTER, \
    OPEN_AI_EMBEDDING, HUB_REPO, OPEN_AI_MODEL_NAME, OPEN_AI_MODEL_TEMP, QUESTIONS_FILE, DATA_FEEDER_FILE, \
    SUCCESS_RESPONSE_MESSAGE, SUCCESS_RESPONSE_CODE, HTTP_METHOD_POST
from .utils.file_util import FileUtil
from .factory.text_splitter_factory import TextSplitterFactory
from .forms import GenerateAnswerRequest
from langchain.vectorstores import Chroma


@csrf_exempt
def generate_chatbot_answers(request):
    if request.method == HTTP_METHOD_POST:
        request_form = GenerateAnswerRequest(request.POST, request.FILES)

        if request_form.is_valid():
            # Process the form data
            questions = request_form.cleaned_data[QUESTIONS_FILE]
            data_feeder = request_form.cleaned_data[DATA_FEEDER_FILE]

            # Get questions data
            questions_data = FileUtil.load_json_file_data(questions)
            # Get the data from feeder file
            feeder_data = process_data_feeder_file(data_feeder)

            # Get the appropriate text splitter
            text_splitter = TextSplitterFactory.get_text_splitter(RECURSIVE_CHARACTER_TEXT_SPLITTER)
            splits = text_splitter.create_text_splits(feeder_data)

            # Create vector store with data set
            vectorstore = create_vector_store(splits)

            response_data = generate_answers_for_bot(vectorstore, questions_data)

            # Return the results as JSON
            return JsonResponse({
                "message": SUCCESS_RESPONSE_MESSAGE,
                "response_code": SUCCESS_RESPONSE_CODE,
                "data": response_data
            }, safe=False)
        else:
            raise ChatbotException("0001", Exception("Invalid Request data"), 400)


def create_vector_store(text_splits):
    try:
        return Chroma.from_documents(documents=text_splits,
                                     embedding=EmbeddingsFactory.get_embedding(OPEN_AI_EMBEDDING))
    except Exception as e:
        raise ChatbotException(exception_id="0009", exception=e, status_code=500)


def process_data_feeder_file(feeder_file):
    # Determine the file type (PDF or JSON)
    data_feeder_file_type = FileUtil.get_file_type(feeder_file)

    if data_feeder_file_type == PDF_FILE_EXTENSION:
        feeder_file_data = FileUtil.load_pdf_file_data(feeder_file)
    elif data_feeder_file_type == JSON_FILE_EXTENSION:
        feeder_file_data = FileUtil.load_feeder_json_file_data(feeder_file)
    else:
        raise ChatbotException(exception_id="0004", exception=Exception("Invalid file type."), status_code=400)

    return feeder_file_data


def generate_answers_for_bot(vectorstore, questions):
    try:
        retriever = vectorstore.as_retriever()
        prompt = hub.pull(HUB_REPO)
        llm = ChatOpenAI(model_name=OPEN_AI_MODEL_NAME, temperature=OPEN_AI_MODEL_TEMP)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
        )

        response = []
        for question in questions["questions"]:
            response.append((question["question"], rag_chain.invoke(question["question"])))

        return response
    except Exception as e:
        raise ChatbotException(exception_id="0010", exception=e, status_code=500)
    finally:
        vectorstore.delete_collection()
