from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseServerError
import traceback

from .forms import CatForm, EditForm, VaccinationForm, AdopterForm, SurgeryForm
from .models import Cat, VaccinationRecord, AdoptionRecord, SpayNeuterRecord

# Create your views here.
def home(request):
    return render(request, 'home.html')



def available(request):
    # Fetch all cats with adoption_status 'Available Now' or 'Available Soon'
    cats = Cat.objects.filter(adoption_status__in=['Available Now', 'Available Soon'])
    available_count = cats.count()
    # Pass the cats to the template
    context = {'available_count': available_count, 'cats': cats}
    return render(request, 'available.html', context)



def need(request):
    # Retrieve cats that need surgeries (spayed_neutered = False)
    cats_in_need = Cat.objects.filter(spayed_neutered=False)
    need_count = cats_in_need.count()

    # Pass the cats to the template
    context = {'cats': cats_in_need, 'need_count':need_count}
    
    # Render the 'need.html' template with the provided context
    return render(request, 'need.html', context)



def cat_details(request, cat_id):
    # Retrieve the cat object or return 404
    cat = get_object_or_404(Cat, id=cat_id)
    # Render the template with the cat details
    return render(request, 'cat_details.html', {'cat': cat})






def success(request):
# Retrieve cats that need surgeries (spayed_neutered = False)
    cats_successful = Cat.objects.filter(adoption_status__in=['Adopted', 'Adoption Pending'])
    success_count = cats_successful.count()
    # Pass the cats to the template
    context = {'cats': cats_successful, 'success_count':success_count}
    
    return render(request, 'success.html', context)



def contact(request):
    return render(request, 'contact.html')


@login_required
def entercat(request):
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save(commit=False)
            # Do additional processing if needed before saving
            cat.save()
            
            cat_id = cat.id 

            return redirect('cat_details_url', cat_id)
    else:
        form = CatForm()

    return render(request, 'enter_cat.html', {'form': form})

@login_required
def cat_edit(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('cat_details_url', cat_id=cat_id)
    else:
        form = EditForm(instance=cat)

    return render(request, 'catedit.html', {'form': form, 'cat_id': cat_id})




@login_required
def edit_vaccines(request, cat_id):
    cat = Cat.objects.get(pk=cat_id)
    vaccination_records = VaccinationRecord.objects.filter(cat=cat)

    if request.method == 'POST':
        form = VaccinationForm(request.POST)
        if form.is_valid():
            # Create or update the VaccinationRecord tied to the cat
            vaccination_record = form.save(commit=False)
            vaccination_record.cat = cat
            vaccination_record.save()
            return redirect('cat_details_url', cat_id=cat_id)
    else:
        form = VaccinationForm()

    return render(request, 'edit_vaccines.html', {'form': form, 'cat': cat, 'vaccination_records': vaccination_records})

@login_required
def edit_adopter(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)

    # Using get_or_create to retrieve or create an AdoptionRecord
    adopter_record, created = AdoptionRecord.objects.get_or_create(cat=cat)

    if request.method == 'POST':
        form = AdopterForm(request.POST, instance=adopter_record)
        if form.is_valid():
            adopter_record = form.save(commit=False)
            adopter_record.cat = cat
            # Set the adoption_date to the current date and time
            adopter_record.adoption_date = timezone.now().date()

            adopter_record.save()
            return redirect('cat_details_url', cat_id=cat_id)
    else:
        form = AdopterForm(instance=adopter_record)

    return render(request, 'edit_adopter.html', {'form': form, 'cat': cat, 'adopter_record': adopter_record})

@login_required
def all_cats(request):
    # Fetch all cats
    cats = Cat.objects.all()
    
    return render(request, 'all_cats.html', {'cats': cats})

@login_required
def edit_surgery(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    
    try:
        surgery_record = SpayNeuterRecord.objects.get(cat=cat)
    except SpayNeuterRecord.DoesNotExist:
        surgery_record = None

    if request.method == 'POST':
        form = SurgeryForm(request.POST, instance=surgery_record)
        if form.is_valid():
            try:
                if surgery_record is None:
                    # If there is no existing record, create a new one
                    surgery_record = form.save(commit=False)
                    surgery_record.cat = cat
                    surgery_record.save()
                else:
                    # Update the existing record
                    form.save()

                # Redirect to the cat_details view for the same cat
                return redirect('cat_details_url', cat_id=cat_id)
            except Exception as e:
                print("Error:", e)
                print(traceback.format_exc())
                return HttpResponseServerError("Internal Server Error")
    else:
        form = SurgeryForm(instance=surgery_record)

    return render(request, 'edit_surgery.html', {'form': form, 'cat': cat, 'surgery_record': surgery_record})