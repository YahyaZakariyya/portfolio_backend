"""
Management command: seed_blog
Creates sample blog posts for development and testing.

Usage:
    DJANGO_ENV=development python manage.py seed_blog
    DJANGO_ENV=development python manage.py seed_blog --clear   # wipe first
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.models import BlogTag, BlogPost


TAGS = [
    {'name': 'Django',         'slug': 'django',         'color': '#092e20'},
    {'name': 'Python',         'slug': 'python',         'color': '#3572a5'},
    {'name': 'System Design',  'slug': 'system-design',  'color': '#7c3aed'},
    {'name': 'PostgreSQL',     'slug': 'postgresql',     'color': '#336791'},
    {'name': 'Redis',          'slug': 'redis',          'color': '#dc382d'},
    {'name': 'Docker',         'slug': 'docker',         'color': '#2496ed'},
    {'name': 'REST APIs',      'slug': 'rest-apis',      'color': '#f59e0b'},
    {'name': 'Performance',    'slug': 'performance',    'color': '#10b981'},
]

POSTS = [
    {
        'title': 'Building a Production-Grade Django REST API from Scratch',
        'slug': 'django-rest-api-production',
        'excerpt': (
            'A deep dive into structuring a Django REST Framework project '
            'the way it is done in production — versioned endpoints, '
            'custom serializer validation, throttling, and a sane deployment pipeline.'
        ),
        'featured': True,
        'tags': ['django', 'rest-apis', 'python'],
        'blocks': [
            {
                'type': 'paragraph',
                'content': (
                    'Most Django REST API tutorials stop at the hello-world stage. '
                    'This post goes further: we structure the project like it will '
                    'serve real traffic on day one. By the end you\'ll have versioned '
                    'endpoints, proper error envelopes, request throttling, and a '
                    'containerised deployment that mirrors production.'
                ),
            },
            {'type': 'heading2', 'content': 'Project Structure'},
            {
                'type': 'paragraph',
                'content': (
                    'The single biggest mistake I see in Django projects is a flat '
                    'apps/views.py that grows to 2,000 lines. Instead, split by '
                    'domain from day one. A project serving users, billing, and '
                    'notifications should have three separate Django apps — not one '
                    '"api" app holding everything.'
                ),
            },
            {
                'type': 'code',
                'language': 'bash',
                'content': (
                    'project/\n'
                    '├── config/          # settings, urls, wsgi, asgi\n'
                    '│   ├── settings/\n'
                    '│   │   ├── base.py\n'
                    '│   │   ├── development.py\n'
                    '│   │   └── production.py\n'
                    '│   └── urls.py\n'
                    '├── apps/\n'
                    '│   ├── users/\n'
                    '│   ├── billing/\n'
                    '│   └── notifications/\n'
                    '└── manage.py'
                ),
                'caption': 'Domain-driven project layout',
            },
            {'type': 'heading2', 'content': 'API Versioning'},
            {
                'type': 'paragraph',
                'content': (
                    'URL-based versioning (/api/v1/...) is explicit and cacheable. '
                    'Header-based versioning is cleaner for clients but harder to debug '
                    'in a browser. For public-facing APIs I always go URL-based.'
                ),
            },
            {
                'type': 'code',
                'language': 'python',
                'content': (
                    '# config/urls.py\n'
                    'from django.urls import path, include\n\n'
                    'urlpatterns = [\n'
                    '    path("api/v1/", include("apps.api_v1.urls")),\n'
                    '    path("api/v2/", include("apps.api_v2.urls")),\n'
                    ']'
                ),
            },
            {'type': 'heading3', 'content': 'Custom Error Envelopes'},
            {
                'type': 'paragraph',
                'content': (
                    'DRF\'s default error format is inconsistent. A custom exception handler '
                    'normalises every error into the same shape so clients only parse one format.'
                ),
            },
            {
                'type': 'code',
                'language': 'python',
                'content': (
                    'def custom_exception_handler(exc, context):\n'
                    '    response = exception_handler(exc, context)\n'
                    '    if response is not None:\n'
                    '        response.data = {\n'
                    '            "error": {\n'
                    '                "status": response.status_code,\n'
                    '                "message": _flatten_errors(response.data),\n'
                    '            }\n'
                    '        }\n'
                    '    return response'
                ),
            },
            {
                'type': 'callout',
                'callout_variant': 'info',
                'content': (
                    'Always document your error envelope contract in your API spec. '
                    'Frontend teams will thank you.'
                ),
            },
            {'type': 'heading2', 'content': 'Throttling & Rate Limiting'},
            {
                'type': 'paragraph',
                'content': (
                    'DRF ships with AnonRateThrottle and UserRateThrottle out of the box. '
                    'For burst + sustained limits, layer two throttle classes on the same view.'
                ),
            },
            {
                'type': 'code',
                'language': 'python',
                'content': (
                    'REST_FRAMEWORK = {\n'
                    '    "DEFAULT_THROTTLE_CLASSES": [\n'
                    '        "rest_framework.throttling.AnonRateThrottle",\n'
                    '        "rest_framework.throttling.UserRateThrottle",\n'
                    '    ],\n'
                    '    "DEFAULT_THROTTLE_RATES": {\n'
                    '        "anon": "100/day",\n'
                    '        "user": "1000/day",\n'
                    '    },\n'
                    '}'
                ),
            },
            {
                'type': 'list',
                'variant': 'bullet',
                'items': [
                    'Use Redis as the throttle cache backend in production',
                    'Expose X-RateLimit-* headers so clients can back off gracefully',
                    'Log throttle violations — they\'re often the first sign of abuse',
                    'Add custom throttle scopes per endpoint for granular control',
                ],
            },
            {'type': 'heading2', 'content': 'Deployment'},
            {
                'type': 'paragraph',
                'content': (
                    'A Gunicorn + Nginx stack behind a reverse proxy is the standard. '
                    'The key is to get the worker count right: start at 2 × CPU cores + 1 '
                    'and tune from there using response time percentiles, not guesswork.'
                ),
            },
            {
                'type': 'quote',
                'content': (
                    'Premature optimisation is the root of all evil, but measured '
                    'performance tuning is the root of all production stability.'
                ),
                'attribution': 'Every senior engineer, eventually',
            },
            {'type': 'divider'},
            {
                'type': 'tags',
                'items': ['django', 'python', 'rest-apis', 'deployment'],
            },
        ],
    },

    {
        'title': 'PostgreSQL Query Optimisation: From Slow to Sub-millisecond',
        'slug': 'postgresql-query-optimisation',
        'excerpt': (
            'How I took a 4-second report query down to 18 ms using EXPLAIN ANALYZE, '
            'composite indexes, and a single well-placed materialised view.'
        ),
        'featured': False,
        'tags': ['postgresql', 'performance', 'system-design'],
        'blocks': [
            {
                'type': 'paragraph',
                'content': (
                    'The report endpoint had worked fine for months. Then a client '
                    'added 200,000 rows to their account and the request started timing out. '
                    'This is the story of the four hours it took to bring it from 4,200 ms '
                    'down to 18 ms — and the mental model that made it obvious in hindsight.'
                ),
            },
            {'type': 'heading2', 'content': 'Start with EXPLAIN ANALYZE'},
            {
                'type': 'paragraph',
                'content': (
                    'Never guess at query performance. Run EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) '
                    'and read the actual row counts next to the estimated ones. A mismatch of '
                    '10× or more is a red flag that your table statistics are stale or your '
                    'query plan is wrong.'
                ),
            },
            {
                'type': 'code',
                'language': 'sql',
                'content': (
                    'EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)\n'
                    'SELECT\n'
                    '  o.id,\n'
                    '  o.created_at,\n'
                    '  SUM(oi.quantity * oi.unit_price) AS total\n'
                    'FROM orders o\n'
                    'JOIN order_items oi ON oi.order_id = o.id\n'
                    'WHERE o.tenant_id = $1\n'
                    '  AND o.status = \'completed\'\n'
                    '  AND o.created_at >= NOW() - INTERVAL \'30 days\'\n'
                    'GROUP BY o.id, o.created_at\n'
                    'ORDER BY o.created_at DESC;'
                ),
                'caption': 'The offending query',
            },
            {
                'type': 'callout',
                'callout_variant': 'warning',
                'content': (
                    'Never run EXPLAIN ANALYZE on production with a long-running write query. '
                    'It actually executes the query — use a replica or a dry-run environment.'
                ),
            },
            {'type': 'heading2', 'content': 'The Problem: Sequential Scans on Large Tables'},
            {
                'type': 'paragraph',
                'content': (
                    'The plan showed a Seq Scan on order_items with an estimated cost of '
                    '850,000 rows. There was a single-column index on order_id, but '
                    'PostgreSQL chose not to use it because the planner estimated it would '
                    'visit more than ~15% of the table — at which point a sequential scan '
                    'is faster than random I/O through an index.'
                ),
            },
            {'type': 'heading3', 'content': 'Composite Index to the Rescue'},
            {
                'type': 'code',
                'language': 'sql',
                'content': (
                    '-- Before: single column, planner skips it for large result sets\n'
                    'CREATE INDEX idx_orders_tenant ON orders (tenant_id);\n\n'
                    '-- After: composite index covering the WHERE + ORDER BY columns\n'
                    'CREATE INDEX idx_orders_tenant_status_date\n'
                    'ON orders (tenant_id, status, created_at DESC)\n'
                    'WHERE status = \'completed\';  -- partial index'
                ),
            },
            {
                'type': 'paragraph',
                'content': (
                    'The partial index (WHERE status = \'completed\') cuts the index size '
                    'by ~70% in this dataset. Smaller index = fits in shared_buffers = '
                    'faster cache hits. After re-running ANALYZE to refresh statistics, '
                    'the planner switched to an Index Scan with a cost 200× lower.'
                ),
            },
            {'type': 'heading2', 'content': 'Materialised View for Aggregates'},
            {
                'type': 'paragraph',
                'content': (
                    'The SUM aggregation was still expensive because it hit every order_items '
                    'row for the period. For a dashboard that refreshes every 5 minutes, '
                    'a materialised view is the right trade-off.'
                ),
            },
            {
                'type': 'code',
                'language': 'sql',
                'content': (
                    'CREATE MATERIALIZED VIEW mv_order_totals AS\n'
                    'SELECT\n'
                    '  o.tenant_id,\n'
                    '  o.id AS order_id,\n'
                    '  o.created_at,\n'
                    '  SUM(oi.quantity * oi.unit_price) AS total\n'
                    'FROM orders o\n'
                    'JOIN order_items oi ON oi.order_id = o.id\n'
                    'WHERE o.status = \'completed\'\n'
                    'GROUP BY o.tenant_id, o.id, o.created_at;\n\n'
                    'CREATE UNIQUE INDEX ON mv_order_totals (tenant_id, order_id);\n\n'
                    '-- Refresh from a pg_cron job or a background task\n'
                    'REFRESH MATERIALIZED VIEW CONCURRENTLY mv_order_totals;'
                ),
            },
            {
                'type': 'table',
                'caption': 'Query performance before and after',
                'headers': ['Approach', 'Avg latency', 'P99 latency', 'Rows examined'],
                'rows': [
                    ['Original query', '4,200 ms', '6,800 ms', '850,000'],
                    ['Composite index', '320 ms', '480 ms', '12,400'],
                    ['Materialised view', '18 ms', '31 ms', '420'],
                ],
            },
            {
                'type': 'callout',
                'callout_variant': 'success',
                'content': (
                    '18 ms average, 31 ms P99. The endpoint went from timing out to '
                    'being the fastest query in the service.'
                ),
            },
            {'type': 'divider'},
            {
                'type': 'tags',
                'items': ['postgresql', 'performance', 'indexing', 'sql'],
            },
        ],
    },

    {
        'title': 'Redis as More Than a Cache: Queues, Pub/Sub, and Rate Limiting',
        'slug': 'redis-beyond-cache',
        'excerpt': (
            'Most teams use Redis exclusively as a key-value cache. '
            'Here is how to unlock its full value: background queues, '
            'real-time pub/sub fanout, and sliding-window rate limiting.'
        ),
        'featured': False,
        'tags': ['redis', 'system-design', 'python'],
        'blocks': [
            {
                'type': 'paragraph',
                'content': (
                    'Redis gets introduced to most projects as a cache. '
                    'SET key value EX 300, and suddenly your database load drops by 40%. '
                    'But Redis is a data structures server, not just a cache. '
                    'Once you internalise that, your architecture options multiply.'
                ),
            },
            {'type': 'heading2', 'content': 'Background Queues with Redis Lists'},
            {
                'type': 'paragraph',
                'content': (
                    'LPUSH / BRPOP gives you a reliable FIFO queue in two commands. '
                    'Celery uses Redis this way under the hood. For simpler use cases '
                    'you don\'t need Celery at all — a daemon process calling BRPOP in '
                    'a loop is 30 lines of Python and zero extra dependencies.'
                ),
            },
            {
                'type': 'code',
                'language': 'python',
                'content': (
                    'import redis\nimport json\n\nr = redis.Redis()\n\n'
                    '# Producer\n'
                    'def enqueue_email(payload: dict):\n'
                    '    r.lpush("email:queue", json.dumps(payload))\n\n'
                    '# Consumer (runs in a separate process)\n'
                    'def worker():\n'
                    '    while True:\n'
                    '        _, raw = r.brpop("email:queue", timeout=5)\n'
                    '        if raw:\n'
                    '            payload = json.loads(raw)\n'
                    '            send_email(**payload)'
                ),
            },
            {
                'type': 'callout',
                'callout_variant': 'warning',
                'content': (
                    'Plain Redis lists are not durable. If the consumer crashes mid-task '
                    'the job is lost. Use Redis Streams (XADD/XREADGROUP) or Celery '
                    'with REDIS_TASK_SERIALIZER=\'json\' and acks_late=True for durability.'
                ),
            },
            {'type': 'heading2', 'content': 'Pub/Sub for Real-Time Fanout'},
            {
                'type': 'paragraph',
                'content': (
                    'When multiple services need to react to the same event, pub/sub beats '
                    'HTTP callbacks. The publisher doesn\'t need to know who is listening, '
                    'and adding a new subscriber doesn\'t require any changes to the publisher.'
                ),
            },
            {
                'type': 'code',
                'language': 'python',
                'content': (
                    '# Publisher (e.g. in a Django signal or view)\n'
                    'r.publish("orders:completed", json.dumps({"order_id": 42}))\n\n'
                    '# Subscriber (separate service / worker)\n'
                    'pubsub = r.pubsub()\n'
                    'pubsub.subscribe("orders:completed")\n\n'
                    'for message in pubsub.listen():\n'
                    '    if message["type"] == "message":\n'
                    '        handle_order_completed(json.loads(message["data"]))'
                ),
            },
            {'type': 'heading2', 'content': 'Sliding-Window Rate Limiting'},
            {
                'type': 'paragraph',
                'content': (
                    'Fixed-window rate limiting (100 requests per minute, reset at the '
                    'top of each minute) has a well-known doubling attack: send 100 '
                    'requests at 00:59 and 100 more at 01:00. Sliding-window fixes this '
                    'with a sorted set of timestamps.'
                ),
            },
            {
                'type': 'code',
                'language': 'python',
                'content': (
                    'import time\n\n'
                    'def is_rate_limited(user_id: str, limit: int, window_secs: int) -> bool:\n'
                    '    key = f"rl:{user_id}"\n'
                    '    now = time.time()\n'
                    '    window_start = now - window_secs\n\n'
                    '    pipe = r.pipeline()\n'
                    '    pipe.zremrangebyscore(key, 0, window_start)   # remove old\n'
                    '    pipe.zadd(key, {str(now): now})               # add current\n'
                    '    pipe.zcard(key)                                # count in window\n'
                    '    pipe.expire(key, window_secs)\n'
                    '    _, _, count, _ = pipe.execute()\n\n'
                    '    return count > limit'
                ),
            },
            {
                'type': 'list',
                'variant': 'bullet',
                'items': [
                    'No doubling attacks — every request is timestamped precisely',
                    'Atomic pipeline — no race conditions under concurrency',
                    'TTL on the key prevents orphaned data accumulation',
                    'Works across multiple app servers — state lives in Redis, not memory',
                ],
            },
            {
                'type': 'callout',
                'callout_variant': 'info',
                'content': (
                    'For very high-throughput rate limiting, look into Redis modules like '
                    'RedisBloom (probabilistic) or lua scripts to avoid network round trips.'
                ),
            },
            {'type': 'divider'},
            {
                'type': 'tags',
                'items': ['redis', 'queues', 'rate-limiting', 'python'],
            },
        ],
    },

    {
        'title': 'Containerising a Django App with Docker and GitHub Actions',
        'slug': 'django-docker-github-actions',
        'excerpt': (
            'Step-by-step: a multi-stage Dockerfile that produces a lean production '
            'image, Docker Compose for local development, and a GitHub Actions pipeline '
            'that builds, tests, and pushes to a registry on every merge.'
        ),
        'featured': False,
        'tags': ['docker', 'django', 'python'],
        'blocks': [
            {
                'type': 'paragraph',
                'content': (
                    'A reproducible build pipeline is non-negotiable for any serious project. '
                    'Docker gives you environment parity between local, CI, and production. '
                    'GitHub Actions makes the pipeline free for public repos and cheap for '
                    'private ones. Together they eliminate "works on my machine" forever.'
                ),
            },
            {'type': 'heading2', 'content': 'Multi-Stage Dockerfile'},
            {
                'type': 'paragraph',
                'content': (
                    'A naive single-stage Dockerfile installs build tools, compilers, '
                    'and test dependencies into the final image, bloating it from ~100 MB '
                    'to 800 MB+. Multi-stage builds solve this: the builder stage installs '
                    'everything; the production stage copies only the compiled artefacts.'
                ),
            },
            {
                'type': 'code',
                'language': 'dockerfile',
                'content': (
                    '# Stage 1 — builder\n'
                    'FROM python:3.12-slim AS builder\n'
                    'WORKDIR /build\n'
                    'COPY requirements.txt .\n'
                    'RUN pip install --user --no-cache-dir -r requirements.txt\n\n'
                    '# Stage 2 — production image\n'
                    'FROM python:3.12-slim\n'
                    'ENV PYTHONDONTWRITEBYTECODE=1 \\\n'
                    '    PYTHONUNBUFFERED=1 \\\n'
                    '    PATH=/home/app/.local/bin:$PATH\n\n'
                    'RUN useradd --create-home app\n'
                    'USER app\n'
                    'WORKDIR /home/app\n\n'
                    'COPY --from=builder /root/.local /home/app/.local\n'
                    'COPY . .\n\n'
                    'CMD ["gunicorn", "config.wsgi:application", \\\n'
                    '     "--bind", "0.0.0.0:8000", "--workers", "4"]'
                ),
                'caption': 'Final image is ~120 MB vs 840 MB naive',
            },
            {'type': 'heading2', 'content': 'Docker Compose for Local Dev'},
            {
                'type': 'code',
                'language': 'yaml',
                'content': (
                    'services:\n'
                    '  web:\n'
                    '    build: .\n'
                    '    command: python manage.py runserver 0.0.0.0:8000\n'
                    '    volumes:\n'
                    '      - .:/home/app\n'
                    '    ports:\n'
                    '      - "8000:8000"\n'
                    '    env_file: .env.local\n'
                    '    depends_on:\n'
                    '      db:\n'
                    '        condition: service_healthy\n\n'
                    '  db:\n'
                    '    image: postgres:16-alpine\n'
                    '    environment:\n'
                    '      POSTGRES_DB: portfolio\n'
                    '      POSTGRES_USER: dev\n'
                    '      POSTGRES_PASSWORD: dev\n'
                    '    healthcheck:\n'
                    '      test: ["CMD", "pg_isready", "-U", "dev"]\n'
                    '      interval: 5s\n'
                    '      retries: 5\n\n'
                    '  redis:\n'
                    '    image: redis:7-alpine'
                ),
            },
            {'type': 'heading2', 'content': 'GitHub Actions CI/CD'},
            {
                'type': 'code',
                'language': 'yaml',
                'content': (
                    'name: CI\n\n'
                    'on:\n'
                    '  push:\n'
                    '    branches: [main]\n\n'
                    'jobs:\n'
                    '  test:\n'
                    '    runs-on: ubuntu-latest\n'
                    '    services:\n'
                    '      postgres:\n'
                    '        image: postgres:16-alpine\n'
                    '        env:\n'
                    '          POSTGRES_DB: test\n'
                    '          POSTGRES_USER: test\n'
                    '          POSTGRES_PASSWORD: test\n'
                    '        options: >-\n'
                    '          --health-cmd pg_isready\n'
                    '    steps:\n'
                    '      - uses: actions/checkout@v4\n'
                    '      - uses: actions/setup-python@v5\n'
                    '        with: {python-version: "3.12"}\n'
                    '      - run: pip install -r requirements.txt\n'
                    '      - run: python manage.py test\n\n'
                    '  build-and-push:\n'
                    '    needs: test\n'
                    '    runs-on: ubuntu-latest\n'
                    '    steps:\n'
                    '      - uses: actions/checkout@v4\n'
                    '      - uses: docker/build-push-action@v5\n'
                    '        with:\n'
                    '          push: true\n'
                    '          tags: ghcr.io/${{ github.repository }}:latest'
                ),
            },
            {
                'type': 'callout',
                'callout_variant': 'success',
                'content': (
                    'Pin your base image to a digest (python:3.12-slim@sha256:...) '
                    'in production to guarantee reproducible builds and eliminate '
                    'supply-chain drift.'
                ),
            },
            {'type': 'divider'},
            {
                'type': 'tags',
                'items': ['docker', 'ci-cd', 'django', 'github-actions'],
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample blog posts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing blog posts and tags before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            BlogPost.objects.all().delete()
            BlogTag.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared all blog data.'))

        # Create tags
        tag_map = {}
        for t in TAGS:
            tag_obj, created = BlogTag.objects.get_or_create(
                slug=t['slug'],
                defaults={'name': t['name'], 'color': t['color']},
            )
            tag_map[t['slug']] = tag_obj
            status = 'created' if created else 'exists'
            self.stdout.write(f'  Tag [{status}]: {tag_obj.name}')

        # Create posts
        for post_data in POSTS:
            tag_slugs = post_data.pop('tags')
            post_data['status'] = 'published'
            post_data['published_at'] = timezone.now()

            post, created = BlogPost.objects.update_or_create(
                slug=post_data['slug'],
                defaults=post_data,
            )
            post.tags.set([tag_map[s] for s in tag_slugs if s in tag_map])

            status = 'created' if created else 'updated'
            self.stdout.write(self.style.SUCCESS(f'  Post [{status}]: {post.title}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {len(POSTS)} posts, {len(TAGS)} tags seeded.'
        ))
