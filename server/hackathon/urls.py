from rest_framework import routers
from .views import HackthonPostViewSet, RegistrationViewSet, SubmissionViewSet

router = routers.DefaultRouter()
router.register(r"hackathon", HackthonPostViewSet, basename="hackathon")
router.register(r"submission", SubmissionViewSet, basename="submission")
router.register(r"registration", RegistrationViewSet, basename="registration")

urlpatterns = router.urls
