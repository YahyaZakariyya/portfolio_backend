"""
Portfolio API views.
All views are read-only (GET only). No authentication required.
"""

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, Skill, Project, Experience, Education, Certification
from .serializers import (
    ProfileSerializer,
    SkillSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    ExperienceSerializer,
    EducationSerializer,
    CertificationSerializer,
)


class ProfileView(APIView):
    """
    GET /api/profile/
    Returns the single developer profile.
    No pagination — returns a single object.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        profile = Profile.objects.first()
        if profile is None:
            return Response(
                {"detail": "Profile not configured yet."},
                status=404,
            )
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class SkillListView(ListAPIView):
    """
    GET /api/skills/
    Returns all skills, ordered by `order` field.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]
    pagination_class = None  # Return all skills without pagination


class ProjectListView(ListAPIView):
    """
    GET /api/projects/
    Returns all projects with lightweight serialization.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class ProjectDetailView(RetrieveAPIView):
    """
    GET /api/projects/<slug>/
    Returns full project detail by slug.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class ExperienceListView(ListAPIView):
    """
    GET /api/experience/
    Returns all work experience entries.
    """
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class EducationListView(ListAPIView):
    """
    GET /api/education/
    Returns all education entries.
    """
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class CertificationListView(ListAPIView):
    """
    GET /api/certifications/
    Returns all certification entries.
    """
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [AllowAny]
    pagination_class = None
