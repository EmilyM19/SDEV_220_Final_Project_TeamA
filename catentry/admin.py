from django.utils.html import format_html
from django.contrib import admin
from catentry.models import Cat, Adopter
from django.forms import TextInput, Textarea, DateInput, DateTimeInput, Select
from django.db import models

# Customizing the admin interface for the Cat model
class CatAdmin(admin.ModelAdmin):

    # Define the columns to be displayed in the list view
    list_display = (
        "cat_ID",
        "cat_name",
        "intake_date",
        "adoption_date",
        "cat_status",
        "cat_surgery_status",
        "display_photo_thumbnail",  # Custom method for displaying thumbnail in the list
        "photo",
    )

    # Define columns that can be edited directly in the list view
    list_editable = ('cat_status', 'cat_surgery_status', 'adoption_date', "photo")
    
    # Add filters for specific columns in the list view
    list_filter = ('cat_status', 'cat_surgery_status')

    # Make the 'display_photo' field read-only in the detail view
    readonly_fields = ("display_photo",)

    # Custom method to display a thumbnail in the detail view
    def display_photo_thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
        return "-"
    display_photo_thumbnail.short_description = "Photo Thumbnail"

    # Custom method to display a larger photo in the detail view
    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" height="100" />', obj.photo.url)
        return "-"
    display_photo.short_description = "Photo"

    # Customize the layout of the detail view using fieldsets
    fieldsets = (
        ("Basic Information", {
            'fields': (
                "cat_ID",
                "cat_name",
                "intake_date",
                "adoption_date",
            ),
        }),
        ("Status Information", {
            'fields': (
                "cat_status",
                "cat_surgery_status",
            ),
        }),
        ("Photo", {
            'fields': (
                "display_photo",
            ),
        }),
    )

    # Override formfield widgets for specific model fields
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'10'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':40})},
        models.DateField: {'widget': DateInput(attrs={'size': '8'})},  # Adjust 'size' as needed
        models.DateTimeField: {'widget': DateInput(attrs={'size': '12'})},  # Adjust 'size' as needed
        models.CharField: {'widget': Select(attrs={'style': 'width: 4em;'})},  # Adjust 'width' as needed
    }

# Customizing the admin interface for the Adopter model
class AdopterAdmin(admin.ModelAdmin):
    # Define the columns to be displayed in the list view
    list_display = (
        "cat",
        "id",
        "adopter_name",
        "adopter_phone",
        "adopter_street_address",
        "adopter_city",
        "adopter_state",
        "adopter_zip",
    )
    # Add filters for specific columns in the list view
    list_filter = ("adopter_name",)
    # Define columns that can be edited directly in the list view
    list_editable = (
        'adopter_name',
        'adopter_phone',
        'adopter_street_address',
        "adopter_city",
        "adopter_state",
        "adopter_zip"
    )
    
    # Override formfield widgets for specific model fields
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':40})},
    }

# Register the Cat and Adopter models with their respective custom admin interfaces
admin.site.register(Cat, CatAdmin)
admin.site.register(Adopter, AdopterAdmin)