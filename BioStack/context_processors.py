# BioStack/context_processors.py
import os
from django.urls import resolve
from django.conf import settings

def supabase_config(request):
    return {
        'SUPABASE_URL': os.environ.get('SUPABASE_URL'),
        'SUPABASE_ANON_KEY': os.environ.get('SUPABASE_ANON_KEY'),
    }


def seo_context(request):
    """
    Context processor that provides SEO metadata for different pages.
    """
    domain = request.build_absolute_uri('/').rstrip('/')
    path = request.path
    
    # Default SEO data
    seo_data = {
        'site_name': 'BioStack',
        'site_url': domain,
        'page_url': request.build_absolute_uri(),
        'description': 'BioStack - Your Professional Identity Platform. Create stunning bio links, profiles, and personal websites in minutes.',
        'og_image': f'{domain}/static/images/main-logo.png',
        'keywords': 'bio link, profile, personal website, link aggregator, professional identity',
        'author': 'BioStack Team',
        'locale': 'en_US',
    }
    
    # Page-specific overrides
    page_overrides = {
        '/': {
            'title': 'BioStack | Your Professional Identity',
            'description': 'Create a stunning professional profile and bio link in minutes. Showcase your work, links, and personality all in one place.',
        },
        '/about-us/': {
            'title': 'About Us | BioStack',
            'description': 'Learn about BioStack\'s mission to empower professionals with beautiful, easy-to-use bio links and profiles.',
        },
        '/features/': {
            'title': 'Features | BioStack',
            'description': 'Explore BioStack features: customizable themes, link tracking, analytics, and more. Grow your online presence.',
        },
        '/pricing/': {
            'title': 'Pricing | BioStack',
            'description': 'Choose the perfect plan for your needs. Free and premium options available with no hidden fees.',
        },
        '/auth/login/': {
            'title': 'Login | BioStack',
            'description': 'Sign in to your BioStack account and manage your professional profile.',
            'noindex': True,
        },
        '/auth/signup/': {
            'title': 'Sign Up | BioStack',
            'description': 'Create your BioStack account and start building your professional presence today.',
            'noindex': True,
        },
        '/dashboard/': {
            'title': 'Dashboard | BioStack',
            'description': 'Manage your profiles, customize themes, and track link analytics.',
            'noindex': True,
        },
        '/profile/me/': {
            'title': 'My Profiles | BioStack',
            'description': 'Manage and customize your BioStack profiles.',
            'noindex': True,
        },
        '/blogs/': {
            'title': 'Blog | BioStack',
            'description': 'Read articles about building your professional presence, personal branding, and productivity tips.',
        },
        '/terms/': {
            'title': 'Terms of Service | BioStack',
            'description': 'BioStack Terms of Service and Legal Information.',
            'noindex': True,
        },
        '/privacy/': {
            'title': 'Privacy Policy | BioStack',
            'description': 'How BioStack protects your privacy and personal data.',
            'noindex': True,
        },
        '/careers/': {
            'title': 'Careers | BioStack',
            'description': 'Join the BioStack team. We\'re looking for talented individuals to help us build the future.',
        },
    }
    
    # Check if we have specific overrides for this path
    if path in page_overrides:
        seo_data.update(page_overrides[path])
    elif path.startswith('/profile/') or path.startswith('/blogs/'):
        # For blog and profile detail pages, keep default title but could be overridden in views
        if path.startswith('/blogs/'):
            seo_data['title'] = 'Blog | BioStack'
    else:
        # Default title for pages without specific overrides
        seo_data['title'] = 'BioStack | Your Professional Identity'
    
    # Add Twitter card data
    seo_data['twitter_card'] = 'summary_large_image'
    seo_data['twitter_creator'] = '@BioStackApp'
    
    return {'seo': seo_data}