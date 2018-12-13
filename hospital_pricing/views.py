from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.forms import ModelForm
from hospital_pricing.forms import forms
import django_filters
from django_filters.views import FilterView
from django.conf.urls import url
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django_filters.views import FilterView


from .models import Hospital
from .models import HospitalPricing
from .models import Pricing
from .forms import HospitalPricingForm
from .filters import HospitalFilterView





def index(request):
	return HttpResponse("Hello, world. Come explore United States Hospitals")

class HomePageView(generic.TemplateView):
	template_name = 'hospital_pricing/home.html'

class AboutPageView(generic.TemplateView):
	template_name = 'hospital_pricing/about.html'

class PaginatedFilterView(generic.View):
	"""
	Creates a view mixin, which separates out default 'page' keyword and returns the
	remaining querystring as a new template context variable.
	https://stackoverflow.com/questions/51389848/how-can-i-use-pagination-with-django-filter
	"""
	def get_context_data(self, **kwargs):
		context = super(PaginatedFilterView, self).get_context_data(**kwargs)
		if self.request.GET:
			querystring = self.request.GET.copy()
			if self.request.GET.get('page'):
				del querystring['page']
			context['querystring'] = querystring.urlencode()
		return context


class HospitalFilterView(PaginatedFilterView, FilterView):
	model = Hospital
	filterset_class = HospitalFilterView
	template_name = 'hospital_pricing/hospital_filter.html'
	context_object_name = 'hospitals'
	paginate_by = 30

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
			hospital = form.save(commit=False)
			hospital.save()
			for charge in form.cleaned_data['hospitals']:
				HospitalPricing.objects.create(hospital=hospital, pricing=charge)
			return redirect(hospital) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(hospital.get_absolute_url())
		return render(request, 'hospital_pricing/hospital_new.html', {'form': form})

	def get(self, request):
		form = HospitalPricingForm()
		return render(request, 'hospital_pricing/hospital_new.html', {'form': form})




@method_decorator(login_required, name='dispatch')
class HospitalUpdateView(generic.UpdateView):
	model = Hospital
	form_class = HospitalPricingForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'hospitals'
	# pk_url_kwarg = 'site_pk'
	success_message = "Hospital updated successfully"
	template_name = 'hospital_pricing/hospital_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		hospital = form.save(commit=False)
		# hospital.updated_by = self.request.user
		# hospital.date_updated = timezone.now()
		hospital.save()

		# Current pricing_id values linked to site
		old_ids = HospitalPricing.objects\
			.values_list('hospital_id', flat=True)\
			.filter(hospital_id=hospital.hospital_id)

		# New hospital list
		new_hospital = form.cleaned_data['hospital']

		# TODO can these loops be refactored?

		# New ids
		new_ids = []

		# Insert new unmatched country entries
		for hospital in new_hospital:
			new_id = hospital.hospital_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				HospitalPricing.objects \
					.create(hospital=hospital, pricing=charge)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				HospitalPricing.objects \
					.filter(hospital_id=hospital.hospital_id, pricing_id=old_id) \
					.delete()

		return HttpResponseRedirect(hospital.get_absolute_url())
		# return redirect('hospital/hospital_detail', pk=site.pk)


@method_decorator(login_required, name='dispatch')
class HospitalDeleteView(generic.DeleteView):
	model = Hospital
	success_message = "Hospital deleted successfully"
	success_url = reverse_lazy('hospital')
	context_object_name = 'hospitals'
	template_name = 'hospital_pricing/site_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete HeritageSiteJurisdiction entries
		HospitalPricing.objects \
			.filter(hospital_id=self.object.hospital_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())


