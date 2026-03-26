"""
Writer portal views — authenticated template-based blog management.
URL namespace: 'writer'  (/writer/)
"""

import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_datetime
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .models import BlogPost, BlogTag

_LOGIN = 'writer:login'


# ── Auth ─────────────────────────────────────────────────────────────────────

def writer_login(request):
    if request.user.is_authenticated:
        return redirect('writer:dashboard')
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username', '').strip(),
            password=request.POST.get('password', ''),
        )
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'writer:dashboard'))
        error = 'Invalid username or password.'
    return render(request, 'writer/login.html', {'error': error})


def writer_logout(request):
    logout(request)
    return redirect(_LOGIN)


# ── Dashboard ────────────────────────────────────────────────────────────────

@login_required(login_url=_LOGIN)
def dashboard(request):
    posts = BlogPost.objects.prefetch_related('tags').order_by('-created_at')
    return render(request, 'writer/dashboard.html', {'posts': posts})


# ── Post create / edit ───────────────────────────────────────────────────────

@login_required(login_url=_LOGIN)
def post_create(request):
    if request.method == 'POST':
        return _save_post(request, post=None)
    return render(request, 'writer/post_form.html', {
        'post': None,
        'tags': BlogTag.objects.all(),
        'blocks_json': '[]',
        'selected_tag_ids': [],
    })


@login_required(login_url=_LOGIN)
def post_edit(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == 'POST':
        return _save_post(request, post=post)
    return render(request, 'writer/post_form.html', {
        'post': post,
        'tags': BlogTag.objects.all(),
        'blocks_json': json.dumps(post.blocks or [], ensure_ascii=False),
        'selected_tag_ids': list(post.tags.values_list('id', flat=True)),
    })


def _save_post(request, post):
    d = request.POST
    title = d.get('title', '').strip()
    if not title:
        messages.error(request, 'Title is required.')
        return _form_response(request, post, d)

    slug_val = d.get('slug', '').strip() or slugify(title)
    excerpt = d.get('excerpt', '').strip()
    cover_image = d.get('cover_image', '').strip()
    status = d.get('status', BlogPost.Status.DRAFT)
    featured = d.get('featured') == 'on'
    order = int(d.get('order') or 0)
    seo_title = d.get('seo_title', '').strip()
    seo_description = d.get('seo_description', '').strip()
    og_image = d.get('og_image', '').strip()
    tag_ids = d.getlist('tags')

    try:
        blocks = json.loads(d.get('blocks_json', '[]') or '[]')
        if not isinstance(blocks, list):
            blocks = []
    except (json.JSONDecodeError, ValueError):
        blocks = []

    if post is None:
        post = BlogPost()

    post.title = title
    post.slug = slug_val
    post.excerpt = excerpt
    post.cover_image = cover_image
    post.status = status
    post.featured = featured
    post.order = order
    post.seo_title = seo_title
    post.seo_description = seo_description
    post.og_image = og_image
    post.blocks = blocks

    pub_raw = d.get('published_at', '').strip()
    if pub_raw:
        parsed = parse_datetime(pub_raw)
        if parsed:
            post.published_at = parsed

    try:
        post.save()
        post.tags.set(BlogTag.objects.filter(id__in=tag_ids))
        messages.success(request, f'"{post.title}" saved.')
        return redirect('writer:post_edit', slug=post.slug)
    except Exception as exc:
        messages.error(request, f'Save failed: {exc}')
        return _form_response(request, post, d)


def _form_response(request, post, data):
    tag_ids = [int(i) for i in data.getlist('tags') if i.isdigit()]
    return render(request, 'writer/post_form.html', {
        'post': post,
        'tags': BlogTag.objects.all(),
        'blocks_json': data.get('blocks_json', '[]'),
        'selected_tag_ids': tag_ids,
    })


# ── Post delete ───────────────────────────────────────────────────────────────

@login_required(login_url=_LOGIN)
@require_POST
def post_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    title = post.title
    post.delete()
    messages.success(request, f'"{title}" deleted.')
    return redirect('writer:dashboard')


# ── Tags ──────────────────────────────────────────────────────────────────────

@login_required(login_url=_LOGIN)
def tags_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            name = request.POST.get('name', '').strip()
            color = request.POST.get('color', '#3b82f6').strip()
            if name:
                BlogTag.objects.get_or_create(
                    slug=slugify(name),
                    defaults={'name': name, 'color': color},
                )
                messages.success(request, f'Tag "{name}" created.')
            else:
                messages.error(request, 'Name is required.')
        elif action == 'delete':
            tag = get_object_or_404(BlogTag, id=request.POST.get('tag_id'))
            messages.success(request, f'Tag "{tag.name}" deleted.')
            tag.delete()
        return redirect('writer:tags')

    return render(request, 'writer/tags.html', {
        'tags': BlogTag.objects.all(),
    })
