from django.urls import path
from . import views


urlpatterns = [
    path('upload-link/', views.UploadLinkView.as_view(), name="rest-upload-link"),
    path('upload-file/', views.UploadFileView.as_view(), name="rest-upload-file"),
    path('secure-link/', views.SecureLinkView.as_view(), name="rest-secure-link"),
    path('secure-file/', views.SecureFileView.as_view(), name="rest-secure-file")
]