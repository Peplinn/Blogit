from django.urls import path
from . import views
from .views import (
    TaleListView,
    TaleDetailView,
    TaleCreateView,
    TaleUpdateView,
    TaleDeleteView,
    UserTaleListView
)


urlpatterns = [
    # path('', PostListView.as_view(), name='blog-home'),
    path('', views.home, name='blog-home'),
    path('user/<str:username>', UserTaleListView.as_view(), name='user-tales'),
    path('tale/<int:pk>/', TaleDetailView.as_view(), name='tale-detail'), #pk - Primary Key/ ID. Can change the name pk by adding an attribute to the class
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # path('post/new/', PostCreateView.as_view(), name='post-create'), #<model>/_<form>
    path('about/', views.about, name='blog-about'),
    path('tales/', TaleListView.as_view(), name='blog-tales'),
]