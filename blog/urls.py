from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static
app_name='blog'

urlpatterns = [
    path('', views.home , name='home'),
    path('post/', views.post , name='post'),
    path('page/', views.page , name='page'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)