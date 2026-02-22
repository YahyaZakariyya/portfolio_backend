"""
Portfolio Django Admin configuration.
Customized with list_display, search_fields, list_filter, and ordering
for efficient data management.
"""

from django.contrib import admin
from .models import Profile, Skill, Project, Experience, Education


# =============================================================================
# ADMIN SITE CUSTOMIZATION
# =============================================================================

admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Backend"
admin.site.index_title = "Manage Portfolio Content"


# =============================================================================
# MODEL ADMINS
# =============================================================================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'email', 'years_of_experience', 'updated_at')
    search_fields = ('full_name', 'title', 'email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Personal Info', {
            'fields': ('full_name', 'title', 'bio', 'years_of_experience', 'avatar_url')
        }),
        ('Contact & Links', {
            'fields': ('email', 'linkedin_url', 'github_url', 'resume_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        """Only allow one Profile instance."""
        if Profile.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency_level', 'icon', 'order')
    list_filter = ('category',)
    search_fields = ('name',)
    list_editable = ('order', 'proficiency_level')
    ordering = ('order', 'category', 'name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'featured', 'order', 'updated_at')
    list_filter = ('featured',)
    search_fields = ('name', 'description')
    list_editable = ('featured', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Project Info', {
            'fields': ('name', 'slug', 'description', 'tech_stack', 'key_features')
        }),
        ('Links', {
            'fields': ('github_url', 'live_url', 'thumbnail_url')
        }),
        ('Architecture', {
            'fields': ('architecture_summary',),
            'classes': ('wide',),
        }),
        ('Display', {
            'fields': ('featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company_name', 'start_date', 'end_date', 'is_current', 'order')
    list_filter = ('is_current',)
    search_fields = ('company_name', 'role', 'description')
    list_editable = ('order', 'is_current')
    ordering = ('order', '-start_date')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Position', {
            'fields': ('company_name', 'role', 'company_url')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Details', {
            'fields': ('description', 'technologies_used')
        }),
        ('Display', {
            'fields': ('order',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institute_name', 'field_of_study', 'start_year', 'end_year', 'order')
    search_fields = ('institute_name', 'degree', 'field_of_study')
    list_editable = ('order',)
    ordering = ('order', '-start_year')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Institution', {
            'fields': ('institute_name', 'degree', 'field_of_study')
        }),
        ('Duration', {
            'fields': ('start_year', 'end_year')
        }),
        ('Details', {
            'fields': ('description', 'grade')
        }),
        ('Display', {
            'fields': ('order',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
