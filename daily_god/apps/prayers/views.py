from django.shortcuts import render
from .models import Prayer
from .forms import PrayerForm
import logging

logger = logging.getLogger('app')

# Create your views here.
def get_prayer(request, id):
    try:
        prayer = Prayer.objects.get(id=id)
    except Prayer.DoesNotExist:
        prayer = None
    
    if prayer:
        context = {
            'content': prayer,
            'type': 'prayer',
        }
        return render(request, 'components/modal.html', context=context)
    
    return None

def submit_new_prayer(request):
    
    if request.method == 'POST':
        form = PrayerForm(request.POST)
        
        if form.is_valid():
            prayer = form.save(commit=False)
            prayer.posted_by = request.user
            prayer.save()
        
        logger.debug(f'Form Errors: {form.errors}')

    return render(request, 'posts/new_post.html#prayer-quote-form')