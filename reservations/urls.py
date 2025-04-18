from django.urls import path
from . import views


urlpatterns = [
    path('gallery/', views.gallery,name='gallery'),
    path('review/<str:pk>/', views.create_review,name='review'),
    path('gallery/<str:pk>/', views.res_profile,name='res_profile'),
    path('comments_of_realestate/<str:pk>/', views.comments_of_realestate,name='comments_of_realestate'),
    path('new_realestate/', views.new_realestate,name='new_realestate'),
    path('favourit/', views.favourit_view,name='favourit'),
    path('profile/', views.profile,name='profile'),
    path('reservation/<int:realestate_id>/', views.create_reservation_period, name='create-reservation'),
    path('DaysOff/<int:realestate_id>/', views.create_DaysOff_period, name='create-DaysOff'),
    path('toggle-favorite/<int:realestate_id>/', views.toggle_favorite, name='toggle-favorite'),
    path('property_bookings/<int:realestate_id>/', views.property_bookings, name='property-bookings'),
    path('get_accepted_reservations/<int:realestate_id>/', views.get_accepted_reservations, name='get_accepted_reservations'),
]