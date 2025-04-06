from django.urls import path, include
from . import views
from rest_framework import routers

from .views import JobSeekerViewSet

router = routers.DefaultRouter()
router.register('jobseeker', JobSeekerViewSet)
urlpatterns = [
    path('', include(router.urls))
]