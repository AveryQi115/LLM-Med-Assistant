from django.db import models

# Create your models here.
# TODO(avery): add user authentication

class UserInputPost(models.Model):
    patient_id = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)

    def __str__(self):
        return f"id: {self.patient_id} name: {self.patient_name}"
