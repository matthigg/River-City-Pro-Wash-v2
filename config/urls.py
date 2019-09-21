"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .views import contact, faq, index, our_work, services, thanks
from .views import house_washing, concrete_brick_washing, deck_patio_washing, deck_staining, fence_cleaning, graffiti_removal

# Needed to serve MEDIA files associated with the uploaded_images app in local 
# development
# https://wsvincent.com/django-image-uploads/
from django.conf import settings
from django.conf.urls.static import static

# Sitemap
# https://docs.djangoproject.com/en/2.2/ref/contrib/sitemaps/
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
sitemaps = {
  'static': StaticViewSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',          index,    name='index'),
    path('',          include('apps.contact_form.urls', namespace='contact_form')),
    path('contact/',  contact,  name='contact'),
    path('faq/',      faq,      name='faq'),
    path('our-work/', our_work, name='our-work'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('services/house-washing',          house_washing,          name='house-washing'),
    path('services/concrete-brick-washing', concrete_brick_washing, name='concrete-brick-washing'),
    path('services/deck-patio-washing',     deck_patio_washing,     name='deck-patio-washing'),
    path('services/deck-staining',          deck_staining,          name='deck-staining'),
    path('services/fence-cleaning',         fence_cleaning,         name='fence-cleaning'),
    path('services/graffiti-removal',       graffiti_removal,       name='graffiti-removal'),
    path('thanks',    thanks,   name='thanks'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Last line in urlpatterns[] is needed to serve MEDIA files associated with the 
# uploaded_images app in local development
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# https://wsvincent.com/django-image-uploads/
# https://stackoverflow.com/questions/5517950/django-media-url-and-media-root
# https://docs.djangoproject.com/en/1.9/howto/static-files/#serving-files-uploaded-by-a-user-during-development
