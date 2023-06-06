from django.shortcuts import render, redirect
from django.http import HttpResponse
from bigbrother.forms import UserForm
from bigbrother.models import CustomUser, Connection
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

import subprocess

def index(request):
    # The index view
    return render(request, 'bigbrother/index.html')

def user_detail(request, user_id):
    # The user detail view
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return HttpResponse("User does not exist")
    return render(request, 'bigbrother/user_detail.html', {'user': user})

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Create a Connection for the new user
                Connection.objects.create(user=user, active=False)
                login(request, user)
                return redirect('user_page')
    else:
        form = UserForm()
    return render(request, 'bigbrother/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_page')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'bigbrother/login.html', {'form': form})

def get_vpn_status(user_id):
    # Run the wg show command
    result = subprocess.run(["wg", "show"], capture_output=True, text=True)

    # Parse the output
    lines = result.stdout.split("\n")
    for line in lines:
        if "peer:" in line:
            # Assuming that the user_id is used as the peer name in WireGuard
            if str(user_id) in line:
                return "Connected"

    return "Not connected"

@login_required
def user_page(request):
    print(f"request.user is {request.user} and its type is {type(request.user)}")
    # Get the User instance based on the username
    user = User.objects.get(username=request.user.username)
    # Find the Connection object associated with the current user
    connection = Connection.objects.get(user=user)
    # Get the user's VPN status.
    vpn_status = get_vpn_status(connection.user.id)
    return render(request, 'bigbrother/user_page.html', {'user': user, 'vpn_status': vpn_status})

@login_required
def toggle_vpn(request):
    print(f"request.user is {request.user} and its type is {type(request.user)}")
    # Get the User instance based on the username
    user = User.objects.get(username=request.user.username)
    # Find the Connection object associated with the current user
    connection = Connection.objects.get(user=user)
    # Toggle the active field
    connection.active = not connection.active
    connection.save()
    return redirect('user_page')



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
