"""
Portfolio app URL configuration.
All endpoints are read-only (GET) except blog likes (POST).
"""

from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # ── Combined home-page endpoint (preferred) ────────────────
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),

    # ── Individual endpoints (kept for backwards compat) ───────
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('skills/', views.SkillListView.as_view(), name='skill-list'),
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('experience/', views.ExperienceListView.as_view(), name='experience-list'),
    path('education/', views.EducationListView.as_view(), name='education-list'),
    path('certifications/', views.CertificationListView.as_view(), name='certification-list'),

    # ── Blog ───────────────────────────────────────────────────
    path('blog/tags/', views.BlogTagListView.as_view(), name='blog-tags'),
    path('blog/posts/', views.BlogPostListView.as_view(), name='blog-posts'),
    path('blog/posts/<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('blog/posts/<slug:slug>/like/', views.BlogPostLikeView.as_view(), name='blog-post-like'),
    path('blog/posts/<slug:slug>/related/', views.RelatedPostsView.as_view(), name='blog-post-related'),
]
