from django.shortcuts import render
from .models import Quote
from .forms import QuoteForm
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

def submit_new_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        
        if form.is_valid():
            prayer = form.save(commit=False)
            prayer.posted_by = request.user
            prayer.save()

    return render(request, 'posts/new_post.html#prayer-quote-form')