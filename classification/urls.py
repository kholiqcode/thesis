from django.urls import path

from classification.views import akun, akun_detail, dashboard, data_latih, preprocessing, setting, term_frequency, tf_idf

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('data-latih', data_latih, name="data_latih"),
    path('preprocessing', preprocessing, name="preprocessing"),
    path('term-frequency', term_frequency, name="term_frequency"),
    path('tfidf', tf_idf, name="tf_idf"),
    path('akun', akun, name="akun"),
    path('akun/<str:username>', akun_detail, name="akun_detail"),
    path('setting', setting, name="setting"),
]