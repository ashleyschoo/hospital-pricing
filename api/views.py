from hospital_pricing.models import Hospital, HospitalPricing
from api.serializers import HospitalSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


class HospitalViewSet(viewsets.ModelViewSet):
	"""
	This ViewSet provides both 'list' and 'detail' views.
	"""
	queryset = HospitalPricing.objects.select_related('hospital').order_by('hospital.hospital_name')
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