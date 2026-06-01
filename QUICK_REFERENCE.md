# BioStack - Quick Reference & Testing Guide

## 🚀 Quick Start After Changes

### 1. Verify URLs Work
```bash
# Test new profile URL structure
curl -I https://biostack.site/username/profile-slug/

# Should return 200 OK
```

### 2. Check SEO Endpoints
```bash
# Test robots.txt
curl https://biostack.site/robots.txt

# Test sitemap
curl https://biostack.site/sitemap.xml

# Both should return valid content
```

### 3. Verify Meta Tags (Local Development)
```bash
# Start Django shell
python manage.py shell

# Test context processor
from BioStack.context_processors import seo_context
from django.test import RequestFactory

factory = RequestFactory()
request = factory.get('/')
seo_data = seo_context(request)
print(seo_data['seo'])
```

---

## 🧪 Testing Checklist

### Automated Tests
```bash
# Run Django tests
python manage.py test

# Check for syntax errors
python manage.py check

# Migrate any pending migrations
python manage.py migrate
```

### Manual Testing - Browser
1. Open browser DevTools (F12)
2. Go to Network tab
3. Visit: `https://biostack.site/`
4. Verify:
   - [ ] Static files are compressed (size < original)
   - [ ] Gzip encoding shown in Response Headers
   - [ ] CSS/JS files have hash fingerprints (e.g., `main.a1b2c3d4.css`)

### Manual Testing - Meta Tags
```bash
# Test with curl
curl -s https://biostack.site/ | grep -o '<meta [^>]*>'

# Or in browser, right-click → View Page Source
# Look for:
# - <meta name="description">
# - <meta property="og:title">
# - <link rel="canonical">
# - <script type="application/ld+json">
```

### Structured Data Validation
1. Visit: https://schema.org/validator
2. Paste your URL: `https://biostack.site/`
3. Verify no errors

### SEO Tools Integration

#### Google Search Console
```
1. Add property: biostack.site
2. Upload sitemap: https://biostack.site/sitemap.xml
3. Check:
   - Coverage (indexed pages)
   - Mobile usability
   - Core Web Vitals
```

#### Lighthouse Audit (DevTools)
```
1. Open DevTools → Lighthouse
2. Run audit for:
   - Performance
   - Accessibility
   - Best Practices
   - SEO
3. Target: 90+ on all categories
```

#### Google PageSpeed Insights
```
Visit: https://pagespeed.web.dev/
Enter URL: https://biostack.site/
Check metrics:
- Largest Contentful Paint (LCP) < 2.5s
- First Input Delay (FID) < 100ms
- Cumulative Layout Shift (CLS) < 0.1
```

---

## 📝 Configuration Changes Reference

### Environment Variables (if needed)
```bash
# No new environment variables required
# Existing ones still apply:
ALLOWED_HOSTS=biostack.site
DEBUG=False  # Critical for security headers
SECRET_KEY=your_secret_key
```

### Database Settings - No Changes Required
Existing PostgreSQL configuration remains the same.

### Cache Configuration
Current: In-memory cache (LocMemCache)
For production upgrade to Redis:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

---

## 🔧 Common Commands

### Clear Cache
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

### Check Database Queries (Debug Mode Only)
```python
# In Django shell
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as ctx:
    from profiles.models import Profile
    profiles = Profile.objects.select_related('theme').all()
    list(profiles)

print(f"Queries: {len(ctx.captured_queries)}")
for query in ctx.captured_queries:
    print(query['sql'])
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput

# This will:
# - Compress CSS/JS
# - Add hash fingerprints
# - Copy to STATIC_ROOT
```

### Generate Sitemap (test)
```bash
python manage.py shell
>>> from BioStack.views import sitemap_xml
>>> from django.test import RequestFactory
>>> factory = RequestFactory()
>>> request = factory.get('/sitemap.xml')
>>> response = sitemap_xml(request)
>>> print(response.content.decode())
```

---

## 🐛 Troubleshooting

### Issue: URLs not working (404 on new profile URLs)
**Solution**:
```bash
# Clear Django cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()

# Restart server
# Verify profiles/urls.py doesn't have the catch-all pattern
```

### Issue: Static files not compressing
**Check**:
1. `DEBUG = False` in settings
2. Run `collectstatic`:
   ```bash
   python manage.py collectstatic --noinput
   ```
3. Verify WhiteNoise middleware is first:
   ```python
   MIDDLEWARE = [
       'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be first
       ...
   ]
   ```

### Issue: Meta tags not showing
**Check**:
1. Context processor registered:
   ```python
   'BioStack.context_processors.seo_context',  # Must be in TEMPLATES
   ```
2. Template includes SEO block:
   ```html
   <meta name="description" content="{{ seo.description }}" />
   ```
3. Clear browser cache (Ctrl+Shift+Delete)

### Issue: HTTPS security warnings
**Solution**:
```python
# Ensure in production settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Also set in web server (Nginx/Apache)
```

---

## 📈 Performance Baseline

### Before Optimizations (Example)
- Homepage load time: ~3.2s
- Largest Contentful Paint: ~2.8s
- Total JS size: ~450KB
- Total CSS size: ~280KB

### After Optimizations (Expected)
- Homepage load time: ~1.2s (62% improvement)
- Largest Contentful Paint: ~0.9s (68% improvement)
- Total JS size: ~140KB (69% gzipped)
- Total CSS size: ~85KB (70% gzipped)

---

## 📋 Deployment Checklist

- [ ] DEBUG = False in production settings
- [ ] ALLOWED_HOSTS configured correctly
- [ ] SECRET_KEY is strong and hidden
- [ ] Static files collected (`collectstatic`)
- [ ] Database migrations applied (`migrate`)
- [ ] HTTPS certificate installed
- [ ] Security headers verified in production
- [ ] Sitemap and robots.txt accessible
- [ ] Google Search Console set up
- [ ] Analytics tracking code added
- [ ] Backup database before deploying
- [ ] Test URLs with prod domain

---

## 🎓 Learning Resources

### Django Performance
- Official: https://docs.djangoproject.com/en/6.0/topics/performance/
- Query optimization patterns

### SEO Best Practices
- Google Search Central: https://developers.google.com/search
- Yoast SEO Guide: https://yoast.com/

### Schema Markup
- JSON-LD: https://json-ld.org/
- Schema.org: https://schema.org/
- Structured Data Testing: https://validator.schema.org/

### Web Performance
- Core Web Vitals: https://web.dev/vitals/
- Lighthouse: https://developers.google.com/web/tools/lighthouse
- WebPageTest: https://www.webpagetest.org/

---

## 📞 Support & Questions

For issues or questions about these implementations:
1. Check SEO_PERFORMANCE_GUIDE.md (comprehensive guide)
2. Review relevant Django documentation
3. Test in development environment first
4. Use browser DevTools for debugging

---

**Last Updated**: May 31, 2026  
**Status**: All optimizations active
