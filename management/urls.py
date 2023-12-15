from django.urls import path
from .import views, models
from .views import home, available, need, entercat, cat_edit, contact, success, cat_details, edit_vaccines,edit_adopter,all_cats,edit_surgery

urlpatterns = [
    path('', home, name='home'),
    path('available/', available, name='available_cats'),
    path('need/', need, name='cats_in_need'),
    path('entercat/', entercat, name='entercat_url'),
    path('cat_edit/', cat_edit, name='cat_edit_url'),
    path('contact/', contact, name='contact'),
    path('success/', success, name='success'),
    path('allcats/', all_cats, name='all_cats_url'),
    path('cat_details/<int:cat_id>/', cat_details, name='cat_details_url'),
    path('cat_edit/<int:cat_id>/', cat_edit, name='cat_edit_url'),
    path('cats/<int:cat_id>/edit_vaccines/', edit_vaccines, name='edit_vaccines_url'),
    path('cats/<int:cat_id>/edit_adopter/', edit_adopter, name='edit_adopter_url'),
    path('cats/<int:cat_id>/edit_surgery/', edit_surgery, name='edit_surgery_url'),
]

    
