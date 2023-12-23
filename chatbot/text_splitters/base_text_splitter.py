from django.db import models


class BaseTextSplitter(models.Model):

    class Meta:
        abstract = True

    def create_text_splits(self, data_to_split):
        raise NotImplementedError("Subclasses must implement the create_text_splits method.")

