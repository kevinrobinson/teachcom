from django.conf.urls import patterns, include, url
from teachercomapp.forms import UserRegistrationForm

from registration.views import register
import registration.backends.default.urls as regUrls
# import regbackend


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'teachercomapp.views.index', name='index'),
    url(r'^send/', 'teachercomapp.views.send', name='send'),
    # url(r'^teachercom/', include('teachercom.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', register, {'backend': 'registration.backends.default.DefaultBackend','form_class': UserRegistrationForm}, name='registration_register'),
    (r'^accounts/', include(regUrls)),
    )
