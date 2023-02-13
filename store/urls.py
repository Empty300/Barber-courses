
from django.urls import path, include

from store.views import index_page, LessonsListView

urlpatterns = [
    path('', index_page, name='store'),
    path('lessons/', LessonsListView.as_view(), name='Уроки')
]
