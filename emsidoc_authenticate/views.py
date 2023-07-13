from django.shortcuts import render, redirect
from emsidoc_admin.views import * 
from emsidoc_fonctionnaire.views import * 
from emsidoc_citoyen.views import * 
from emsidoc_admin.models import *


from django.contrib import messages


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(login=username, mot_de_passe=password)
            # Authentication successful
            # Set user details in session or any other authentication mechanism
            if user:
                request.session['USER'] = {
                    'id': user.id, 'login': user.login, 'pwd': user.mot_de_passe, 'nom': user.Nom, 'prenom': user.Prenom, 'type': user.type, 'signature': user.signature.path, 'img_user': user.photo.path }
            # Redirect to a success page
            return redirect('dashboard')
        except User.DoesNotExist:
            # Authentication failed
            messages.error(request, 'Invalid login credentials')

    return render(request, 'pages/login.html')


def dashboard(request):
    if 'USER' in request.session:
        user = request.session['USER']
        user_type = user['type']
        
        if user_type == 'Admin':
            return redirect('index')  # Redirect to the admin dashboard
        elif user_type == 'citoyen':
            return redirect('indexC')  # Redirect to the customer dashboard
        elif user_type == 'Fonctionnaire':
            return redirect('index2')  # Redirect to the fonctionnaire dashboard
        else:
            return redirect('default_dashboard')  # Redirect to a default dashboard if no specific type is found
    else:
        return redirect('login')  # Redirect to the login page if the user is not authenticated