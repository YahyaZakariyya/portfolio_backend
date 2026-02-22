"""
Portfolio app URL configuration.
All endpoints are read-only (GET).
"""

from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('skills/', views.SkillListView.as_view(), name='skill-list'),
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('experience/', views.ExperienceListView.as_view(), name='experience-list'),
    path('education/', views.EducationListView.as_view(), name='education-list'),
]
