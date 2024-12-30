from django.shortcuts import render
from .models import Quote
# Create your views here.

def get_quote(request, id):
    try:
        quote = Quote.objects.get(id=id)
    except Quote.DoesNotExist:
        quote = None
    
    if quote:
        context = {
            'content': quote,
            'type': 'quote',
        }
        return render(request, 'components/modal.html', context=context)
    
    return None