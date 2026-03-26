"""
Root URL configuration for portfolio_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """API root — returns available endpoints for discoverability."""
    return JsonResponse({
        "message": "Portfolio Backend API",
        "version": "1.0.0",
        "endpoints": {
            "profile": "/api/profile/",
            "skills": "/api/skills/",
            "projects": "/api/projects/",
            "projects_detail": "/api/projects/<slug>/",
            "experience": "/api/experience/",
            "education": "/api/education/",
            "certifications": "/api/certifications/",
        }
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('portfolio.urls', namespace='portfolio')),
    path('writer/', include('portfolio.writer_urls', namespace='writer')),
]
