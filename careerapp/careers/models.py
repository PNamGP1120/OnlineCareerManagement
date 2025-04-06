from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class DateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering = ['-created_at']

# Mô hình User
class MyUser(AbstractUser):
    ROLE_CHOICES = [
        ('jobseeker', 'JobSeeker'),
        ('recruiter', 'Recruiter'),
    ]
    avatar = CloudinaryField('image', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='jobseeker')
    updated_at = models.DateTimeField(auto_now=True)

# Mô hình JobSeeker
class JobSeeker(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    skills = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)

# Mô hình Recruiter
class Recruiter(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=255)

# Mô hình Job
class Job(DateModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)
    salary = models.IntegerField()
    location = models.CharField(max_length=255)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)

# Mô hình JobApplication
class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, blank=True, null=True)

# Mô hình Notification
class Notification(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    recruiter = models.ForeignKey(Recruiter, blank=True, null=True, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeeker, blank=True, null=True, on_delete=models.CASCADE)

# Mô hình Conversation
class Conversation(DateModel):
    recruiter = models.ForeignKey(Recruiter, blank=True, null=True, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeeker, blank=True, null=True, on_delete=models.CASCADE)

# Mô hình Message
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Interview(DateModel):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    ]

    application = models.OneToOneField('JobApplication', on_delete=models.CASCADE, related_name='interview')
    scheduled_at = models.DateTimeField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Interview for {self.application.job.title} - {self.application.job_seeker.user.username}"