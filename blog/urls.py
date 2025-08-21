from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static
app_name='blog'

urlpatterns = [
    path('', views.home , name='home'),
    path('post/<slug:slug>/', views.post , name='post'),
    path('page/<slug:slug>/', views.page, name='page'),
    path('created_by/<int:author_pk>/', views.created_by, name='created_by'),
    path('category/<slug:slug>/', views.category, name='category'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)