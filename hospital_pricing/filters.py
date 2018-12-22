import django_filters
from hospital_pricing.models import Hospital, Pricing, \
	HospitalQualityScore, HospitalOwnership, City, State, ZipCode, DRGCode


class PricingFilterView(django_filters.FilterSet):
	hospital = django_filters.ModelChoiceFilter(
		queryset=Hospital.objects.order_by('hospital_name'),
		field_name='hospital',
		label='Hospital',
	)
	# hospital_id = django_filters.CharFilter(
	# 	field_name='hospital__hospital_id',
	# 	label='Hospital ID',
	# 	lookup_expr='exact'
	# 	)
	pricing_id = django_filters.CharFilter(
		field_name='pricing_id',
		label='Pricing ID',
		lookup_expr='exact'
		)
	drg_code = django_filters.ModelChoiceFilter(
		queryset=DRGCode.objects.order_by('drg_code'),
		field_name='drg_code',
		label='DRG Code',
		)
	class Meta:
		model = Pricing
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = ['hospital','pricing_id','drg_code']


class HospitalFilterView(django_filters.FilterSet):
	hospital_name = django_filters.CharFilter(
		field_name='hospital_name',
		label='Hospital Name',
		lookup_expr='icontains'
	)

	# Add description, heritage_site_category, region, sub_region and intermediate_region filters here
	address = django_filters.CharFilter(
		field_name='address',
		label='Address',
		lookup_expr='icontains'

		)
	city = django_filters.CharFilter(
		field_name = 'city__city_name',
		label='City',
		lookup_expr='icontains'
		)

	state = django_filters.ModelChoiceFilter(
		queryset=State.objects.all().order_by("state"),
		field_name = 'state',
		label = 'State',
		)

	hospital_ownership = django_filters.ModelChoiceFilter(
		queryset=HospitalOwnership.objects.all().order_by("hospital_ownership_description"),
		field_name='hospital_ownership',
		label = 'Hospital Ownership',
		lookup_expr='exact'
		)

	hospital_quality_score = django_filters.ModelChoiceFilter(
		queryset=HospitalQualityScore.objects.all().order_by("hospital_quality_score"),
		field_name='hospital_quality_score',
		label='Hospital Quality Score',
		lookup_expr='exact'
	)

	class Meta:
		model = Hospital
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []