from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('hospital/', views.HospitalListView.as_view(), name='hospital'),
    path('hospital/<int:pk>/', views.HospitalDetailView.as_view(), name='hospital_detail'),
]