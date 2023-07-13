from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'id' : forms.NumberInput(attrs={'class':'form-control'}),
            'Nom' : forms.TextInput(attrs={'class':'form-control'}),
            'Prenom' : forms.TextInput(attrs={'class':'form-control'}),
            'login' : forms.TextInput(attrs={'class':'form-control'}),
            'mot_de_passe' : forms.PasswordInput(attrs={'class':'form-control'}),
            'photo' : forms.FileInput(attrs={'class':'form-control'}),
            'signature' : forms.FileInput(attrs={'class':'form-control'}),
            'type' : forms.Select(attrs={'class':'form-control'}),
            'cin' : forms.TextInput(attrs={'class':'form-control'}),

        }
