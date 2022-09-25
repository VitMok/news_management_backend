from django.urls import path

from . import views


urlpatterns = [
    path('parsing/', views.NewsParsingView.as_view()),
    path('news/', views.NewsListView.as_view()),
]
