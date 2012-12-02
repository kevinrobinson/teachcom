from django.conf.urls import patterns, include, url
from teachercomapp.forms import UserRegistrationForm

from registration.views import register
# from registration.views import login
import registration.backends.default.urls as regUrls
# import registration.backends.simple.urls as simpleUrls

from teachercom import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

backend_string = ('registration.backends.' + 
    ('default.DefaultBackend' if settings.SEND_EMAIL else 'simple.SimpleBackend'))

register_args = { 'backend': backend_string,'form_class': UserRegistrationForm }

if not settings.SEND_EMAIL:
    register_args['success_url'] = 'send'

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'teachercomapp.views.index', name='index'),
    url(r'^send/', 'teachercomapp.views.send', name='send'),
    url(r'^csv/', 'teachercomapp.views.handle_csv', name='csv'),
    # url(r'^teachercom/', include('teachercom.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', register, register_args, name='registration_register'),
    url(r'^accounts/', include(regUrls)),
    )