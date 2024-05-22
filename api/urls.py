from api.router import urlpatterns
from django.urls import path, include

# app_name = "api"

urlpatterns += [
    path('staff/', include('api.staff.urls')),
    path('auth/', include('api.auth.urls')),
]
