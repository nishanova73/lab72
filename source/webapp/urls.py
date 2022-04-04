from django.urls import path, include

from webapp.views import IndexView

app_name = 'webapp'

urlpatterns = [
path('', IndexView.as_view(), name='index'),
]