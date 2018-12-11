# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse

class ChargeAmount(models.Model):
    charge_id = models.AutoField(primary_key=True)
    charge = models.DecimalField(unique=True, max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'charge_amount'
        ordering = ['charge_id']
        verbose_name = 'Average Amount Charged'
        verbose_name_plural = 'Average Amount Charged'



    def __str__(self):
        return self.charge


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'city'
        ordering = ['city_name']
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city_name


class Hospital(models.Model):
    hospital_id = models.AutoField(primary_key=True)
    hospital_provider_identifier = models.CharField(unique=True, max_length=6)
    hospital_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.ForeignKey('City', models.DO_NOTHING, blank=True, null=True)
    state = models.ForeignKey('State', models.DO_NOTHING, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    hospital_ownership = models.ForeignKey('HospitalOwnership', models.DO_NOTHING, blank=True, null=True)
    hospital_quality_score = models.ForeignKey('HospitalQualityScore', models.DO_NOTHING, blank=True, null=True)
    # intermediate model (hospital -> hospital_pricing -> pricing)
    pricing = models.ManyToManyField('Pricing', through='HospitalPricing')

    class Meta:
        managed = False
        db_table = 'hospital'
        ordering = ['hospital_provider_identifier']
        verbose_name = 'U.S. Hospital'
        verbose_name_plural = 'U.S. Hospitals'

    def __str__(self):
        return self.hospital_name

    def get_absolute_url(self):
        return reverse('hospital_detail', kwargs={'pk': self.pk})

    def pricing_display(self):
        return ', '.join(pricing.charge for hospital in self.hospital.all()[:25])

    pricing_display.short_description = 'Average Amount Charged'

class HospitalOwnership(models.Model):
    hospital_ownership_id = models.AutoField(primary_key=True)
    hospital_ownership_description = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'hospital_ownership'
        ordering = ['hospital_ownership_id']
        verbose_name = 'Hospital Ownership'

    def __str__(self):
        return self.hospital_ownership_description


class HospitalPricing(models.Model):
    hospital_pricing_id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey('Hospital', models.DO_NOTHING)
    price = models.ForeignKey('Pricing', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hospital_pricing'
        ordering = ['hospital','price']
        verbose_name = 'Hospital Pricing'


class HospitalQualityScore(models.Model):
    hospital_quality_score_id = models.AutoField(primary_key=True)
    hospital_quality_score = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hospital_quality_score'
        ordering = ['hospital_quality_score_id']
        verbose_name = 'Hospital Overall Quality Score'
        verbose_name_plural = 'Hospital Overall Quality Scores'

    def __str__(self):
        return self.hospital_quality_score


class Pricing(models.Model):
    price_id = models.AutoField(primary_key=True)
    pricing_provider_identifier = models.CharField(unique=True, max_length=6)
    charge = models.ForeignKey('ChargeAmount', models.DO_NOTHING, blank=True, null=True)
    drg_code = models.CharField(max_length=3, blank=True, null=True)
    drg_definition = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'pricing'
        ordering = ['pricing_provider_identifier']
        verbose_name = 'Pricing for Diagnosis Related Code: 313, Chest Pain'



class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    state = models.CharField(unique=True, max_length=3)

    class Meta:
        managed = False
        db_table = 'state'
        ordering = ['state']
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return self.state