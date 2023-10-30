from django.db import models

# Create your models here.
# TODO(avery): add user authentication

class UserInputPost(models.Model):
    patient_records = models.FileField(upload_to="documents/")
    prompt_info = models.TextField()

    def __str__(self):
        return f"prompt_info: {self.prompt_info}"
