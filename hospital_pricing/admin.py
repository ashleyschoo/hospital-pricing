from django.contrib import admin

# Register your models here.
import hospital_pricing.models as models

# admin.site.hospital
@admin.register(models.Hospital)
class Hospital(admin.ModelAdmin):
	fieldsets = (
			(None, {
				'fields': (
				'hospital_name',
				'hospital_provider_identifier',
				'hospital_ownership',
				'hospital_quality_score'				
				)
				}),
			('Location', {
				'fields': [
					(
					'address',
					'city',
					'state'
					'zip_code')],
					})
)
# may need to add the foreign key here from the joining table
	list_display = (
		'hospital_name',
		'hospital_provider_identifier',
		'city',
		'state',
		'pricing_display'
		)

	list_filter = (
		'state',
		'hospital_quality_score',
		'hospital_ownership',
		)

# admin.site.pricing
@admin.register(models.Pricing)
class PricingAdmin(admin.ModelAdmin):
	fields = ['drg_code', 
	'charge', 'pricing_provider_identifier', 'zip_code']

	list_display = ['drg_code', 
	'charge', 'pricing_provider_identifier', 'zip_code']

	list_filter = ['drg_code', 
	'charge', 'pricing_provider_identifier', 'zip_code']

# admin.site.chargeamount
@admin.register(models.ChargeAmount)
class ChargeAmountAdmin(admin.ModelAdmin):
	fields = ['charge']
	list_display = ['charge']
	ordering = ['charge']

#  admin.site.state
@admin.register(models.State)
class State(admin.ModelAdmin):
	fields = ['state']
	list_display = ['state']
	ordering = ['state']

#  admin.site.city
@admin.register(models.City)
class City(admin.ModelAdmin):
	fields = ['city_name']
	list_display = ['city_name']
	ordering = ['city_name']

#  admin.site.zip_code
@admin.register(models.ZipCode)
class ZipCode(admin.ModelAdmin):
	fields = ['zip_code']
	list_display = ['zip_code']
	ordering = ['zip_code']

#  admin.site.city
@admin.register(models.DRGCode)
class DRGCode(admin.ModelAdmin):
	fields = ['drg_definition']
	list_display = ['drg_definition']
	ordering = ['drg_code_id']

#  admin.site.hospitalownership
@admin.register(models.HospitalOwnership)
class HospitalOwnership(admin.ModelAdmin):
	fields = ['hospital_ownership_description']
	list_display = ['hospital_ownership_description']
	ordering = ['hospital_ownership_description']

#  admin.site.hospitalqualityscore
@admin.register(models.HospitalQualityScore)
class HospitalQualityScore(admin.ModelAdmin):
	fields = ['hospital_quality_score']
	list_display = ['hospital_quality_score']
	ordering = ['hospital_quality_score']