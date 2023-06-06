from django.contrib import admin
from django.urls import path, include
from chat import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),
    path('index/', views.index_view),
    path('host/', views.host_view),
    path('client/', views.client_view),
    path('client_sp/', views.sp_view),
    path('seperate/', views.seperate),
    path('delete/', views.delete),
    path('stream/', views.stream_view),
    path('videos/', views.videos_view),
    path('login/', views.login_view),
    path('signup/', views.signup_view),
    # path('sendmess/', views.sendmess),
]
