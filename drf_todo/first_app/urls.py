from django.urls import path,include
from django.contrib import admin
from .views import todo_list,todo_detail,ToDoView,ToDoDetailView,GenericAPIView


urlpatterns = [
    # path('list/',ToDoView.as_view()),
    path('detail/<int:pk>/',ToDoDetailView.as_view()),
    path('generic/<int:pk>/',GenericAPIView.as_view()),
    path('',ToDoView.as_view()),
]







