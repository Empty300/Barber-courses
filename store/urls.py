
from django.urls import path, include

from store.views import index_page

urlpatterns = [
    path('', index_page, name='store'),
]
