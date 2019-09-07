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
  print(context)
  return render(request, 'index.html', context)

def our_work(request):

  from collections import defaultdict
  context = defaultdict(list)
  for img in UploadedImages.objects.all():
    context[img.img_category].append({
      'img_alt_before': img.img_alt_before,
      'img_before': img.img_before,
      'img_alt_after': img.img_alt_after,
      'img_after': img.img_after,
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