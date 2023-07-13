from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
def validate_pdf(value):
    ext = value.name.split('.')[-1]
    if ext.lower() != 'pdf':
        raise ValidationError('Only PDF files are allowed.')
class User(models.Model):
    type_choix2 = [
        ('Admin', 'Admin'),
        ('Fonctionnaire', 'Fonctionnaire'),
        ('citoyen', 'citoyen'),
    ]
    id = models.IntegerField(primary_key=True)
    Nom = models.CharField(max_length=255)
    Prenom = models.CharField(max_length=255)
    login = models.CharField(max_length=255, null=False)
    mot_de_passe = models.CharField(max_length=255, null=False)
    photo = models.ImageField(null=False)
    signature = models.FileField(upload_to='signatures/')
    type = models.CharField(max_length=255, null=False, choices = type_choix2)
    cin = models.CharField(max_length=255)

    def __str__(self):
        return self.cin