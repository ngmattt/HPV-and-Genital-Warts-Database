from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        managed = False
        db_table = 'Country'

class Region(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Region'

class GenderOrientation(models.Model):
    label = models.CharField(max_length=255, unique=True)

    class Meta:
        managed = False
        db_table = 'GenderOrientation'

class AgeGroup(models.Model):
    group_label = models.CharField(max_length=255, unique=True)

    class Meta:
        managed = False
        db_table = 'AgeGroup'

class WartsStats(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    gender_orientation = models.ForeignKey(GenderOrientation, on_delete=models.CASCADE)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)
    sti = models.CharField(max_length=255)
    year = models.IntegerField()
    diagnoses = models.IntegerField(null=True, blank=True)
    rate_per_100k = models.FloatField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'WartsStats'