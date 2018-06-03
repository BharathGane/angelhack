from django.conf.urls import include, url

from api.views import *

urlpatterns = [
	url(r'^session$', get_session),
]