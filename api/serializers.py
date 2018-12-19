from hospital_pricing.models import Hospital, Pricing, City, \
	State, HospitalOwnership, HospitalQualityScore, ZipCode, DRGCode
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
	city_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=City.objects.all(),
		source='city'
	)

	state = StateSerializer(
		many=False,
		read_only=True
		)
	state_id = serializers.PrimaryKeyRelatedField(
		many=False,
		write_only=True,
		queryset=State.objects.all(),
		source='state'
	)

	zip_code = ZipCodeSerializer(
		many=False,
		read_only=True
		)
	zip_code_id = serializers.PrimaryKeyRelatedField(
		many=False,
		write_only=True,
		queryset=ZipCode.objects.all(),
		source='zip_code'
	)

	hospital_ownership = HospitalOwnershipSerializer(
		many=False,
		read_only=True
		)
	# hospital_ownership_id = serializers.PrimaryKeyRelatedField(
	# 	many=False,
	# 	write_only=True,
	# 	queryset=HospitalOwnership.objects.all(),
	# )

	hospital_quality_score = HospitalQualityScoreSerializer(
		many=False,
		read_only=True
		)
	# hospital_quality_score_id = serializers.PrimaryKeyRelatedField(
	# 	many=False,
	# 	write_only=True,
	# 	queryset=HospitalQualityScore.objects.all(),
	# )

	# drg_codes = serializers.PrimaryKeyRelatedField(
	# 	many=True,
	# 	write_only=True,
	# 	queryset=Pricing.objects.all(),
	# )

	class Meta:
		model = Hospital
		fields = (
			'hospital_id',
			'hospital_provider_identifier',
			'hospital_name',
			'address',
			'city',
			'city_id',
			'state',
			'state_id',
			'zip_code',
			'zip_code_id',
			'hospital_ownership',
			# 'hospital_ownership_id',
			'hospital_quality_score',
			# 'hospital_quality_score_id',

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

		# hospital_tbl = validated_data.pop('hospital')  #many to many table here
		hospital = Hospital.objects.create(**validated_data)

		# if hospital_tbl is not None:
		# 	for hosp in hospital_tbl:
		# 		Hospital.objects.create(
		# 			hospital_id=hospital_id
		# 		)
		return hospital

	def update(self, instance, validated_data):
		hospital_id = instance.hospital_id

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
		# instance.city_id = validated_data.get(
		# 	'city_id',
		# 	instance.city_id
		# )
		# instance.state_id = validated_data.get(
		# 	'state_id',
		# 	instance.state_id
		# )
		# instance.zip_code_id = validated_data.get(
		# 	'zip_code_id',
		# 	instance.zip_code_id
		# )
		# instance.hospital_ownership_id = validated_data.get(
		# 	'hospital_ownership_id',
		# 	instance.hospital_ownership_id
		# )
		# instance.hospital_quality_score_id = validated_data.get(
		# 	'hospital_quality_score_id',
		# 	instance.hospital_quality_score_id
		# )
		instance.save()

		# If any existing country/areas are not in updated list, delete them
		# new_ids = []
		# old_ids = Hospital.objects \
		# 	.values_list('hospital_id', flat=True) \
		# 	.filter(hospital_id__exact=hospital_id)

		# # TODO Insert may not be required (Just return instance)

		# # Insert new unmatched country entries
		# for price in new_prices:
		# 	new_id = pricing.price_id
		# 	new_ids.append(new_id)
		# 	if new_id in old_ids:
		# 		continue
		# 	else:
		# 		Hospital.objects \
		# 			.create(hospital_id=hospital_id, pricing_id=new_id)

		# # Delete old unmatched country entries
		# for old_id in old_ids:
		# 	if old_id in new_ids:
		# 		continue
		# 	else:
		# 		Hospital.objects \
		# 			.filter(hospital_id=hospital_id, pricing_id=old_id) \
		# 			.delete()

		# return instance





# make like heritagesitejuristdiction serializer 
# look at serializers.listfield


# https://www.django-rest-framework.org/api-guide/serializers/#listserializer
# class PricingListSerializer(serializers.ListSerializer):
# 	def create(self, validated_data):
# 		price = [Pricing(**item) for item in validated_data]
# 		return Pricing.objects.bulk_create(price)

# class PricingSerializer(serializers.Serializer):
# 	# prices_list = PricesSerializer(
# 	# 	many=False,
# 	# 	read_only=False
# 	# 	)
# 	# prices_id = serializers.PrimaryKeyRelatedField(
# 	# 	many=True,
# 	# 	write_only=True,
# 	# 	)
# 	# prices = serializers.DictField(
# 	# 	child=serializers.CharField(allow_blank=False)
# 	# 	)

# 	class Meta:
# 		list_serializer_class = PricingListSerializer
# 		# model = Pricing
# 		# fields = (
# 		# 	prices
# 		# 	)

# 	def create():
# 		prices = validated_data.pop('prices')
# 		if prices is not None:
# 			for price in prices:
# 				Pricing.objects.create(hospital_id=price[0],drg_code=price[1],price=price[2])


class PricingSerializer(serializers.Serializer):
	hospital_id = serializers.CharField()
	drg_code = serializers.CharField()
	price = serializers.CharField()

	class Meta:
		model = Pricing
		fields = (
			'hospital_id',
			'drg_code',
			'price'
			)

	def create():
		prices = validated_data.pop('prices')
		if prices is not None:
			for price in prices:
				Pricing.objects.create(hospital_id=price[0],drg_code=price[1],price=price[2])





# look at heritagesites update queryset that gets the existing pricing.objects.create.filter by hospital_id
# open dictionary, dig out hospital_id, delete curret entries for hospital_id in pricing table and
# replace it with the new info, api is a replacement api


	def update():

		prices = validated_data.pop('prices')
		if prices is not None:
			for price in prices:
				Pricing.objects.create(hospital_id=price[0],drg_code=price[1],price=price[2])

		# If any existing country/areas are not in updated list, delete them
		new_ids = []
		old_ids = Pricing.objects \
			.values_list('pricing', flat=True) \
			.filter(pricing_id__exact=pricing)

		# TODO Insert may not be required (Just return instance)

		# Insert new unmatched country entries
		for price in new_prices:
			new_id = pricing.price_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				Pricing.objects \
					.create(pricing_id=pricing, drg_code_id=new_id)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				Pricing.objects \
					.filter(pricing_id=pricing, drg_code_id=old_id) \
					.delete()

		return instance
