from django.urls import path
from .import views, models
from .views import create_cat_view, success_page, home, cats_needing_surgery, view_all_cats

urlpatterns = [
    path('', home, name='home'),
    path('create/', create_cat_view, name='create_cat'),
    path('success/', success_page, name='success_page'),
    path('need/', cats_needing_surgery, name='cats_needing_surgery'),
    path('viewall/', view_all_cats, name='view_all_cats'),


]