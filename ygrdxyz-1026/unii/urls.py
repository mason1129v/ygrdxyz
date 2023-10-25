
from django.contrib import admin
from django.urls import path, include
from uni import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index_view),
    path('index/', views.index_view),
    path('host/', views.host_view),
    path('client/', views.client_view),
    path('seperate/', views.seperate),
    path('delete/', views.delete),
    path('sendmess/', views.sendmess),
    path('chat_with_ai/', views.chat_with_ai),
    path('stream/', views.stream_view),
]
