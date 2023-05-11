from django.contrib import admin

# Register your models here.

from .models import HackathonPost, Registration, Submission

admin.site.register(HackathonPost)
admin.site.register(Registration)
admin.site.register(Submission)
