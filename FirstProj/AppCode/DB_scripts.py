from django.db import models
from FirstProj import models as mod
import WHO_API as who

k = mod.Country(country_name='United States', country_code='USA', population=305861306)
k.save()
print(mod.Country.objects.all())

class insert():
    def insert_country(self):
        name = ''
        code = ''
        pop = ''
        it = mod.Country(country_name=name, country_code=code, population=pop)