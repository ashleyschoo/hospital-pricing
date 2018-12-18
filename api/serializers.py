from hospital_pricing.models import Hospital, Pricing, HospitalPricing, City, \
	State, ChargeAmount, HospitalOwnership, HospitalQualityScore, ZipCode, DRGCode
from rest_framework import response, serializers, status


class StateSerializer(serializers.ModelSerializer):

	class Meta:
		model = State
		fields = ('state_id', 'state')


class DRGCodeSerializer(serializers.ModelSerializer):

	class Meta:
		model = DRGCode
		fields = ('drg_code_id', 'drg_definition')


class CitySerializer(serializers.ModelSerializer):

	class Meta:
		model = City
		fields = ('city_id', 'city_name')


class ZipCodeSerializer(serializers.ModelSerializer):

	class Meta:
		model = ZipCode
		fields = ('zip_code_id', 'zip_code')

class HospitalOwnershipSerializer(serializers.ModelSerializer):

	class Meta:
		model = HospitalOwnership
		fields = ('hospital_ownership_id', 'hospital_ownership_description')

class HospitalQualityScoreSerializer(serializers.ModelSerializer):

	class Meta:
		model = HospitalQualityScore
		fields = ('hospital_quality_score_id', 'hospital_quality_score')



class ChargeAmountSerializer(serializers.ModelSerializer):

	class Meta:
		model = ChargeAmount
		fields = ('charge_id', 'charge')


class PricingSerializer(serializers.ModelSerializer):
	charge = ChargeAmountSerializer(many=False, read_only=True)
	drg_code = DRGCodeSerializer(many=False, read_only=True)
	zip_code = ZipCodeSerializer(many=False, read_only=True)

	class Meta:
		model = Pricing
		fields = (
			'price_id',
			'pricing_provider_identifier',
			'charge',
			'drg_code',
			'zip_code')





class HospitalPricingSerializer(serializers.ModelSerializer):
	hospital = serializers.ReadOnlyField(source='hospital.hospital_id')
	price = serializers.ReadOnlyField(source='pricing.price_id')

	class Meta:
		model = HospitalPricing
		fields = ('hospital_pricing_id', 'hospital', 'price')


class HospitalSerializer(serializers.ModelSerializer):
	hospital_name = serializers.CharField(
		allow_blank=False,
		max_length=255
	)
	hospital_provider_identifier = serializers.CharField(
		allow_blank=False
	)
	address = serializers.CharField(
		allow_blank=True
	)
	city = CitySerializer(
		many=False,
		read_only=True
	)
	city_ids = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=City.objects.all(),
		source='city'
	)


	state_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=State.objects.all(),
		source='state'
	)

	zip_code_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=ZipCode.objects.all(),
		source='zip_code'
	)

	hospital_ownership_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=HospitalOwnership.objects.all(),
		source='hospital_ownership'
	)

	hospital_quality_score_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=HospitalQualityScore.objects.all(),
		source='hospital_quality_score'
	)

	class Meta:
		model = Hospital
		fields = (
			'hospital_id',
			'hospital_provider_identifier',
			'hospital_name',
			'address',
			'city',
			'city_ids',
			'state',
			'state_ids',
			'zip_code',
			'zip_code_ids',
			'hospital_ownership',
			'hospital_ownership_ids',
			'hospital_quality_score',
			'hospital_quality_score_ids',
		)

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""

		# print(validated_data)

		hospital_pricing_tbl = validated_data.pop('hospital_pricing')  #many to many table here
		hospital = Hospital.objects.create(**validated_data)

		if hospital_pricing_tbl is not None:
			for hosp in hospital_pricing_tbl:
				HospitalPricing.objects.create(
					hospital_id=hospital.hospital_id,
					price_id=pricing.price_id
				)
		return hospital

	def update(self, instance, validated_data):
		hospital_id = instance.hospital_id
		new_hospitals = validated_data.pop('hospital_pricing') #many to many table

		instance.hospital_name = validated_data.get(
			'hospital_name',
			instance.hospital_name
		)
		instance.hospital_provider_identifier = validated_data.get(
			'hospital_provider_identifier',
			instance.hospital_provider_identifier
		)
		instance.address = validated_data.get(
			'address',
			instance.address
		)
		instance.city_id = validated_data.get(
			'city_id',
			instance.city_id
		)
		instance.state_id = validated_data.get(
			'state_id',
			instance.state_id
		)
		instance.zip_code_id = validated_data.get(
			'zip_code_id',
			instance.zip_code_id
		)
		instance.hospital_ownership_id = validated_data.get(
			'hospital_ownership_id',
			instance.hospital_ownership_id
		)
		instance.hospital_quality_score_id = validated_data.get(
			'hospital_quality_score_id',
			instance.hospital_quality_score_id
		)
		instance.save()

		# If any existing country/areas are not in updated list, delete them
		new_ids = []
		old_ids = HospitalPricing.objects \
			.values_list('hospital_id', flat=True) \
			.filter(hospital_id__exact=hospital_id)

		# TODO Insert may not be required (Just return instance)

		# Insert new unmatched country entries
		for price in new_prices:
			new_id = pricing.price_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				HospitalPricing.objects \
					.create(hospital_id=hospital_id, pricing_id=new_id)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				HospitalPricing.objects \
					.filter(hospital_id=hospital_id, pricing_id=old_id) \
					.delete()

		return instance