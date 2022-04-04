from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import QuoteViewSet

app_name = 'api'

router = DefaultRouter()
router.register('quote', QuoteViewSet, basename='quote')

urlpatterns = [
    path('', include(router.urls))
]