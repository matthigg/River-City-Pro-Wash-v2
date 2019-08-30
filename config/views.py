from django.shortcuts import render
from apps.contact_form.forms import CreateContactForm

# Main Navigation

def index(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'index.html', context)

def services(request):
  context = {}
  return render(request, 'services.html', context)

def our_work(request):
  context = {}
  return render(request, 'our-work.html', context)

def contact(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'contact.html', context)

def faq(request):
  context = {}
  return render(request, 'faq.html', context)

# Services

def house_washing(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'services/house-washing.html', context)

def concrete_brick_washing(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'services/concrete-brick-washing.html', context)

def deck_patio_cleaning(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'services/deck-patio-cleaning.html', context)

def deck_staining(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'services/deck-staining.html', context)

def grafitti_removal(request):
  form = CreateContactForm
  context = { 'form': form, }
  return render(request, 'services/grafitti-removal.html', context)