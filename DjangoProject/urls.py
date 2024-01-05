from django.contrib import admin
from django.urls import path
from FirstProj.views import index
from django.urls import include
from FirstProj import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('FirstProj/', include('FirstProj.urls')),
    path('<str:id>', views.index, name='stringpage'),
    path('', views.home, name='homepage'),
    path("__debug__/", include("debug_toolbar.urls")),

]


