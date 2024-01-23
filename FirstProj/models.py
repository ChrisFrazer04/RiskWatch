from django.db import models

# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=200)
    country_code = models.CharField(max_length = 4)
    pop2020 = models.IntegerField()
    pop2021 = models.IntegerField()
    pop2022 = models.IntegerField()

    def __str__(self):
        return self.country_name

class Disease(models.Model):
    disease_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.disease_name

class Baseline(models.Model):
    disease = models.OneToOneField(Disease, on_delete=models.CASCADE, primary_key=True)
    indicator_code = models.CharField(max_length = 50)
    indicator_name = models.CharField(max_length = 300)

    def __str__(self):
        return self.indicator_name

class BaselineData(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=5)
    country_name = models.CharField(max_length=50)
    incidence_2020 = models.FloatField(null=True)
    incidence_2021 = models.FloatField(null=True)
    incidence_2022 = models.FloatField(null=True)



    def __str__(self):
        return self.country_name


    def __str__(self):
        return self.disease

class Modifiers(models.Model):
    category = models.CharField(max_length=50)
    indicator_name = models.CharField(max_length=300)
    indicator_code = models.CharField(max_length=50)





