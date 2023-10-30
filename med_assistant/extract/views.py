from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserInputPostForm
from django.core.files.storage import FileSystemStorage
from .models import UserInputPost
import os

#TODO(avery): user authentication

def extract_patient_related_data(request):
    if request.method == "POST":
        input_post_form = UserInputPostForm(request.POST, request.FILES)
        if input_post_form.is_valid():
            input_post_form.save()
            #TODO(avery): search the data and get LLM generated results for it
            with open(os.path.join('documents',input_post_form.cleaned_data['patient_records'].name)) as f:
                patient_records = f.read()
            context = {"data": {"""You are an AI assistant tasked with examining a patient's medical information.  
                                Your goal is to extract information strictly from the patient's file and not make any inferences or assumptions. 
                                Here is the patient's file: {}. 
                                Generate a patient report following the prompt template: {}""".format(patient_records, input_post_form.cleaned_data['prompt_info'])}}
            return render(request, "extract/patient_data.html", context)
        else:
            return HttpResponse("Invalid form content")
    else:
        input_post_form = UserInputPostForm()
        context = {"input_post_form": input_post_form}
    return render(request, "extract/extract_patient_related_data.html", context)
