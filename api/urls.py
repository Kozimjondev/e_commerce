from api.router import urlpatterns
from django.urls import path, include

# app_name = "api"

urlpatterns += [
    path('staff/', include('api.staff.urls')),
    path('auth/', include('api.auth.urls')),
]


"""    data = {
            "receipt_product":
                [
                    {
                        "warehouse": 1,
                        "product": 1,
                        "uom": 1,
                        "quantity": 2,
                        "unitPrice": 1000,
                    },
                    {
                        "warehouse": 1,
                        "product": 2,
                        "uom": 1,
                        "quantity": 4,
                        "unitPrice": 1000,
                    },
                    {
                        "warehouse": 1,
                        "product": 3,
                        "uom": 1,
                        "quantity": 5,
                        "unitPrice": 1000,
                    }
                ]
        }
"""
