from django.urls import path

from example_project import views


urlpatterns = [
    path('test/', views.test, name='test')
]
