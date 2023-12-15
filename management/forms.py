from django import forms
from django.forms.widgets import FileInput, DateInput
from .models import Cat, VaccinationRecord, AdoptionRecord, SpayNeuterRecord

class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ['name', 'age', 'gender', 'color', 'adoption_status', 'spayed_neutered', 'intake_date', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'intake_date': forms.DateInput(attrs={'type': 'date'}),
        }
        spayed_neutered = forms.BooleanField(
            label='Spayed/Neutered',
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
        )

class EditForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ['name', 'age', 'gender', 'color', 'adoption_status',
                  'spayed_neutered', 'intake_date', 'description', 'image',
                  ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'intake_date': forms.DateInput(attrs={'type': 'date'}),
        }
        spayed_neutered = forms.BooleanField(
            label='Spayed/Neutered',
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
        )
        is_adopted = forms.BooleanField(
            label='Adopted',
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
        )

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = FileInput()

class VaccinationForm(forms.ModelForm):
    class Meta:
        model = VaccinationRecord
        fields = ['vaccine_type', 'administration_date', 'administering_vet']
        widgets = {
            'administration_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AdopterForm(forms.ModelForm):
    class Meta:
        model = AdoptionRecord
        fields = ['adopter_name', 'adoption_date', 'contact_email', 'contact_phone',
                  'street_address', 'city', 'state', 'postal_code',
                  'is_home_approved', 'adoption_fee_paid']
    
        widgets = {
            'adoption_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SurgeryForm(forms.ModelForm):
    class Meta:
        model = SpayNeuterRecord
        fields = ['surgery_date','veterinarian_name', 'cost']
    
        widgets = {
            'surgery_date': forms.DateInput(attrs={'type': 'date'}),
        }