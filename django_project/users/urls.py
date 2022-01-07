from django.urls import path
from . import views
urlpatterns=[
path('tc',views.register,name="user-register")
]
