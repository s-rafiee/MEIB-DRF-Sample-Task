from django.urls import path
from . import views

app_name = 'companies'
urlpatterns = [
    path('companies/', views.CompanyView.as_view(), name='companies_view'),
    path('statements/', views.StatementView.as_view({'get': 'list'}), name='statements_view'),
]
