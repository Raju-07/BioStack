from django.shortcuts import render, redirect
from profiles.models import Profile,LinkClick,ProfileView
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta,date
import json

def dashboard_view(request):
    profile_id = request.session.get("active_profile_id")
    profile = None
    if profile_id:
        profile = Profile.objects.filter(id=profile_id, user=request.user).first()

    if not profile:
        return redirect("profiles:list")

    # --- 1. KEY METRICS ---
    stats = {
        'views': ProfileView.objects.filter(profile=profile).count(),
        'clicks': LinkClick.objects.filter(profile_section__profile=profile).count(),
        'ctr': 0
    }
    if stats['views'] > 0:
        stats['ctr'] = round((stats['clicks'] / stats['views']) * 100, 1)

    # --- 2. CHART DATA & DAILY TRENDS ---
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    
    date_list = [today - timedelta(days=i) for i in range(6, -1, -1)]
    
    # Init dicts
    daily_views = {date: 0 for date in date_list}
    daily_clicks = {date: 0 for date in date_list}

    # Query Views
    views_qs = ProfileView.objects.filter(
        profile=profile, timestamp__date__gte=date_list[0]
    ).annotate(date=TruncDate('timestamp')).values('date').annotate(count=Count('id'))
    
    for entry in views_qs:
        daily_views[entry['date']] = entry['count']

    # Query Clicks
    clicks_qs = LinkClick.objects.filter(
        profile_section__profile=profile, timestamp__date__gte=date_list[0]
    ).annotate(date=TruncDate('timestamp')).values('date').annotate(count=Count('id'))

    for entry in clicks_qs:
        daily_clicks[entry['date']] = entry['count']

    # Calculate "Growth" (Today vs Yesterday)
    views_today = daily_views.get(today, 0)
    views_yesterday = daily_views.get(yesterday, 0)
    
    clicks_today = daily_clicks.get(today, 0)
    
    # --- 3. RECENT ACTIVITY ---
    recent_activity = ProfileView.objects.filter(profile=profile).order_by('-timestamp')[:5]

    # --- 4. SMART PROFILE HEALTH CHECK ---
    # We build a list of missing items to show the user
    score = 0
    missing_actions = []

    if profile.profile_image: 
        score += 20
    else:
        missing_actions.append({'label': 'Upload Profile Picture', 'points': 20, 'url': 'profiles:sections'}) # Redirect to edit

    if profile.bio: 
        score += 20
    else:
        missing_actions.append({'label': 'Write a Bio', 'points': 20, 'url': 'profiles:sections'})

    if profile.sections.count() > 0: 
        score += 30
    else:
        missing_actions.append({'label': 'Add First Link/Section', 'points': 30, 'url': 'profiles:sections'})

    if profile.theme: 
        score += 10
    else:
        missing_actions.append({'label': 'Select a Theme', 'points': 10, 'url': 'profiles:themes'})

    if stats['views'] > 0: 
        score += 20
    else:
        # This one they can't "fix" by clicking, just waiting
        missing_actions.append({'label': 'Get your first visitor', 'points': 20, 'url': None})
    
    completion_score = min(score, 100)

    data = {
        'profile': profile,
        'stats': stats,
        # Trend Data
        'views_today': views_today,
        'views_trend': views_today - views_yesterday, # Positive or negative number
        'clicks_today': clicks_today,
        # Health Data
        'completion_score': completion_score,
        'missing_actions': missing_actions,
        'recent_activity': recent_activity,
        # Chart JSON
        'chart_labels': json.dumps([date.strftime("%a") for date in daily_views.keys()]),
        'chart_views': json.dumps(list(daily_views.values())),
        'chart_clicks': json.dumps(list(daily_clicks.values())),
    }

    return render(request, "dashboard/index.html", data)
