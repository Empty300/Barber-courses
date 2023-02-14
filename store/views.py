from django.shortcuts import render
from django.views.generic import ListView, CreateView

from store.models import Lessons
from users.forms import UserRegistrationForm
from users.models import User


class IndexPageView(CreateView):
    model = User
    template_name = 'store/index.html'
    form_class = UserRegistrationForm


class LessonsListView(ListView):
    model = Lessons
    template_name = 'store/portfolio-details.html'

    def get_queryset(self):
        queryset = Lessons.objects.all()
        return queryset
