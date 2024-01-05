from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('distance', views.Distance_calc.as_view(), name='distance_calc'),
    path('riskcalculator', views.Risk_Calculator.as_view(), name='RiskCalculator'),
    path('test', views.Test.as_view(), name='testing'),
]