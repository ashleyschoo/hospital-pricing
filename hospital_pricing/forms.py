from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from hospital_pricing.models import Hospital, Pricing, DRGCode


class HospitalPricingForm(forms.ModelForm):
	class Meta:
		model = Hospital
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'submit'))


class PricingForm(forms.ModelForm):
	class Meta:
		model = Pricing
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'submit'))