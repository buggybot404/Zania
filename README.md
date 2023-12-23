# Question n Answer Bot

Application is Question-Answering bot that leverages the capabilities of a large language model. It answer questions based on the content of a data feeder document which provides context to bot. This context is used to provide relevant answers to the queries

## API Details

**Endpoint** - ```http://{{zania_base_url}}/api/v1/get_answers```

**Sample Request** - 

```
curl --location 'http://127.0.0.1:8000/api/v1/get_answers' \
--form 'data_feeder=@"<<your_data_feeder_doc>>"' \
--form 'questions_set=@"<<your_queries_doc>>"'
```

### Request File(s) Details

* Data Feeder(provider) File - This file contains the data that provides context to the bot to answer the queries thrown by the user. This file can be of following types -
  * PDF
  * Json
 
  PDF file can be any valid pdf document that contains the necessary information to be consumned by the bot. Json file too contains the relevant data for the bot and have following format -

  ```
  [
    {
        "content": "Does Company have a Network Diagram showing firewalls in place to separate networks they can share?",
        "id": "8f3d94b4-b290-4484-9d47-16690823cbf9~50a42721-a8ac-4192-8f0d-8ad108c76444~questionnaire_import_template (5).csv~6",
        "createdAt": "2023-08-31T21:01:05.000Z",
        "modifiedAt": "2023-10-20T12:40:52.000Z",
        "answer": "Yes, we do have a Network Diagram showing firewalls in place to separate networks. Please verify the comment below to see what the specifics are and if we actually follow this to the satisfaction of your guidelines. We need to clarify more but this is a good basic level of understanding.",
        "comment": "A Network Diagram showing segmentation is available for download from the Trust Center under Documents at security.company.com. We also take this deeply seriously and struggle to make sure that this is always working. Please bear with us as we work through making the updates necessary for these aspects. We need to keep balancing the efforts to find the best path forward and work through the challenges to find out the balance of how we proceed forward based on the aspects of bet intent. We swear we are working on this and not just vamping for the purpose of testing long messages ",
        "pageNumber": null,
        "questionNumber": 6,
        "product": null,
        "products": [
            {
                "id": "--global--"
            }
        ],
        "isFavorite": true,
        "accessLevel": "private",
        "source": "questionnaire",
        "subtype": {
            "raw": [
                "Custom"
            ],
            "pretty": [
                "Custom"
            ]
        }
    },
    {
        "content": "What were the results of the Company's latest pen test, and what remediation was done?",
        "id": "8f3d94b4-b290-4484-9d47-16690823cbf9~50a42721-a8ac-4192-8f0d-8ad108c76444~questionnaire_import_template (5).csv~5",
        "createdAt": "2023-08-31T21:01:05.000Z",
        "modifiedAt": "2023-08-31T21:01:05.000Z",
        "answer": null,
        "comment": "Company does not share this type of detailed and/or sensitive evidence for routine vendor due diligence assessments. This evidence has been provided to our external auditors for SOC 2 Type 2 and ISO 27001. The audit reports that are available under NDA at our Company Security Hub (security.company.com) are a testament to the implementation and effectiveness of this control in the Company environment.",
        "pageNumber": null,
        "questionNumber": 5,
        "product": null,
        "products": [
            {
                "id": "--global--"
            }
        ],
        "isFavorite": true,
        "accessLevel": "private",
        "source": "questionnaire",
        "subtype": {
            "raw": [
                "Custom"
            ],
            "pretty": [
                "Custom"
            ]
        }
    }
  ]
  ```

* Questions File - This file contains the questions/ queries required to be answered on the basis of context generated from data feeder files. This file have following format -  

  ```
  {
    "questions":[
      {
        "question": "question1"
        "id": "question1_id"
      },
      {
        "question": "question2"
        "id": "question2_id"
      }
    ]
  }
  ```


  # Running Project

  ## Prerequisites -

  * Python with version between 3.1.x and 3.10. [Download](https://www.python.org/downloads/)
  * Virtual Environment. [Doc](https://python.land/virtual-environments/virtualenv)
  * Add Your_Open_Ai_Key in ```.env``` file
  * Your favourite editor.
 
  ## Steps to run project -

  * Clone this repository
  * Open it in your favourite editor
  * Activate the virtual environment
  * Go to project root (~/Zania/QnA_Bot) and run ```pip install -r requirements.txt ```
  * Run Django Server ```python manage.py runserver```
  * Hit the endpoint providing your input files
  
