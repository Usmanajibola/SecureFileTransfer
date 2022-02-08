from django.urls import path
from . import views


# app_name = 'files'
urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('link/', views.LinkView.as_view(), name='link'),
    path('file/', views.FileView.as_view(), name='file'),
    path('secure-link/<str:signed_pk>/', views.SecureLinkView.as_view(), name='secure-link'),
    path('secure-file/<str:signed_pk>/', views.SecureFileView.as_view(), name='secure-file'),
    path('login/', views.LoginView.as_view(), name="login"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('logout/', views.LogoutView.as_view(), name="logout")
]