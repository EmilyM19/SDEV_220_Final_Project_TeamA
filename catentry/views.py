from django.shortcuts import render
from .models import Cat
from .forms import CatForm

# Homepage view: Displays cats with 'Available', 'Available Soon' status
def home(request):
    # Get all cats excluding those with certain statuses
    cats = Cat.objects.exclude(
        cat_status__in=['Adopted', 
                        'Unavailable', 
                        'Unknown Adoption Status'])

    # Get the count of available cats
    available_cats_count = Cat.objects.filter(cat_status='Available Now').count()

    return render(request, 'home.html', {'cats': cats, 'available_cats_count': available_cats_count})

# View to create a new cat
def create_cat_view(request):
    success_message = None
    form = CatForm()

    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            success_message = 'Successfully saved!'  # Set the success message
            form = CatForm()
    else:
        form = CatForm()

    return render(request, 'create_cat.html', {'form': form, 'success_message': success_message})

# Success page view: Displays adopted cats
def success_page(request):
    adopted_cats = Cat.objects.filter(cat_status='Adopted')
    adopted_cats_count = adopted_cats.count()

    return render(request, 'success.html', {'adopted_cats': adopted_cats, 'adopted_cats_count': adopted_cats_count})

# View for available cats
def available_cats(request):
    available_cats = Cat.objects.filter(cat_status='Available Now')
    context = {'available_cats': available_cats, 'available_cats_count': available_cats.count()}

    return render(request, 'home.html', context)

# View for cats needing surgery
def cats_needing_surgery(request):
    # Retrieve the cats needing surgery from the database
    cats_needing_surgery = Cat.objects.filter(cat_surgery_status='Needs Surgery')

    # Count the number of cats needing surgery
    need_count = cats_needing_surgery.count()

    # Render the 'needs_surgery.html' template with the context
    return render(request, 'needs_surgery.html', {'cats': cats_needing_surgery, 'need_count': need_count})

# View to display all cats
def view_all_cats(request):
    allcats = Cat.objects.all()
    all_count = allcats.count()

    return render(request, 'view_all_cats.html', {'allcats': allcats, 'all_count': all_count})