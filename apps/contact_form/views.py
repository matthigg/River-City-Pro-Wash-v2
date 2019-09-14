from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CreateContactForm
from .amazon_ses import send_email

import os
import requests

def submit(request):

  # reCAPTCHA v3
  r = requests.post(
    'https://www.google.com/recaptcha/api/siteverify', 
    params={
      'response': request.POST["g-recaptcha-response"],
      'secret': os.environ["RECAPTCHA_SECRET_KEY"],
    }
  )

  # Return 'error' message if reCAPTCHA fails
  if r.json()['success'] == False:
      messages.add_message(request, messages.INFO, 'There was an error with your request. We appologize for the inconvenience.')
      return redirect('contact')

  # Continue with normal POST request if reCAPTCHA succeeds
  if request.method == "POST":

    # Send email via Amazon SES
    send_email(request.POST)

    # Create a contact form using the CreateContactForm model
    form = CreateContactForm(request.POST)

    # Save form to database if data is valid, create a messages{} 
    # object with a success message, and redirect to contact.html
    if form.is_valid():

      # Here, we want to add the user's IP address to the database. So far we've
      # gathered the user's contact form submission in an instance of the
      # ModelForm class, and named the instance 'form'.
      #
      # An instance of the ModelForm class looks like a string of HTML tags, so 
      # trying to add information to that would be difficult. 
      #
      # Instead, use *.save(commit=False) to return a Model object, and adding 
      # data to objects is a lot easier than trying to append a string that
      # resembles HTML to the output of an instance of the ModelForm class.
      form_submission = form.save(commit=False)

      # Add the IP address to an instance of the Model object
      form_submission.ip_address = request.META['REMOTE_ADDR']

      # Save the complete submission
      form.save()
      # messages.add_message(request, messages.INFO, 'Your Message Has Been Sent!')
      return redirect('thanks')

    # Django stores error messages in form.error. Create & send a new
    # blank empty form when there's an error.
    else: 
      form = CreateContactForm() 
    return render(request, 'contact', { 'form': form })