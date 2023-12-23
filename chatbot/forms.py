from django import forms


class GenerateAnswerRequest(forms.Form):
    questions_set = forms.FileField()
    data_feeder = forms.FileField()
