from django.shortcuts import render
from .models import Prayer

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
