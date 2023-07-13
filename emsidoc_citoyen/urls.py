from django.urls import path
from . import views


urlpatterns = [
    path('', views.indexC, name='indexC'),
    path('/DocForm', views.docform, name='docform'),
    path('/delete/<int:id>', views.delete, name='deleteC'),
       path('/logout/', views.logout_view, name='logout'),

]