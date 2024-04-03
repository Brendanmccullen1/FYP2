# myapp/urls.py
from django.urls import path
from .views import home, recommendations, contact_us, stores_near_you, recommendation_page, webtoon_profile

urlpatterns = [
    path('', home, name='home'),
    path('webtoon_recommendation_page/', recommendations, name='webtoon_recommendation_page'),
    path('contact_us/', contact_us, name='contact_us'),
    path('stores_near_you/', stores_near_you, name='stores_near_you'),
    path('recommendation/', recommendation_page, name='recommendation_page'),
    path('webtoon/<str:webtoon_name>/', webtoon_profile, name='webtoon_profile'),

]
