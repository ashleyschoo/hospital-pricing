from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('hospital/', views.HospitalListView.as_view(), name='hospital'),
    path('hospital/<int:pk>/', views.HospitalDetailView.as_view(), name='hospital_detail'),
    path('hospital/new/', views.HospitalCreateView.as_view(), name='hospital_new'),
	path('hospital/<int:pk>/delete/', views.HospitalDeleteView.as_view(), name='hospital_delete'),
	path('hospital/<int:pk>/update/', views.HospitalUpdateView.as_view(), name='hospital_update'),
	path('hospital_filter/', views.HospitalFilterView.as_view(), kwargs=None, name='hospital_filter'),

 #    path('pricing/', views.PricingListView.as_view(), name='pricing'),
 #    path('pricing/<int:pk>/', views.PricingDetailView.as_view(), name='pricing_detail'),
 #    path('hospital/new/', views.HospitalCreateView.as_view(), name='hospital_new'),
	# path('hospital/<int:pk>/delete/', views.HospitalDeleteView.as_view(), name='hospital_delete'),
	# path('hospital/<int:pk>/update/', views.HospitalUpdateView.as_view(), name='hospital_update'),
	# path('hospital_filter/', views.HospitalFilterView.as_view(), kwargs=None, name='hospital_filter'),	

]