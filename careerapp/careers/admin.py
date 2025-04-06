from django.contrib import admin

from .models import JobSeeker, MyUser, Recruiter

admin.site.register(MyUser)
admin.site.register(JobSeeker)
admin.site.register(Recruiter)
