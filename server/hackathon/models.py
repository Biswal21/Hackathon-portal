from django.db import models
from django.contrib.auth.models import User
import uuid

GROUP_ROLE = ["Organiser", "Participant"]


LINK = "link"
IMG = "image"
FILE = "file"

SUBMISSION_TYPE_CHOICES = [
    (FILE, "File"),
    (IMG, "Image"),
    (LINK, "Link"),
]


# Create your models here.
class HackathonPost(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField()
    bg_image = models.URLField()
    submission_type = models.CharField(
        max_length=5, choices=SUBMISSION_TYPE_CHOICES, default=LINK
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reward = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Registration(models.Model):
    registration_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    fk_user = models.ForeignKey(
        User, related_name="participant", on_delete=models.CASCADE
    )
    fk_hackathon = models.ForeignKey(HackathonPost, on_delete=models.CASCADE)
    is_submitted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fk_hackathon.title}-{self.registration_id}"


class Submission(models.Model):
    fk_registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    summary = models.TextField()
    submission_file = models.FileField(
        upload_to="static/submissions", null=True, blank=True
    )
    submission_link = models.URLField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
