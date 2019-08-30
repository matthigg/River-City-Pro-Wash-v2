from django.urls import path
from .views import submit

app_name = "contact-form"
urlpatterns = [
  path('submit/', submit, name='submit'),
]