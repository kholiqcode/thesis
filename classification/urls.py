from django.urls import path

from classification.views import dashboard, data_latih, preprocessing

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('data-latih', data_latih, name="data_latih"),
    path('preprocessing', preprocessing, name="preprocessing"),
]