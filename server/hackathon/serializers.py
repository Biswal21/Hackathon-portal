from rest_framework import serializers
from .models import HackathonPost, Submission, Registration


class HackathonPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonPost
        fields = [
            "id",
            "title",
            "description",
            "image",
            "bg_image",
            "submission_type",
            "start_date",
            "end_date",
            "reward",
            "updated_at",
            "created_at",
        ]


class SubmissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            "id",
            "fk_registration",
            "name",
            "summary",
            "submission_file",
            "submission_link",
        ]


class SubmissionDataSerializers(serializers.Serializer):
    file = serializers.FileField()
    data = SubmissionSerializers()

    class Meta:
        fields = [
            "file",
            "data",
        ]


class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            "registration_id",
            "fk_user",
            "fk_hackathon",
            "is_submitted",
        ]


class RegistrationRequestSerializer(serializers.Serializer):
    fk_hackathon = serializers.IntegerField()


class DeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())
