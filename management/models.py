from django.db import models
import datetime
from datetime import date
from PIL import Image 
import os
from django.core.exceptions import ValidationError

class VaccinationRecord(models.Model):
    cat = models.ForeignKey('Cat', on_delete=models.CASCADE, related_name='vaccination')
    VACCINE_CHOICES = [
        ('FVRCP', 'FVRCP'),
        ('Rabies', 'Rabies'),
        ('FeLV', 'FeLV'),
    ]
    vaccine_type = models.CharField(max_length=10, choices=VACCINE_CHOICES)
    administration_date = models.DateField()
    administering_vet = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.cat.name} - {self.vaccine_type} vaccine on {self.administration_date}"

class ImageProcessor:
    @classmethod
    def process_image(cls, image_path):
        img = Image.open(image_path)

        # Set the maximum height
        max_height = 200
        if img.height != max_height or img.width > 200:

            # Calculate the proportional width based on the maximum height
            width_percent = (max_height / float(img.size[1]))
            new_width = int((float(img.size[0]) * float(width_percent)))

            # Resize the image while maintaining aspect ratio
            img = img.resize((new_width, max_height))

            # Rotate the image based on Exif orientation
            if hasattr(img, '_getexif') and img._getexif() is not None:
                exif = img._getexif()
                orientation = exif.get(0x0112, 1)  # Defaults to 1 if orientation not found
                rotate_values = {3: 180, 6: 270, 8: 90}

                if orientation in rotate_values:
                    img = img.rotate(rotate_values[orientation], expand=True)

            img.save(image_path)

    @classmethod
    def delete_old_image(cls, old_image_path):
        # Delete the old photo file
        if old_image_path and os.path.isfile(old_image_path):
            os.remove(old_image_path)

class Cat(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    ADOPTION_STATUS_CHOICES = [
        ('Available Soon', 'Available Soon'),
        ('Available Now', 'Available Now'),
        ('Unavailable', 'Not Available'),
        ('Adoption Pending', 'Adoption Pending'),
        ('Adopted', 'Adopted')
    ]

    CAT_COLOR_CHOICES = [
        ('White', 'White'),
        ('Black', 'Black'),
        ('Gray', 'Gray'),
        ('Brown', 'Brown'),
        ('Orange', 'Orange'),
        ('Mixed', 'Mixed'),
    ]

    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    color = models.CharField(max_length=20, choices=CAT_COLOR_CHOICES)
    adoption_status = models.CharField(max_length=16, choices=ADOPTION_STATUS_CHOICES, default='Soon')
    spayed_neutered = models.BooleanField(default=False)
    intake_date = models.DateField(
        default=datetime.datetime.today().strftime('%m/%d/%Y'), 
        blank=False)
    description = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='images/', blank=True, null=True)

    
  

    def save(self, *args, **kwargs):
        # Check if the Cat instance already exists in the database
        if self.pk is not None:
            # Get the existing Cat instance from the database
            existing_cat = Cat.objects.get(pk=self.pk)

            # Check if a new photo is being uploaded
            if self.image and existing_cat.image != self.image:
                # Delete the old photo file
                ImageProcessor.delete_old_image(existing_cat.image.path)

            # Check if the adoption status has changed to 'Adoption Pending' or 'Adopted'
            if existing_cat.adoption_status != self.adoption_status and self.adoption_status in ['Adoption Pending', 'Adopted']:
                # Create an AdoptionRecord instance
                adoption_record = AdoptionRecord(
                    cat=self,
                    adoption_date=date.today(),
                    # Other fields can be left blank for user input
                )
                adoption_record.save()


        # Save the current instance
        super().save(*args, **kwargs)

        # After saving, trigger image processing
        if self.image:
            self.process_image()

    def process_image(self):
        ImageProcessor.process_image(self.image.path)

    def __str__(self):
        return f"{self.name} - ID: {self.id}"

class AdoptionRecord(models.Model):
    cat = models.ForeignKey('Cat', on_delete=models.CASCADE)
    adopter_name = models.CharField(max_length=100)
    adoption_date = models.DateField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)  # Assuming state codes like 'CA', 'NY', etc.
    postal_code = models.CharField(max_length=10)

    is_home_approved = models.BooleanField(default=False)
    adoption_fee_paid = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Set adoption_date to the current date when creating a new record
        if not self.adoption_date:
            self.adoption_date = date.today()

        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.adopter_name} adopted {self.cat.name}"

class SpayNeuterRecord(models.Model):
    cat = models.ForeignKey('Cat', on_delete=models.CASCADE)
    surgery_date = models.DateField()
    veterinarian_name = models.CharField(max_length=100)

    cost = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.cat.name} - Spayed/Neutered on {self.surgery_date}"
    
    def save(self, *args, **kwargs):
        # Set cat.spayed_neutered to True when saving the SpayNeuterRecord
        self.cat.spayed_neutered = True
        self.cat.save(update_fields=['spayed_neutered'])

        super().save(*args, **kwargs)