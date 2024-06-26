# myapp/urls.py
from django.urls import path
from .views import home, recommendations, contact_us, stores_near_you, recommendation_page, webtoon_profile, \
    manga_recommendation_page, manga_profile,character_profile

urlpatterns = [
    path('', home, name='home'),
    path('webtoon_recommendation_page/', recommendations, name='webtoon_recommendation_page'),
    path('contact_us/', contact_us, name='contact_us'),
    path('stores_near_you/', stores_near_you, name='stores_near_you'),
    path('recommendation/', recommendation_page, name='recommendation_page'),
    path('webtoon/<str:webtoon_name>/', webtoon_profile, name='webtoon_profile'),
    path('manga_recommendation/', manga_recommendation_page, name='manga_recommendations'),
    path('manga_profile/<str:manga_title>/', manga_profile, name='manga_profile'),
    path('character_profile/<str:character_name>/', character_profile, name='character_profile'),

]
