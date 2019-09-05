from django.shortcuts import render, redirect
from .forms import CreateContactForm
from django.contrib import messages
from .amazon_ses import send_email

def submit(request):
  if request.method == "POST":

    # Send email via Amazon SES
    send_email(request.POST)

    # Create a contact form using the CreateContactForm model
    form = CreateContactForm(request.POST)

    # Save form to database if data is valid, create a messages{} 
    # object with a success message, and redirect to contact.html
    if form.is_valid():
      form.save()
      # messages.add_message(request, messages.INFO, 'Your Message Has Been Sent!')
      return redirect('thanks')

    # Django stores error messages in form.error. Create & send a new
    # blank empty form when there's an error.
    else: 
      form = CreateContactForm() 
    return render(request, 'contact', { 'form': form })