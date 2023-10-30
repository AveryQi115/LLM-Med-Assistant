from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserInputPostForm
from django.core.files.storage import FileSystemStorage
from .models import UserInputPost

#TODO(avery): user authentication

def extract_patient_related_data(request):
    if request.method == "POST":
        input_post_form = UserInputPostForm(request.POST, request.FILES)
        if input_post_form.is_valid():
            input_post_form.save()
            #TODO(avery): search the data and get LLM generated results for it
            context = {"data": {}}
            return render(request, "extract/patient_data.html", context)
        else:
            return HttpResponse("Invalid form content")
    else:
        input_post_form = UserInputPostForm()
        context = {"input_post_form": input_post_form}
    return render(request, "extract/extract_patient_related_data.html", context)
