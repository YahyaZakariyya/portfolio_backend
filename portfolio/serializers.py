"""
Portfolio serializers.
Read-only serializers for all portfolio models.
"""

from rest_framework import serializers
from .models import Profile, Skill, Project, Experience, Education


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'full_name',
            'title',
            'bio',
            'years_of_experience',
            'email',
            'linkedin_url',
            'github_url',
            'resume_url',
            'avatar_url',
        ]
        read_only_fields = fields


class SkillSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True,
    )

    class Meta:
        model = Skill
        fields = [
            'id',
            'name',
            'category',
            'category_display',
            'proficiency_level',
            'icon',
            'order',
        ]
        read_only_fields = fields


class ProjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for project listings."""

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'tech_stack',
            'github_url',
            'live_url',
            'thumbnail_url',
            'featured',
            'order',
        ]
        read_only_fields = fields


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Full serializer for individual project detail."""

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'tech_stack',
            'github_url',
            'live_url',
            'thumbnail_url',
            'architecture_summary',
            'key_features',
            'featured',
            'order',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class ExperienceSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            'id',
            'company_name',
            'role',
            'start_date',
            'end_date',
            'description',
            'technologies_used',
            'company_url',
            'is_current',
            'duration',
            'order',
        ]
        read_only_fields = fields

    def get_duration(self, obj):
        """Calculate human-readable duration."""
        from datetime import date
        end = obj.end_date or date.today()
        months = (end.year - obj.start_date.year) * 12 + (end.month - obj.start_date.month)
        years = months // 12
        remaining_months = months % 12
        parts = []
        if years:
            parts.append(f"{years} yr{'s' if years > 1 else ''}")
        if remaining_months:
            parts.append(f"{remaining_months} mo{'s' if remaining_months > 1 else ''}")
        return ' '.join(parts) or 'Less than a month'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id',
            'institute_name',
            'degree',
            'field_of_study',
            'start_year',
            'end_year',
            'description',
            'grade',
            'order',
        ]
        read_only_fields = fields
