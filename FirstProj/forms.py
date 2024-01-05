from django import forms

disease_choices = [('Malaria', 'Select a disease'), ('Rubella', 'Rubella'), ('Syphilis', 'Syphilis'), ('Tuberculosis', 'Tuberculosis'), ('Diphtheria', 'Diphtheria'), ('Malaria', 'Malaria'), ('HIV', 'HIV'), ('Japanese encephalitis', 'Japanese encephalitis'), ('Leprosy', 'Leprosy'), ('Measles', 'Measles'), ('Mumps', 'Mumps'), ('Cutaneous leishmaniasis', 'Cutaneous leishmaniasis'), ('Visceral leishmaniasis', 'Visceral leishmaniasis'), ('Buruli ulcer', 'Buruli ulcer'), ('T.b. gambiense', 'T.b. gambiense'), ('T.b. rhodesiense', 'T.b. rhodesiense'), ('Pertussis', 'Pertussis'), ('Yellow Fever', 'Yellow Fever') ]
class DistanceInput(forms.Form):
    location1 = forms.CharField(max_length=200)
    location2 = forms.CharField(max_length=200)

class RiskCalculator(forms.Form):
    dropdown = forms.ChoiceField(choices=disease_choices, label='Diseases', required=True)
    location = forms.CharField(max_length=500)

class Testing(forms.Form):
    input1 = forms.IntegerField()
    input2 = forms.IntegerField()
