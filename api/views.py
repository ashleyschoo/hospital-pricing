from hospital_pricing.models import Hospital, Pricing, DRGCode
from api.serializers import HospitalSerializer, PricingSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


class PricingViewSet(viewsets.ModelViewSet):
	"""
	This ViewSet provides both 'list' and 'detail' views.
	"""
	queryset = Pricing.objects.select_related('hospital','drg_code').order_by('pricing_id')
	serializer_class = PricingSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def delete(self, request, pk, format=None):
		site = self.get_object(pk)
		self.perform_destroy(self, site)

		return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance):
		instance.delete()


class HospitalViewSet(viewsets.ModelViewSet):
	"""
	This ViewSet provides both 'list' and 'detail' views.
	"""
	queryset = Hospital.objects.select_related('city','state','zip_code','hospital_quality_score','hospital_ownership').order_by('hospital.hospital_id')
	serializer_class = HospitalSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def delete(self, request, pk, format=None):
		site = self.get_object(pk)
		self.perform_destroy(self, site)

		return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance):
		instance.delete()




'''
class SiteListAPIView(generics.ListCreateAPIView):
	queryset = HeritageSite.objects.select_related('heritage_site_category').order_by('site_name')
	serializer_class = HeritageSiteSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
'''

'''
class SiteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	queryset = HeritageSite.objects.select_related('heritage_site_category').order_by('site_name')
	serializer_class = HeritageSiteSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
'''