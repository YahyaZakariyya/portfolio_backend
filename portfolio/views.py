"""
Portfolio API views.
All views are read-only (GET only). No authentication required.
"""

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, Skill, Project, Experience, Education, Certification, BlogTag, BlogPost
from .serializers import (
    ProfileSerializer,
    SkillSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    ExperienceSerializer,
    EducationSerializer,
    CertificationSerializer,
    PortfolioSerializer,
    BlogTagSerializer,
    BlogPostListSerializer,
    BlogPostDetailSerializer,
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


class PortfolioView(APIView):
    """
    GET /api/portfolio/
    Single combined endpoint for the home page.
    Returns profile, skills, projects, experience, education, certifications
    in one round trip. Replaces the 6+ individual calls.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        profile = Profile.objects.first()
        if profile is None:
            return Response({'detail': 'Profile not configured yet.'}, status=404)

        data = {
            'profile':        profile,
            'skills':         Skill.objects.all(),
            'projects':       Project.objects.all(),
            'experience':     Experience.objects.all(),
            'education':      Education.objects.all(),
            'certifications': Certification.objects.all(),
        }
        serializer = PortfolioSerializer(data)
        return Response(serializer.data)


# ─── Blog Views ────────────────────────────────────────────────


class BlogTagListView(ListAPIView):
    """
    GET /api/blog/tags/
    Returns all blog tags.
    """
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class BlogPostListView(ListAPIView):
    """
    GET /api/blog/posts/
    Query params: ?tag=<slug>, ?featured=true, ?search=<term>, ?limit=<n>
    """
    serializer_class = BlogPostListSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        qs = BlogPost.objects.filter(status='published')
        tag = self.request.query_params.get('tag')
        featured = self.request.query_params.get('featured')
        search = self.request.query_params.get('search')
        limit = self.request.query_params.get('limit')

        if tag:
            qs = qs.filter(tags__slug=tag)
        if featured == 'true':
            qs = qs.filter(featured=True)
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(excerpt__icontains=search)
        if limit:
            try:
                qs = qs[:int(limit)]
            except (ValueError, TypeError):
                pass
        return qs


class BlogPostDetailView(RetrieveAPIView):
    """
    GET /api/blog/posts/<slug>/
    Returns full post detail and increments view count.
    """
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        BlogPost.objects.filter(pk=instance.pk).update(views=instance.views + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BlogPostLikeView(APIView):
    """
    POST /api/blog/posts/<slug>/like/
    Body: {"action": "like"} or {"action": "unlike"}
    Honor-system anonymous likes — no auth required.
    """
    permission_classes = [AllowAny]

    def post(self, request, slug):
        try:
            post = BlogPost.objects.get(slug=slug, status='published')
        except BlogPost.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

        action = request.data.get('action', 'like')
        if action == 'unlike':
            post.likes = max(0, post.likes - 1)
        else:
            post.likes += 1
        post.save(update_fields=['likes'])
        return Response({'likes': post.likes})


class RelatedPostsView(ListAPIView):
    """
    GET /api/blog/posts/<slug>/related/
    Returns up to 3 posts sharing tags with the given post.
    """
    serializer_class = BlogPostListSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            post = BlogPost.objects.get(slug=slug, status='published')
        except BlogPost.DoesNotExist:
            return BlogPost.objects.none()
        tag_ids = post.tags.values_list('id', flat=True)
        return (
            BlogPost.objects
            .filter(status='published', tags__in=tag_ids)
            .exclude(pk=post.pk)
            .distinct()[:3]
        )
