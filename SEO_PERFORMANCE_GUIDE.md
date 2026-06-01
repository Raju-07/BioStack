# BioStack SEO & Performance Optimization Guide

## Overview
This document outlines all SEO and performance improvements implemented for BioStack as of May 31, 2026.

## 🎯 URL Structure Changes

### Before & After
```
Before: biostack.site/profiles/username/profile-slug/
After:  biostack.site/username/profile-slug/
```

### Implementation Details
- Clean, SEO-friendly URLs without "profiles" prefix
- Catch-all pattern at root level: `<str:username>/<slug:profile_slug>/`
- **Note**: This must be the last URL pattern to avoid conflicts

### Files Changed
- `BioStack/urls.py` - Added public profile catch-all URL
- `profiles/urls.py` - Removed old pattern
- All templates updated to use `public_profile` URL name instead of `profiles:public`

---

## 🔍 SEO Enhancements

### 1. Meta Tags & Social Media Optimization
**Location**: `BioStack/context_processors.py` - `seo_context()` function

Every page now includes:
- ✅ Meta descriptions (unique per page)
- ✅ Open Graph tags (og:title, og:description, og:image, og:url)
- ✅ Twitter Card tags
- ✅ Canonical URLs
- ✅ Robots meta tags (noindex for authenticated pages)
- ✅ Language and revisit-after tags

**Page-Specific Overrides**:
```python
'/': Home page with rich description
'/about-us/': About page
'/features/': Features page
'/pricing/': Pricing page
'/blogs/': Blog listing
'/auth/login/': Has noindex tag (private)
'/dashboard/': Has noindex tag (private)
```

### 2. XML Sitemap
**Location**: `BioStack/views.py` - `sitemap_xml()` view
**URL**: `/sitemap.xml`

Dynamically generates sitemap with:
- All static pages (priority & changefreq optimized)
- All public profiles (priority 0.7, weekly update)
- Proper XML formatting for search engines

**Priorities Used**:
- Homepage: 1.0
- Features/About: 0.9
- Public Profiles: 0.7
- Secondary Pages: 0.5-0.8

### 3. Robots.txt
**Location**: `BioStack/views.py` - `robots_txt()` view
**URL**: `/robots.txt`

Allows:
- Public pages indexing
- Public profiles indexing

Disallows:
- Admin panel `/admin/`
- Authentication `/auth/`
- Dashboard `/dashboard/`
- User profile management `/profile/me/`

### 4. JSON-LD Structured Data
**Locations**: 
- `templates/base.html` - Organization & Website schema
- `templates/home.html` - Product/SoftwareApplication schema

**Schemas Implemented**:
```json
1. WebSite Schema - Enables site search feature
2. Organization Schema - Brand information & contact
3. SoftwareApplication Schema - Product details with ratings
```

Benefits:
- Enhanced Google Search results (rich snippets)
- Better voice search compatibility
- Improved knowledge graph appearance

---

## ⚡ Performance Optimizations

### 1. GZip Compression
**Location**: `BioStack/settings.py` - MIDDLEWARE

Reduces response size by ~60-70%:
```python
MIDDLEWARE = [
    ...
    'django.middleware.gzip.GZipMiddleware',
    ...
]
```

### 2. Static Files Compression & Caching
**Location**: `BioStack/settings.py` - STATICFILES_STORAGE

```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

- Minifies and compresses CSS/JS
- Adds hash fingerprints (cache busting)
- Browser caches forever with new filename

### 3. In-Memory Caching
**Location**: `BioStack/settings.py` - CACHES

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'biostack-cache',
        'OPTIONS': {'MAX_ENTRIES': 10000}
    }
}
CACHE_TIMEOUT = 3600  # 1 hour
```

**Usage Example**:
```python
from django.views.decorators.cache import cache_page

@cache_page(3600)  # Cache for 1 hour
def my_view(request):
    pass
```

### 4. Database Connection Pooling
**Location**: `BioStack/settings.py`

```python
DATABASE_CONN_MAX_AGE = 600  # Reuse connections for 10 minutes
```

### 5. Query Optimization
**Location**: `profiles/views.py`

Eliminated N+1 queries using:
- `select_related()` - For ForeignKey relationships
- `prefetch_related()` - For reverse relationships

