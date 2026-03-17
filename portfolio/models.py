"""
Portfolio models.

All models include:
- `created_at` / `updated_at` timestamps via TimestampedModel
- `order` field for manual sorting via admin
- `__str__` for readable admin display
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


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
    description_bullets = models.JSONField(
        default=list,
        blank=True,
        help_text='Optional list of bullet points for rendering on the frontend'
    )
    technologies_used = models.JSONField(
        default=list,
        blank=True,
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


class Certification(TimestampedModel):
    """Professional certifications."""

    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(
        max_length=200,
        help_text="e.g. University of Michigan, Codio, Packt"
    )
    issue_date = models.DateField()
    expiration_date = models.DateField(
        null=True,
        blank=True,
        help_text="Leave blank if it does not expire"
    )
    credential_id = models.CharField(max_length=100, blank=True, default='')
    credential_url = models.URLField(blank=True, default='')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-issue_date']
        verbose_name_plural = "Certifications"

    def __str__(self):
        return f"{self.name} from {self.issuing_organization}"


# ─── Blog ──────────────────────────────────────────────────────


class BlogTag(TimestampedModel):
    """Tag for categorising blog posts."""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, unique=True)
    color = models.CharField(
        max_length=7,
        default='#3b82f6',
        help_text="Hex color for tag pill, e.g. #3b82f6"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class BlogPost(TimestampedModel):
    """
    Blog post with structured content blocks.

    The `blocks` field is a JSON array of block objects, e.g.:
      [
        {"type": "paragraph", "content": "Hello world"},
        {"type": "heading2", "content": "Section title"},
        {"type": "code", "language": "python", "content": "print('hi')", "caption": ""},
        {"type": "image", "url": "...", "alt": "...", "caption": ""},
        {"type": "callout", "variant": "info", "content": "Note..."},
        {"type": "list", "variant": "bullet", "items": ["item1", "item2"]},
        {"type": "quote", "content": "Quote text", "attribution": "Author"},
        {"type": "table", "caption": "", "headers": ["A", "B"], "rows": [["1", "2"]]},
        {"type": "video", "url": "...", "poster": "", "caption": ""},
        {"type": "divider"},
        {"type": "tags", "items": ["python", "django"]}
      ]
    """

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=320, unique=True)
    excerpt = models.TextField(
        help_text="Short summary shown in listing cards (1-2 sentences)"
    )
    cover_image = models.URLField(
        blank=True,
        default='',
        help_text="URL for cover / hero image"
    )

    blocks = models.JSONField(
        default=list,
        help_text="Array of content block objects (see model docstring for format)"
    )

    tags = models.ManyToManyField(
        BlogTag,
        blank=True,
        related_name='posts'
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Set automatically when status → Published; can be overridden"
    )

    reading_time = models.PositiveIntegerField(
        default=0,
        help_text="Estimated reading time in minutes (auto-calculated on save)"
    )
    views = models.PositiveIntegerField(default=0, editable=False)
    likes = models.PositiveIntegerField(default=0, editable=False)

    featured = models.BooleanField(
        default=False,
        help_text="Show as featured / hero post in the blog listing"
    )
    order = models.PositiveIntegerField(default=0, help_text="Manual sort order")

    # SEO overrides
    seo_title = models.CharField(
        max_length=60,
        blank=True,
        default='',
        help_text="Override <title> tag (max 60 chars; falls back to title)"
    )
    seo_description = models.CharField(
        max_length=160,
        blank=True,
        default='',
        help_text="Meta description (max 160 chars; falls back to excerpt)"
    )
    og_image = models.URLField(
        blank=True,
        default='',
        help_text="OpenGraph image URL (falls back to cover_image)"
    )

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-set published_at on first publish
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        # Auto-calculate reading time (~200 wpm)
        word_count = 0
        for block in (self.blocks or []):
            content = block.get('content', '')
            if isinstance(content, str):
                word_count += len(content.split())
            for item in (block.get('items') or []):
                if isinstance(item, str):
                    word_count += len(item.split())
        self.reading_time = max(1, round(word_count / 200))

        super().save(*args, **kwargs)
