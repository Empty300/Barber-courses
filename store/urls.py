
from django.urls import path

from store.views import LessonsListView, IndexPageView

app_name = 'store'

urlpatterns = [
    path('', IndexPageView.as_view(), name='store'),
    path('lessons/', LessonsListView.as_view(), name='Уроки'),
]
