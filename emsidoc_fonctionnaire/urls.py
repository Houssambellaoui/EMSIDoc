from django.urls import path
from . import views


urlpatterns = [
    path('/', views.index2, name='index2'),
    path('/files', views.files, name='files'),
    path('/delete/<int:id>', views.delete, name='delete'),
    path('/document/<int:id>/', views.document_detail, name='document_detail'),
    path('/logout/', views.logout_view, name='logout'),



]  