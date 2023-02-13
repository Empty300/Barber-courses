from django.shortcuts import render
from django.views.generic import ListView

from store.models import Lessons


def index_page(request):
    return render(request, 'store/index.html')


class LessonsListView(ListView):
    model = Lessons
    template_name = 'store/portfolio-details.html'
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = Lessons.objects.all()
        return queryset

