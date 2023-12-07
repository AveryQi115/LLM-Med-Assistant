from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserInputPostForm
from django.core.files.storage import FileSystemStorage
from .models import UserInputPost
from django.views.decorators.csrf import csrf_exempt
import os
import json

#TODO(avery): user authentication

def extract_patient_related_data_hidden(request):
    if request.method == "POST":
        input_post_form = UserInputPostForm(request.POST, request.FILES)
        if input_post_form.is_valid():
            input_post_form.save()
            #TODO(avery): search the data and get LLM generated results for it
            with open(os.path.join('documents',input_post_form.cleaned_data['patient_records'].name)) as f:
                patient_records = f.read()
            # context = {"data": {"""You are an AI assistant tasked with examining a patient's medical information.  
            #                     Your goal is to extract information strictly from the patient's file and not make any inferences or assumptions. 
            #                     Here is the patient's file: {}. 
            #                     Generate a patient report following the prompt template: {}""".format(patient_records, input_post_form.cleaned_data['prompt_info'])}}
            
            data = {
                "inputs": [
                    [
                        {
                            "role": "system",
                            "content": """You are an AI assistant tasked with examining a patient's medical information.  Your goal is to extract information strictly from the patient's file \
                                          and not make any inferences or assumptions, generate a patient report with the exact template:
                                          
                                            Task 1:
                                            Extract and print the following details from the patient's medical file:
                                            A) patient's name
                                            B) patient's ID

                                            Task 2:
                                            List all the active medications for the patient, including dosage and intake instructions. Provide the source of this information. 

                                            Task 3:
                                            Summarize the doctor's notes since the patient's last visit. Include the name of the doctor and the source of these notes. 
                                            
                                            Task 4:
                                            Summarize the patient's medical history and hospital course. Include the source of this information.

                                            Task 5:
                                            Summarize the lab results in a manner understandable to a doctor. This should include a min of 10 lab inputs. For example, if the white blood cell count is 13.5, summarize this finding. 

                                            Remember, you should only present information available in the file. Do not infer or create information."""
                        },
                        {
                            "role": "user",
                            "content": patient_records
                        }
                    ]
                ],
                "parameters": {
                    "max_new_tokens": 4000,
                    "top_p": 0.9,
                    "temperature": 0.6
                }
            }
            
            api_url = os.environ.get('API_URL')
            
            response = request.post(api_url, json=data)
            
            # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                api_result = response.json()
                
                # Include the API results in the context
                context = {"data": api_result[0]['generation']['content']}
                return render(request, "extract/patient_data.html", context)
            else:
                return HttpResponse("Failed to get data from the API")            
            
        else:
            return HttpResponse("Invalid form content")
    else:
        input_post_form = UserInputPostForm()
        context = {"input_post_form": input_post_form}
    return render(request, "extract/extract_patient_related_data.html", context)


@csrf_exempt
def extract_patient_related_data(request):
    if request.method == "POST":
        input_post_form = UserInputPostForm(request.POST, request.FILES)
        if input_post_form.is_valid():
            input_post_form.save()
        ret = os.system(f"srun -c 16 --mem=128Gb --gres=gpu:1 extract/generate_result.sh {input_post_form.cleaned_data['patient_records'].name}")
        print(ret)
        with open("generations/result.txt", "r") as f:
            data = f.read()
        assert(type(data) == str, f"{type(data)}")
        sections = data.split("##")
        return HttpResponse(json.dumps({"data": "Request process done, you can now choose your own section", "generations":sections}), content_type="application/json")
    input_post_form = UserInputPostForm()
    context = {"input_post_form": input_post_form}
    return render(request, "extract/bot.html", context)

@csrf_exempt
def generate(request):
    if request.method == "POST":
        data = request.POST.get("generations")
        print(data)
        return HttpResponse(f"{data}")
    return HttpResponse("generate cannot called through get")