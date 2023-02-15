
from django.urls import path

from store.views import IndexPageView, LessonsDetailView, OrderCreateView

app_name = 'store'

urlpatterns = [
    path('', IndexPageView.as_view(), name='store'),
    path('lessons/<int:pk>/', LessonsDetailView.as_view(), name='lessons'),
    path('order/<int:pk>/', OrderCreateView.as_view(), name='order'),
]
