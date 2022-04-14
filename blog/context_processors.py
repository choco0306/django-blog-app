from email import contentmanager
from django.db.models import Count, Q
from blog.models import Category, Tag

def common(request):
    context = {
        'categoryies': Category.objects.annotate(
            count=Count('post', Q(post__is_published=True))
        ),
        'tags': Tag.objects.all(),
    }

    return context