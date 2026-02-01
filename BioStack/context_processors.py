# BioStack/context_processors.py
import os

def supabase_config(request):
    return {
        'SUPABASE_URL': os.environ.get('SUPABASE_URL'),
        'SUPABASE_ANON_KEY': os.environ.get('SUPABASE_ANON_KEY'),
    }