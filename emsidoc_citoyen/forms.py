from django import forms
from emsidoc_sharedmodel.models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'Nom', 
            'type', 
            'fichier'
            ]
