
from django.contrib import admin
from django.urls import path, include
from uni import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index_view),
    path('index/', views.index_view),
    path('host/', views.host_view),
    path('client/', views.client_view),
    path('A/', views.A_view),
    path('B/', views.B_view),
    path('seperate/', views.seperate),
    path('delete/', views.delete),
    path('sendmess/', views.sendmess),
    path('chat_with_ai/', views.chat_with_ai),
    path('chat_with_ai_cloth/', views.chat_with_ai_cloth),
    path('stream/', views.stream_view),
    path('cloth/', views.cloth_view),
    path('alert/', views.alert_view),
    path('alert1/', views.alert1_view),
    path('create_notification/', views.create_notification, name='create_notification'),
    path('check_notifications/', views.check_notifications, name='check_notifications'),
    path('create_direct_notification/', views.create_direct_notification, name='create_direct_notification'),
    path('check_ns/', views.check_ns, name='check_ns'),

    
]
