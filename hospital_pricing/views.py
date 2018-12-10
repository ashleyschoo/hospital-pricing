from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.forms import ModelForm
from hospital_pricing.forms import forms
# import django_filters
# from django_filters.views import FilterView
from django.conf.urls import url
# Create your views here.
from .models import Hospital
from .forms import HospitalPricingForm




def index(request):
	return HttpResponse("Hello, world. Come explore United States Hospitals")

class HomePageView(generic.TemplateView):
	template_name = 'hospital_pricing/home.html'

class AboutPageView(generic.TemplateView):
	template_name = 'hospital_pricing/about.html'


@method_decorator(login_required, name='dispatch')
class HospitalListView(generic.ListView): 
	model = Hospital
	context_object_name = 'hospitals'
	template_name = 'hospital_pricing/hospital.html'
	paginate_by = 20

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Hospital.objects\
				.select_related('hospital_ownership', 'hospital_quality_score')\
				.order_by('hospital_name')

@method_decorator(login_required, name='dispatch')
class HospitalDetailView(generic.DetailView):
	model = Hospital
	context_object_name = 'hospital'
	template_name = 'hospital_pricing/hospital_detail.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class HospitalCreateView(generic.View):
	model = Hospital
	form_class = HospitalPricingForm
	success_message = "Hospital created successfully"
	template_name = 'hospital/hospital_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('heritagesites/site_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = HospitalPricingForm(request.POST)
		if form.is_valid():
			site = form.save(commit=False)
			site.save()
			for charge in form.cleaned_data['hospital']:
				HospitalPricing.objects.create(hospital=site, pricing=charge)
			return redirect(site) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(site.get_absolute_url())
		return render(request, 'hospital_pricing/hospital_new.html', {'form': form})

	def get(self, request):
		form = HospitalPricingForm()
		return render(request, 'hospital_pricing/hospital_new.html', {'form': form})




@method_decorator(login_required, name='dispatch')
class SiteUpdateView(generic.UpdateView):
	model = HeritageSite
	form_class = HeritageSiteForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'site'
	# pk_url_kwarg = 'site_pk'
	success_message = "Heritage Site updated successfully"
	template_name = 'heritagesites/site_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		site = form.save(commit=False)
		# site.updated_by = self.request.user
		# site.date_updated = timezone.now()
		site.save()

		# Current country_area_id values linked to site
		old_ids = HeritageSiteJurisdiction.objects\
			.values_list('country_area_id', flat=True)\
			.filter(heritage_site_id=site.heritage_site_id)

		# New countries list
		new_countries = form.cleaned_data['country_area']

		# TODO can these loops be refactored?

		# New ids
		new_ids = []

		# Insert new unmatched country entries
		for country in new_countries:
			new_id = country.country_area_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				HeritageSiteJurisdiction.objects \
					.create(heritage_site=site, country_area=country)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				HeritageSiteJurisdiction.objects \
					.filter(heritage_site_id=site.heritage_site_id, country_area_id=old_id) \
					.delete()

		return HttpResponseRedirect(site.get_absolute_url())
		# return redirect('heritagesites/site_detail', pk=site.pk)