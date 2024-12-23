def get_model():
    from .models import SeedComment
    return SeedComment

def get_form():
    from .forms import SeedCommentForm
    return SeedCommentForm