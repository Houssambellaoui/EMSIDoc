from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import logout


# Create your views here.



def index(request):

    search = User.objects.all()
    Prenom = None
    if 'search_name' in request.GET:
        Prenom = request.GET['search_name']
        if Prenom:
            search = search.filter(Prenom__icontains=Prenom)


    if request.method == 'POST':
        add_user = UserForm(request.POST, request.FILES)
        if add_user.is_valid():
            add_user.save()
    users = search #User.objects.all()  # Retrieve users from the database
    context = {
        'users': users,
        'form': UserForm
    }
    return render(request, 'pages/users.html', context)

def update(request, id):
    user_id = User.objects.get(id=id)
    if request.method == 'POST':
        user_save = UserForm(request.POST, request.FILES, instance=user_id)
        if user_save.is_valid():
            user_save.save()
            return redirect('/administrateur/')
    else:
        user_save = UserForm(instance=user_id)
    context = {
        'form':user_save,
    }
    return render(request, 'pages/update.html', context)

def delete(request, id):
    user_delete = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_delete.delete()
        return redirect('/administrateur/')
    return render(request, 'pages/delete.html')


def logout_view(request):
    logout(request)
    return redirect('/')
