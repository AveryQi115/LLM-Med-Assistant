from django import forms
from .models import UserInputPost


class UserInputPostForm(forms.ModelForm):
    class Meta:
        model = UserInputPost
        fields = ('patient_records', 'prompt_info')
