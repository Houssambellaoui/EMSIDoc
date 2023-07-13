from django.db import models
from emsidoc_admin.models import User

class Document(models.Model):

    type_choix = [
        ('Attestation', 'Attestation'),
        ('Aval', 'Aval'),
        ('certificat de preuve d identite', 'certificat de preuve d identite'),
        ('certificat d enagement', 'certificat d enagement'),
    ]
    status_choix = [
        ('Pending', 'Pending'),
        ('Signed', 'Signed'),
        ('Rejected', 'Rejected'),
    ]
    Doc_id = models.IntegerField(primary_key=True)
    Nom = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=False, choices= type_choix)
    fichier = models.FileField(upload_to='documents/',null=True, blank=True)
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    status = models.CharField(max_length=255, null=False, choices= status_choix, default='Pending')
    date_enregistrement = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.Nom