from django.db import models
from django.utils.safestring import mark_safe
from PIL import Image 
import datetime, os

# Adopter creation, triggered when Cat.cat_status changes to 'Adopted'
class Adopter(models.Model):
    cat = models.ForeignKey('Cat', on_delete=models.CASCADE)
    adopter_name = models.CharField(max_length=50, null=True, blank=True)
    adopter_phone = models.CharField(max_length=15, null=True, blank=True)
    adopter_street_address = models.TextField(max_length=50, null=True, blank=True)
    adopter_city = models.TextField(max_length=50, null=True, blank=True)
    adopter_state = models.TextField(max_length=2, null=True, blank=True)
    adopter_zip = models.TextField(max_length=10, null=True, blank=True)
    
    def __str__(self):
        return f"{self.adopter_name} - {self.cat.cat_name}"

# Creates a class to handle processing the images uploaded to database
class ImageProcessor:
    @classmethod
    def process_image(cls, image_path):
        img = Image.open(image_path)

        # Sets the maximum height
        max_height = 200
        if img.height != max_height or img.width > 200:

            # Calculates the proportional width based on the maximum height
            width_percent = (max_height / float(img.size[1]))
            new_width = int((float(img.size[0]) * float(width_percent)))

            # Resizes the image while maintaining aspect ratio
            img = img.resize((new_width, max_height))

            # Rotates the image based on Exif orientation
            if hasattr(img, '_getexif') and img._getexif() is not None:
                exif = img._getexif()
                orientation = exif.get(0x0112, 1)  # Defaults to 1 if orientation not found
                rotate_values = {3: 180, 6: 270, 8: 90}

                if orientation in rotate_values:
                    img = img.rotate(rotate_values[orientation], expand=True)

            img.save(image_path)

# Main class for created Cat objects
class Cat(models.Model):
    cat_ID = models.AutoField(
        primary_key=True, 
        auto_created=True)
    
    cat_name = models.CharField(
        max_length=30, 
        default="Unknown", 
        blank=False)
    
    cat_sex = models.CharField(
        max_length=10, 
        choices=[('Female', 'Female'), ('Male', 'Male'), ('Unknown', 'Unknown')],
        default='Unknown', 
        blank=False)
    
    intake_date = models.DateField(
        default=datetime.datetime.today().strftime('%Y-%m-%d'), 
        blank=False)
    
    adoption_date = models.DateField(
        blank=True, 
        null=True)
    
    cat_surgery_status = models.CharField(
        max_length=25, 
        choices=[('Spayed', 'Spayed'), ('Neutered', 'Neutered'),
                 ('Unknown Surgery Status', 'Unknown Surgery Status'),
                 ('Needs Surgery', 'Needs Surgery')],
        default='Unknown Surgery Status', 
        blank=False)
    
    cat_status = models.CharField(
        max_length=30,
        choices=[('Unavailable', 'Unavailable'), 
                 ('Available Soon', 'Available Soon'),
                 ('Available Now', 'Available Now'), 
                 ('Adopted', 'Adopted'),
                 ('Unknown Adoption Status', 'Unknown Adoption Status')],
        default='Unknown Adoption Status', 
        blank=False)
    
    photo = models.ImageField(
        upload_to='pics', 
        default="None")

    # Field to store the previous status for use in Adopter creation
    previous_status = models.CharField(
        max_length=30, 
        default='', 
        blank=True)

    # save method for Cat instance
    def save(self, *args, **kwargs):
        # Check if the Cat instance already exists in the database
        if self.pk is not None:
            # Get the existing Cat instance from the database
            existing_cat = Cat.objects.get(pk=self.pk)

            # Check if a new photo is being uploaded
            if self.photo and existing_cat.photo != self.photo:
                # Delete the old photo file
                if existing_cat.photo and os.path.isfile(existing_cat.photo.path):
                    os.remove(existing_cat.photo.path)

        # Save the current instance
        super().save(*args, **kwargs)

        # After saving, trigger image processing
        self.process_image()

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.photo))

    def publish(self):
        self.save()
        ImageProcessor.process_image(self.photo.path)

    def process_image(self):
        ImageProcessor.process_image(self.photo.path)
    
    def __str__(self):
        return f"{self.cat_name} - {self.cat_ID}"