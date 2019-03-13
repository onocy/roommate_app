"""cleanslate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from doma.views import home, profile, reminders, calendar, edit_chore, create_chore, delete_chore, edit_user_profile, create_user, edit_user, create_home, create_topic, edit_topic, create_event, forum, edit_home, edit_event
#reminders, finance,

urlpatterns = [
    url(r'^$', home, name='doma/login/'),
    url(r'^admin/', admin.site.urls),
    url(r'^doma/$', home, name='home'),
    url(r'^doma/profile/$', profile, name='profile'),
    url(r'^doma/reminders/$', reminders, name='reminder'),
    url(r'^doma/calendar/$', calendar, name='calendar'),
    url(r'^doma/message-board/$', forum, name='message-board'),

    url(r'^doma/profile/(?P<pk>[-\w]+)/edit/$', edit_user_profile, name='edit-user-profile'),
    url(r'^doma/chore/(?P<pk>[-\w]+)/edit/$', edit_chore, name = 'edit-chore-deadline'),
    url(r'^doma/chore/create/$', create_chore, name = 'create-chore'),
    url(r'^doma/chore/(?P<pk>[-\w]+)/delete/$', delete_chore, name = 'delete-chore'),
    url(r'^doma/user/create/$', create_user, name='create-user'),
    url(r'^doma/user/(?P<pk>[-\w]+)/edit/$', edit_user, name='edit-user'),
    url(r'^doma/home/create/$', create_home, name='create-home'),
    url(r'^doma/home/(?P<pk>[-\w]+)/edit/$', edit_home, name='edit-home'),
    url(r'^doma/topic/create/$', create_topic, name='create-topic'),
    url(r'^doma/topic/(?P<pk>[-\w]+)/edit/$', edit_topic, name='edit-topic'),
    url(r'^doma/event/create/$', create_event, name='create-event'),
    url(r'^doma/event/(?P<pk>[-\w]+)/edit/$', edit_event, name='edit-event'),
]

urlpatterns += [
    url(r'^doma/', include('django.contrib.auth.urls')),
    url(r'^markdownx/', include('markdownx.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
