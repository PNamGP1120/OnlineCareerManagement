from rest_framework import viewsets, permissions
from .models import MyUser, JobSeeker, Recruiter
from .serializers import JobSeekerSerializer


class JobSeekerViewSet(viewsets.ModelViewSet):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer

