from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from user_profile.forms import ProfileEditForm
from django.contrib.auth import update_session_auth_hash

# Create your views here
@login_required
def profile_view(req : HttpRequest):
    return render(req, 'profile/profile.html')




@login_required
def profile_edit(req: HttpRequest):
    user = req.user
    if req.method == 'POST':
        profile_form = ProfileEditForm(req.POST, instance=user)
        password_form = PasswordChangeForm(user, req.POST)

        if 'update_profile' in req.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(req, "Profile updated successfully!")
            return redirect('edit')
        elif 'change_password' in req.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(req, user)  # Keep the user logged in after password change
            messages.success(req, "Password updated successfully!")
            return redirect('edit')
    else:
        profile_form = ProfileEditForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(req, 'profile/edit_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })