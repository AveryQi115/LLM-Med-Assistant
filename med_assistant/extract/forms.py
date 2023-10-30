from django import forms
from .models import UserInputPost

# 写文章的表单类
class UserInputPostForm(forms.ModelForm):
    class Meta:
        model = UserInputPost
        fields = ('patient_records', 'prompt_info')
