from django.urls import path

from movies.api.v1 import views

urlpatterns = [
    path('movies/', views.MoviesList.as_view()),
    path('movies/<uuid:pk>/', views.MoviesDetail.as_view())
]

