"""
Portfolio models.

All models include:
- `created_at` / `updated_at` timestamps via TimestampedModel
- `order` field for manual sorting via admin
- `__str__` for readable admin display
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class TimestampedModel(models.Model):
    """Abstract base model with auto-managed timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(TimestampedModel):
    """
    Developer profile — singleton-style model.
    Only one profile should exist; enforced via admin, not DB constraint,
    to keep flexibility for staging/testing.
    """
    full_name = models.CharField(max_length=100)
    title = models.CharField(
        max_length=200,
        help_text="e.g. Senior Backend Engineer"
    )
    bio = models.TextField()
    years_of_experience = models.PositiveIntegerField(default=0)
    email = models.EmailField()
    linkedin_url = models.URLField(blank=True, default='')
    github_url = models.URLField(blank=True, default='')
    resume_url = models.URLField(
        blank=True,
        default='',
        help_text="Link to downloadable resume/CV"
    )
    avatar_url = models.URLField(
        blank=True,
        default='',
        help_text="Link to profile photo"
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name


class Skill(TimestampedModel):
    """Technical skill with category and proficiency level."""

    class Category(models.TextChoices):
        BACKEND = 'Backend', 'Backend'
        FRONTEND = 'Frontend', 'Frontend'
        DEVOPS = 'DevOps', 'DevOps'
        DATABASE = 'Database', 'Database'
        TOOLS = 'Tools', 'Tools'
        OTHER = 'Other', 'Other'

    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.BACKEND,
    )
    proficiency_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Proficiency from 1 to 100",
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text="Icon identifier (e.g., 'python', 'docker') for frontend rendering"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"


class Project(TimestampedModel):
    """Portfolio project showcase."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    tech_stack = models.JSONField(
        default=list,
        help_text='List of technologies, e.g. ["Django", "PostgreSQL", "Docker"]'
    )
    github_url = models.URLField(blank=True, default='')
    live_url = models.URLField(blank=True, default='')
    thumbnail_url = models.URLField(
        blank=True,
        default='',
        help_text="Project screenshot or thumbnail URL"
    )
    architecture_summary = models.TextField(
        blank=True,
        default='',
        help_text="High-level architecture description"
    )
    key_features = models.JSONField(
        default=list,
        blank=True,
        help_text='List of key features, e.g. ["Real-time sync", "Multi-tenant"]'
    )
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-featured', 'name']

    def __str__(self):
        return self.name


class Experience(TimestampedModel):
    """Professional work experience."""

    company_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Leave blank if currently working here"
    )
    description = models.TextField()
    technologies_used = models.JSONField(
        default=list,
        help_text='e.g. ["Python", "Django", "AWS"]'
    )
    company_url = models.URLField(blank=True, default='')
    is_current = models.BooleanField(
        default=False,
        help_text="Currently working at this company"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']
        verbose_name_plural = "Experience"

    def __str__(self):
        return f"{self.role} at {self.company_name}"


class Education(TimestampedModel):
    """Educational background."""

    institute_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True, default='')
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Leave blank if currently studying"
    )
    description = models.TextField(blank=True, default='')
    grade = models.CharField(
        max_length=20,
        blank=True,
        default='',
        help_text="e.g. 3.8 GPA, First Class Honours"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_year']
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} — {self.institute_name}"
