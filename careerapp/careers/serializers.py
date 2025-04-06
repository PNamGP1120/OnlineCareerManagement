from rest_framework.serializers import ModelSerializer
from .models import MyUser, Recruiter, JobSeeker, Job, JobApplication, Notification, Conversation, Message, Interview


class MyUserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
class JobSeekerSerializer(ModelSerializer):
    user = MyUserSerializer()

    class Meta:
        model = JobSeeker
        fields = ['skills', 'experience', 'user']