**Example**:
```python
# Before (N+1 queries)
profiles = request.user.profiles.all()

# After (Optimized)
profiles = request.user.profiles.select_related('theme').all()
```

---

## 🔒 Security Headers (Production Only)

**Location**: `BioStack/settings.py`

Applied when `DEBUG=False`:

### HTTPS & Certificate Pinning
```python
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Cookie Security
```python
SESSION_COOKIE_SECURE = True  # HTTPS only
CSRF_COOKIE_SECURE = True
```

### Content Security Policy
Whitelist for:
- Scripts: Self, Tailwind CDN, JSDelivr
- Styles: Self, Tailwind, Google Fonts
- Images: Self, data URIs, HTTPS
- Fonts: Self, Google Fonts

### Clickjacking Protection
```python
X_FRAME_OPTIONS = 'DENY'
```

---

## 📊 Monitoring & Maintenance

### Key Metrics to Track
1. **Core Web Vitals** (Google PageSpeed Insights)
   - Largest Contentful Paint (LCP)
   - First Input Delay (FID)
   - Cumulative Layout Shift (CLS)

2. **SEO Health**
   - Crawl rate in Google Search Console
   - Index coverage
   - Click-through rate (CTR)

3. **Performance**
   - Page load time
   - Cache hit rate
   - Database query count

### Testing Checklist
- [ ] URLs work: `biostack.site/username/slug/`
- [ ] `/robots.txt` returns valid content
- [ ] `/sitemap.xml` lists all profiles
- [ ] Meta tags present in `<head>` section
- [ ] JSON-LD validates at schema.org/validator
- [ ] Static files compressed and minified
- [ ] HTTPS redirects working
- [ ] Security headers present in response

---

## 🚀 Future Improvements

### Short Term
1. **Image Optimization**
   - Implement WebP format with fallbacks
   - Add lazy loading with `loading="lazy"`
   - Optimize profile image thumbnails

2. **Advanced Caching**
   - Redis for better cache performance
   - Caching on CDN level
   - Cache invalidation on profile updates

3. **Performance Enhancements**
   - Critical CSS extraction
   - Preload important fonts
   - Service Workers for offline support

### Medium Term
1. **SEO Expansion**
   - Blog schema for articles
   - Breadcrumb schema
   - Event schema (if applicable)
   - FAQ schema

2. **Analytics Integration**
   - Core Web Vitals tracking
   - User behavior analytics
   - Heatmap tracking

3. **Mobile Optimization**
   - AMP pages (if beneficial)
   - Mobile-specific meta tags
   - Touch-friendly interactions

### Long Term
1. **Internationalization (i18n)**
   - Multi-language support
   - hreflang tags for language variants
   - Localized sitemaps

2. **Advanced Features**
   - GraphQL API optimization
   - Edge caching with Cloudflare
   - Auto-generated meta descriptions (AI)

---

## 🔧 Developer Guide

### Adding Cache to Views
```python
from django.views.decorators.cache import cache_page

@cache_page(3600)  # Cache for 1 hour
def my_expensive_view(request):
    # Your view logic
    pass
```

### Clearing Cache
```python
from django.core.cache import cache
cache.clear()  # Clear all
cache.delete('specific_key')  # Delete specific
```

### Checking Query Count (Debug Mode)
```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as ctx:
    # Your code here
    pass

print(f"Queries executed: {len(ctx.captured_queries)}")
for q in ctx.captured_queries:
    print(q['sql'])
```

### Adding SEO to New Pages

1. Update context processor page_overrides:
```python
page_overrides = {
    '/new-page/': {
        'title': 'New Page | BioStack',
        'description': 'Description for search engines...',
    },
}
```

2. Add JSON-LD if needed:
```html
{% block structured_data %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CustomSchema",
  ...
}
</script>
{% endblock %}
```

---

## 📚 Resources

- [Google Search Central](https://developers.google.com/search)
- [JSON-LD Documentation](https://json-ld.org/)
- [Django Performance Guide](https://docs.djangoproject.com/en/6.0/topics/performance/)
- [Web Vitals Guide](https://web.dev/vitals/)
- [Schema.org](https://schema.org/)

---

**Last Updated**: May 31, 2026  
**Django Version**: 6.0  
**Python Version**: 3.10+
