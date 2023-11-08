from django.urls import path
from . import views

app_name = "extract"

urlpatterns = [
    path(
        "extract_patient_related_data_hidden",
        views.extract_patient_related_data_hidden,
        name="extract_patient_related_data_hidden",
    ),
    path("extract_patient_related_data", views.extract_patient_related_data, name="extract_patient_related_data"),
]
