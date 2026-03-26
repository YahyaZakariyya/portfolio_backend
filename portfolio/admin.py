"""
Portfolio Django Admin configuration.
Customized with list_display, search_fields, list_filter, and ordering
for efficient data management.

Blog admin includes a custom block editor widget with visual block-builder toolbar.
"""

import json
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Profile, Skill, Project, Experience, Education, Certification, BlogTag, BlogPost


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
            'fields': ('description', 'description_bullets', 'technologies_used')
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


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'issue_date', 'expiration_date', 'order')
    search_fields = ('name', 'issuing_organization', 'credential_id')
    list_editable = ('order',)
    ordering = ('order', '-issue_date')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Certification Details', {
            'fields': ('name', 'issuing_organization')
        }),
        ('Dates', {
            'fields': ('issue_date', 'expiration_date')
        }),
        ('Credentials', {
            'fields': ('credential_id', 'credential_url')
        }),
        ('Display', {
            'fields': ('order',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


# =============================================================================
# BLOG ADMIN
# =============================================================================

BLOCK_EDITOR_JS = """
<script>
(function() {
  var TEMPLATES = {
    paragraph:       function() { return { type: 'paragraph', content: '' }; },
    heading2:        function() { return { type: 'heading2', content: '' }; },
    heading3:        function() { return { type: 'heading3', content: '' }; },
    image:           function() { return { type: 'image', url: '', alt: '', caption: '' }; },
    video:           function() { return { type: 'video', url: '', poster: '', caption: '' }; },
    list_bullet:     function() { return { type: 'list', variant: 'bullet', items: ['', ''] }; },
    list_numbered:   function() { return { type: 'list', variant: 'numbered', items: ['', ''] }; },
    table:           function() { return { type: 'table', caption: '', headers: ['Column 1', 'Column 2'], rows: [['', '']] }; },
    quote:           function() { return { type: 'quote', content: '', attribution: '' }; },
    callout_info:    function() { return { type: 'callout', variant: 'info', content: '' }; },
    callout_warning: function() { return { type: 'callout', variant: 'warning', content: '' }; },
    callout_success: function() { return { type: 'callout', variant: 'success', content: '' }; },
    callout_error:   function() { return { type: 'callout', variant: 'error', content: '' }; },
    code:            function() { return { type: 'code', language: 'python', content: '', caption: '' }; },
    divider:         function() { return { type: 'divider' }; },
    tags:            function() { return { type: 'tags', items: [] }; }
  };

  document.addEventListener('DOMContentLoaded', function() {
    var textarea = document.getElementById('id_blocks');
    if (!textarea) return;

    var toolbar = document.createElement('div');
    toolbar.style.cssText = 'margin-bottom:8px;display:flex;flex-wrap:wrap;gap:4px;padding:10px;background:#f5f5f5;border:1px solid #ddd;border-radius:4px;align-items:center;';

    function addBtn(label, key, bg) {
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = label;
      b.title = 'Insert block: ' + key;
      b.style.cssText = 'padding:4px 9px;font-size:11px;cursor:pointer;background:' + (bg || '#1a7acc') + ';color:#fff;border:none;border-radius:3px;white-space:nowrap;';
      b.addEventListener('click', function() {
        var blocks = [];
        try { blocks = JSON.parse(textarea.value || '[]'); } catch(e) { blocks = []; }
        blocks.push(TEMPLATES[key]());
        textarea.value = JSON.stringify(blocks, null, 2);
        updateCounter();
      });
      toolbar.appendChild(b);
    }

    addBtn('¶ Para', 'paragraph', '#444');
    addBtn('H2', 'heading2', '#222');
    addBtn('H3', 'heading3', '#222');
    addBtn('⌃ Image', 'image', '#0077b6');
    addBtn('▶ Video', 'video', '#0077b6');
    addBtn('• List', 'list_bullet', '#2d6a4f');
    addBtn('1. List', 'list_numbered', '#2d6a4f');
    addBtn('⊞ Table', 'table', '#2d6a4f');
    addBtn('" Quote', 'quote', '#6b4f9e');
    addBtn('ℹ Info', 'callout_info', '#0077b6');
    addBtn('⚠ Warn', 'callout_warning', '#d97706');
    addBtn('✓ OK', 'callout_success', '#059669');
    addBtn('✗ Err', 'callout_error', '#dc2626');
    addBtn('</> Code', 'code', '#1a1a2e');
    addBtn('— Divider', 'divider', '#888');
    addBtn('# Tags', 'tags', '#7c3aed');

    var sep = document.createElement('div');
    sep.style.cssText = 'width:1px;height:24px;background:#ccc;margin:0 6px;flex-shrink:0;';
    toolbar.appendChild(sep);

    var formatBtn = document.createElement('button');
    formatBtn.type = 'button';
    formatBtn.textContent = '⟳ Format JSON';
    formatBtn.style.cssText = 'padding:4px 9px;font-size:11px;cursor:pointer;background:#777;color:#fff;border:none;border-radius:3px;';
    formatBtn.addEventListener('click', function() {
      try {
        var parsed = JSON.parse(textarea.value || '[]');
        textarea.value = JSON.stringify(parsed, null, 2);
        textarea.style.outline = '2px solid #4caf50';
        setTimeout(function() { textarea.style.outline = ''; }, 1500);
        updateCounter();
      } catch(e) {
        textarea.style.outline = '2px solid #f44336';
        alert('Invalid JSON: ' + e.message);
      }
    });
    toolbar.appendChild(formatBtn);

    var counter = document.createElement('span');
    counter.style.cssText = 'font-size:12px;color:#555;font-weight:600;margin-left:8px;';
    toolbar.appendChild(counter);

    function updateCounter() {
      try {
        var b = JSON.parse(textarea.value || '[]');
        counter.textContent = b.length + ' block' + (b.length !== 1 ? 's' : '');
      } catch(e) {
        counter.textContent = '⚠ invalid JSON';
      }
    }

    textarea.addEventListener('input', updateCounter);
    textarea.parentNode.insertBefore(toolbar, textarea);

    // Pretty-print on initial load
    try { textarea.value = JSON.stringify(JSON.parse(textarea.value || '[]'), null, 2); } catch(e) {}
    updateCounter();
  });
})();
</script>
"""


class BlockEditorWidget(forms.Textarea):
    """Textarea with a visual block-builder toolbar for the blocks JSON field."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({
            'rows': 35,
            'style': (
                'font-family: "Fira Code", "JetBrains Mono", "Courier New", monospace;'
                'font-size: 13px; line-height: 1.5; width: 100%;'
            ),
        })

    def render(self, name, value, attrs=None, renderer=None):
        # Pretty-print the JSON before rendering
        if value and isinstance(value, (list, dict)):
            value = json.dumps(value, indent=2)
        elif value and isinstance(value, str):
            try:
                value = json.dumps(json.loads(value), indent=2)
            except (json.JSONDecodeError, ValueError):
                pass
        rendered = super().render(name, value, attrs, renderer)
        return mark_safe(rendered + BLOCK_EDITOR_JS)


class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
        widgets = {
            'blocks': BlockEditorWidget(),
        }

    def clean_blocks(self):
        blocks = self.cleaned_data.get('blocks')
        if isinstance(blocks, str):
            try:
                return json.loads(blocks)
            except json.JSONDecodeError as e:
                raise forms.ValidationError(f"Invalid JSON in blocks: {e}")
        return blocks or []


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def post_count(self, obj):
        return obj.posts.filter(status='published').count()
    post_count.short_description = 'Published Posts'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ('title', 'status', 'featured', 'reading_time', 'views', 'likes', 'published_at', 'order')
    list_filter = ('status', 'featured', 'tags')
    search_fields = ('title', 'excerpt')
    list_editable = ('status', 'featured', 'order')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at', 'views', 'likes', 'reading_time')
    ordering = ('-published_at', '-created_at')

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'cover_image', 'blocks'),
        }),
        ('Classification', {
            'fields': ('tags', 'featured', 'order'),
        }),
        ('Publishing', {
            'fields': ('status', 'published_at'),
        }),
        ('SEO Overrides', {
            'fields': ('seo_title', 'seo_description', 'og_image'),
            'classes': ('collapse',),
            'description': 'Optional — falls back to title / excerpt / cover_image when left blank.',
        }),
        ('Stats (read-only)', {
            'fields': ('views', 'likes', 'reading_time'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def get_changeform_initial_data(self, request):
        return {
            'blocks': json.dumps([
                {'type': 'paragraph', 'content': 'Start writing here...'}
            ], indent=2)
        }
