# from django.db.models import Q
from django.utils import timezone
from .serializers import (
    HackathonPostSerializer,
    RegistrationSerializers,
    RegistrationRequestSerializer,
    SubmissionSerializers,
    SubmissionDataSerializers,
    DeleteSerializer,
)

from .models import HackathonPost, Registration, Submission, GROUP_ROLE

# from .utils import MultipartJsonParser
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import imghdr
import json


class HackthonPostViewSet(viewsets.ViewSet):
    lookup_field = "id"

    @extend_schema(
        request=HackathonPostSerializer,
        responses={201: HackathonPostSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="create",
        permission_classes=[IsAuthenticated],
    )
    def create_hackathon_post(self, request):
        if request.user.groups.filter(name=GROUP_ROLE[0]).exists():
            pass
        else:
            return Response(
                data={"message": "You are not authorized to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serialized = HackathonPostSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_201_CREATED)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        responses={200: HackathonPostSerializer},
    )
    @action(
        detail=True,
        methods=["get"],
        url_path="read",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def get_hackathon_post(self, request, pk: int):
        try:
            hack_post = HackathonPost.objects.get(id=pk)
        except HackathonPost.DoesNotExist:
            return Response(
                data={"message": "Hackathon post does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serialized = HackathonPostSerializer(instance=hack_post)

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: HackathonPostSerializer(many=True)},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="read",
        permission_classes=[],
    )
    def get_all_hackathons(self, request):
        queryset = HackathonPost.objects.all()

        try:
            serialized = HackathonPostSerializer(instance=queryset, many=True)
        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=HackathonPostSerializer,
        responses={200: HackathonPostSerializer},
    )
    @action(
        detail=True,
        methods=["put"],
        url_path="update",
        permission_classes=[IsAuthenticated],
    )
    def update_hackathon_post(self, request):
        if request.user.groups.filter(name=GROUP_ROLE[0]).exists():
            pass
        else:
            return Response(
                data={"message": "You are not authorized to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            hack_post_id = request.data["id"]
        except KeyError:
            return Response(
                data={"message": "Hackathon post id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            language = HackathonPost.objects.get(id=hack_post_id)
        except HackathonPost.DoesNotExist:
            return Response(
                data={"message": "Hackathon post does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serialized = HackathonPostSerializer(
            instance=language, data=request.data, partial=True
        )
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)
        return Response(
            data=serialized.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @extend_schema(
        request=DeleteSerializer,
        responses={204: DeleteSerializer},
    )
    @action(
        detail=False,
        methods=["delete"],
        url_path="delete",
        permission_classes=[IsAuthenticated],
    )
    def delete_hackthon_posts(self, request):
        serialized = DeleteSerializer(data=request.data)
        if serialized.is_valid():
            listings = HackathonPost.objects.filter(id__in=request.data["ids"])

            try:
                listings.delete()
            except Exception:
                return Response(
                    {"message": "Internal Server Error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(data=request.data, status=status.HTTP_204_NO_CONTENT)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationViewSet(viewsets.ViewSet):
    @extend_schema(
        request=RegistrationRequestSerializer,
        responses={201: RegistrationSerializers},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="register",
        permission_classes=[IsAuthenticated],
    )
    def register_hackathon(self, request):
        user = request.user
        if user.groups.filter(name=GROUP_ROLE[1]).exists():
            pass
        else:
            return Response(
                data={"message": "You can not register, you have to be a participant"},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            hack_post_id = request.data["fk_hackathon"]
        except KeyError:
            return Response(
                data={"message": "Hackathon post id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            hack_post = HackathonPost.objects.get(id=hack_post_id)
        except HackathonPost.DoesNotExist:
            return Response(
                data={"message": "Hackathon does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        reg_data = {
            "fk_hackathon": hack_post.id,
            "fk_user": user.id,
        }
        serialized = RegistrationSerializers(data=reg_data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_201_CREATED)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: RegistrationSerializers(many=True)},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="participant/read",
        permission_classes=[],
    )
    def get_all_participant_registration(self, request):
        if request.user.is_authenticated:
            if request.user.groups.filter(name=GROUP_ROLE[1]).exists():
                queryset = Registration.objects.filter(fk_user=request.user)
                # .order_by(
            # "created_at"
            # )
            else:
                return Response(
                    data={"message": "Unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        else:
            return Response(
                data={"message": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            serialized = RegistrationSerializers(instance=queryset, many=True)
        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        responses={200: RegistrationSerializers(many=True)},
    )
    @action(
        detail=True,
        methods=["get"],
        url_path="participant/read",
        permission_classes=[],
    )
    def get_all_registration(self, request, pk: int):
        if request.user.is_authenticated:
            if request.user.groups.filter(name=GROUP_ROLE[0]).exists():
                queryset = Registration.objects.filter(fk_hackathon=pk)
                # .order_by(
            # "created_at"
            # )
            else:
                return Response(
                    data={"message": "Unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        else:
            return Response(
                data={"message": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            serialized = RegistrationSerializers(instance=queryset, many=True)
        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(data=serialized.data, status=status.HTTP_200_OK)


class SubmissionViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, JSONParser)

    @extend_schema(
        request=SubmissionDataSerializers,
        responses={201: {"message": "Submission created"}},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="create",
        permission_classes=[IsAuthenticated],
    )
    def submit_hackathon_submission(self, request):
        user = request.user
        if user.groups.filter(name=GROUP_ROLE[1]).exists():
            pass
        else:
            return Response(
                data={"message": "You can not submit, you have to be a participant"},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            req_json = json.loads(request.data["data"])
        except:  # noqa
            return Response(
                data={"message": "submission data is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            reg_id = req_json["fk_registration"]
        except:  # noqa
            return Response(
                data={"message": "Registration id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            registration = Registration.objects.get(registration_id=reg_id)
        except HackathonPost.DoesNotExist:
            return Response(
                data={"message": "Hackathon does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if registration.fk_user != user:
            return Response(
                data={"message": "You can not submit for this hackathon"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if registration.is_submitted:
            return Response(
                data={"message": "You have already submitted for this hackathon"},
                status=status.HTTP_403_FORBIDDEN,
            )

        now = timezone.now()
        if registration.fk_hackathon.end_date < now:
            return Response(
                data={"message": "Hackathon submission date is over"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if registration.fk_hackathon.start_date > now:
            return Response(
                data={"message": "Hackathon submission date is not started yet"},
                status=status.HTTP_403_FORBIDDEN,
            )

        sub_record = {
            "fk_registration": registration.registration_id,
            "name": req_json["name"],
            "summary": req_json["summary"],
        }

        if (
            registration.fk_hackathon.submission_type == "file"
            or registration.fk_hackathon.submission_type == "image"
        ):
            if not request.FILES.get("file"):
                return Response(
                    data={"message": "File is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            file = request.FILES.get("file")
            if not file:
                return Response(
                    data={"message": "File is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if registration.fk_hackathon.submission_type == "image":
                file_type = imghdr.what(file)
                if file_type not in ["jpeg", "jpg", "png", "gif"]:
                    return Response(
                        data={"message": "Invalid submission type"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if file.size > 10 * 1024 * 1024:
                    return Response(
                        data={"message": "Image size is too large"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            if file.size > 100 * 1024 * 1024:
                return Response(
                    data={"message": "File size is too large"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            sub_record["submission_file"] = file
            sub_record["submission_link"] = None
        else:
            if not req_json["submission_link"]:
                return Response(
                    data={"message": "Submission link is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            sub_record["submission_link"] = req_json["submission_link"]
            sub_record["submission_file"] = None

        serialized = SubmissionSerializers(data=sub_record)
        if serialized.is_valid():
            serialized.save()
            registration.is_submitted = True
            registration.save()
            return Response(data=serialized.data, status=status.HTTP_201_CREATED)
        return Response(
            data=serialized.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @extend_schema(
        request=SubmissionDataSerializers,
        responses={200: HackathonPostSerializer},
    )
    @action(
        detail=False,
        methods=["put"],
        url_path="update",
        permission_classes=[IsAuthenticated],
    )
    def update_hackathon_submission(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                data={"message": "You have to be logged in"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if user.groups.filter(name=GROUP_ROLE[1]).exists():
            pass
        else:
            return Response(
                data={"message": "You can not submit, you have to be a participant"},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            req_json = json.loads(request.data["data"])
        except KeyError:
            return Response(
                data={"message": "submission data is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            reg_id = req_json["fk_registration"]
        except KeyError:
            return Response(
                data={"message": "Registration id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            registration = Registration.objects.get(registration_id=reg_id)
        except HackathonPost.DoesNotExist:
            return Response(
                data={"message": "Hackathon does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if registration.fk_user != user:
            return Response(
                data={"message": "You can not submit for this hackathon"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not registration.is_submitted:
            return Response(
                data={"message": "You have not submitted for this hackathon"},
                status=status.HTTP_403_FORBIDDEN,
            )

        now = timezone.now()
        if registration.fk_hackathon.end_date < now:
            return Response(
                data={"message": "Hackathon submission date is over"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if registration.fk_hackathon.start_date > now:
            return Response(
                data={"message": "Hackathon submission date is not started yet"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if "id" not in req_json:
            return Response(
                data={"message": "Submission id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            submission = Submission.objects.get(id=req_json["id"])
        except Submission.DoesNotExist:
            return Response(
                data={"message": "Submission does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        sub_record = {
            "fk_registration": registration.registration_id,
            "name": req_json["name"],
            "summary": req_json["summary"],
        }

        if (
            registration.fk_hackathon.submission_type == "file"
            or registration.fk_hackathon.submission_type == "image"
        ):
            if not request.FILES.get("file"):
                return Response(
                    data={"message": "File is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            file = request.FILES.get("file")
            if not file:
                return Response(
                    data={"message": "File is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if registration.fk_hackathon.submission_type == "image":
                file_type = imghdr.what(file)
                if file_type not in ["jpeg", "jpg", "png", "gif"]:
                    return Response(
                        data={"message": "Invalid submission type"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if file.size > 10 * 1024 * 1024:
                    return Response(
                        data={"message": "Image size is too large"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            if file.size > 100 * 1024 * 1024:
                return Response(
                    data={"message": "File size is too large"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            sub_record["submission_file"] = file
            sub_record["submission_link"] = None
        else:
            if not req_json["submission_link"]:
                return Response(
                    data={"message": "Submission link is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            sub_record["submission_link"] = req_json["submission_link"]
            sub_record["submission_file"] = None

        serialized = SubmissionSerializers(
            data=sub_record, instance=submission, partial=True
        )
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_201_CREATED)
        return Response(
            data=serialized.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @extend_schema(
        responses={200: SubmissionSerializers(many=True)},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="participant/read",
        permission_classes=[],
    )
    def get_all_participant_submission(self, request):
        if request.user.is_authenticated:
            if request.user.groups.filter(name=GROUP_ROLE[1]).exists():
                queryset = Submission.objects.filter(
                    fk_registration__fk_user=request.user
                )
            else:
                return Response(
                    data={"message": "Unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                data={"message": "You need to be logged in"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            serialized = SubmissionSerializers(instance=queryset, many=True)
        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(data=serialized.data, status=status.HTTP_200_OK)
