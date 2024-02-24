# myapp/urls.py
from django.urls import path
from .views import home, recommendations, contact_us, stores_near_you, recommendation_page

urlpatterns = [
    path('', home, name='home'),
    path('recommendations/', recommendations, name='recommendations'),
    path('contact_us/', contact_us, name='contact_us'),
    path('stores_near_you/', stores_near_you, name='stores_near_you'),
    path('recommendation/', recommendation_page, name='recommendation_page'),
]
