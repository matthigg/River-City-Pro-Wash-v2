from django.shortcuts import render
from apps.contact_form.forms import CreateContactForm
from apps.uploaded_images.models import UploadedImages

# Main Navigation

def contact(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'contact.html', context)

def faq(request):
  context = {}
  return render(request, 'faq.html', context)

def index(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'index.html', context)

def our_work(request):

  # When someone visits our-work.html, query the database for anything in the
  # table represented by the UploadedImages model and store it in the context{}
  # dictionary, which contains key:value pairs where each value is a list of
  # objects that represent each image in a category represented by the 'key'
  from collections import defaultdict
  context = defaultdict(list)
  for img in UploadedImages.objects.all():
    context[img.Category].append({
      'Category': img.Category,
      'Before_Picture_Description': img.Before_Picture_Description,
      'Before_Picture': img.Before_Picture,
      'After_Picture_Description': img.After_Picture_Description,
      'After_Picture': img.After_Picture,
    })

  return render(request, 'our-work.html', context)

def services(request):
  context = {}
  return render(request, 'services.html', context)

def thanks(request):
  context = {}
  return render(request, 'thanks.html', context)

# Services

def house_washing(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'services/house-washing.html', context)

def concrete_brick_washing(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'services/concrete-brick-washing.html', context)

def deck_patio_washing(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'services/deck-patio-washing.html', context)

def deck_staining(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'services/deck-staining.html', context)

def fence_cleaning(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'services/fence-cleaning.html', context)

def graffiti_removal(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'services/graffiti-removal.html', context)