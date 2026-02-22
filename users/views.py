from django.shortcuts import render, redirect, HttpResponse
from users.forms import CustomRegistrationForm, LoginForm, AssignRoleForm, CreateGroupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
# Sign-up with email-confirmation 
def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')
						
        else:
            print("Form is not valid")
    return render(request, 'register/sign_up.html', {"form": form})

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')

# Sign-up without email-confirmation 
# def sign_up(request):
#     form = CustomRegistrationForm()
#     if request.method == 'POST':
#         form = CustomRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data.get('password1'))
#             user.is_active = True
#             user.save()

#             # Assign default role
#             participate_group = Group.objects.get(name='Participate')
#             user.groups.add(participate_group)

#             messages.success(request, 'Account created successfully.')
#             return redirect('sign-in') 
#         else:
#             print("Form is not valid")

#     return render(request, 'register/sign_up.html', {"form": form})


def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'register/sign_in.html', {'form': form})

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    

@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect('user-list')
    return render(request, 'admin/assign_role.html', {"form": form})

@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('create-group')

    return render(request, 'admin/create_group.html', {'form': form})

@login_required
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html',{'groups':groups})

@login_required
def user_list(request):
    query = request.GET.get('q', '')

    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    )

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No group Assigned'

    return render(request, 'admin/user_list.html', {
        'users': users,
        'query': query
    })

@login_required
def user_details(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, "admin/user_details.html", {"user": user})

@user_passes_test(is_admin, login_url='no-permission')
def delete_user(request, id):
    participate = get_object_or_404(User, id=id)
    
    if request.method == "POST":
        participate.delete()
        messages.success(request,"Participate has been Removed")
        return redirect("user-list")  
    else:
        messages.error(request,"Something went wrong")
        return redirect("user-list")

@login_required
def participant_rsvp_dashboard(request):
    rsvp_events = request.user.events.all() 

    return render(request, "admin/rsvp.html", {
        "rsvp_events": rsvp_events
    })
