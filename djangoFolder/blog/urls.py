from django.urls import path
from .views import BlogListView,BlogDetailView,BlogCreateView,BlogUpdateView,BlogDeleteView,RegistrationFormView\
    ,HomeTemplateView,LoginView,Logout
from django.contrib.auth.decorators import  login_required

urlpatterns = [
    path('',BlogListView.as_view(),name='home'),
    path('post/<int:id>/',login_required(BlogDetailView),name='post_detail'),
    path('post/new',login_required(BlogCreateView.as_view()),name='post_new'),
    path('post/<int:pk>/edit',login_required(BlogUpdateView.as_view()),name='post_edit'),
    path('post/<int:pk>/delete',login_required(BlogDeleteView.as_view()),name='post_delete'),
    path('register/',RegistrationFormView,name='register'),
    path('login/',LoginView,name='login'),
    #path('',HomeTemplateView.as_view(),name='landing'),
    path('user/<int:id>/logout/',Logout,name='logout'),
]