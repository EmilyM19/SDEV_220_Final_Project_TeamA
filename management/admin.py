from django.contrib import admin
from django.utils.html import format_html
from .models import VaccinationRecord, Cat, AdoptionRecord, SpayNeuterRecord
from django.forms import TextInput, Textarea, DateInput, DateTimeInput, Select
from django.db import models



class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ('cat', 'vaccine_type', 'administration_date', 'administering_vet')
    search_fields = ['cat__name', 'vaccine_type']
    list_editable =('administration_date', 'administering_vet')
admin.site.register(VaccinationRecord, VaccinationRecordAdmin)

class AdoptionRecordInline(admin.TabularInline):
    model = AdoptionRecord
    extra = 0

class VaccinationRecordInline(admin.TabularInline):
    model = VaccinationRecord
    extra = 0

class CatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'color', 'adoption_status', 'spayed_neutered', 'intake_date', 'display_image_thumbnail', 'image')
    list_filter = ['adoption_status', 'spayed_neutered']
    search_fields = ['id', 'name']
    list_editable = ('name', 'adoption_status', 'spayed_neutered', 'intake_date', 'image')

    fieldsets = [
        ('Cat Information', {
            'fields': ['name', 'age', 'gender', 'color', 'adoption_status', 'spayed_neutered', 'intake_date'],
        }),
        ('Description', {
            'fields': ['description'],
            'classes': ['collapse'],  # Collapsible fieldset
        }),
        ('Image', {
            'fields': ['image'],
            'classes': ['collapse'],
        }),
    ]

    def display_image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return 'No Image'

    display_image_thumbnail.short_description = 'Thumbnail'

    inlines = [AdoptionRecordInline, VaccinationRecordInline]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':40})},
        models.DateField: {'widget': DateInput(attrs={'size': '8'})},  # Adjust 'size' as needed
    }

admin.site.register(Cat, CatAdmin)

class AdoptionRecordAdmin(admin.ModelAdmin):
    list_display = ('cat', 'adoption_date','adopter_name', 'contact_email','contact_phone')
    search_fields = ['cat__name', 'cat__id', 'adopter_name']
    list_editable = ('adopter_name', 'adoption_date', 'contact_email','contact_phone')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':40})},
    }

admin.site.register(AdoptionRecord, AdoptionRecordAdmin)

class SpayNeuterRecordAdmin(admin.ModelAdmin):
    list_display = ('cat', 'surgery_date', 'veterinarian_name')
    search_fields = ['cat__name', 'surgery_date', 'veterinarian_name']
    list_editable =('surgery_date', 'veterinarian_name')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':40})},
    }
admin.site.register(SpayNeuterRecord, SpayNeuterRecordAdmin)