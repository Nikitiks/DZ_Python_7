from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', views.get_tasks, name="getTasks"),
    path('tasks/add/', views.add_task, name="addTask"),
    path('task/delete/<int:id>/',views.delete_task, name='deleteTask'),
    path('getItem/<int:id>/', views.getItemById, name="ItemByIdPage"),
    path('postbook/', views.postBookJson, name="postBookPage"),
    path('', views.redirectUserAgent, name="homePage"),
    path('mobile-home/', views.mobilePage, name="mobilePage"),
    path('pc-home', views.pcPage, name="pcPage"),
    path('data/<str:key>/', views.getData, name="getData"),
    path('update-data/', views.postData, name="postData"),
]