from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views import View
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import User
from .forms import ProfileIconSelectionForm

# Create your views here.

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('mobile_number')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response




from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django import forms

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password__change_form.html'
    def form_invalid(self, form):
        # Return a JSON response with validation errors
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = {field: error.get_json_data() for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        # Return a JSON response on success
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form.save()  # Save the password change
            return JsonResponse({'success': True})
        return super().form_valid(form)


'''
class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/password__change_form.html'  # Customize as needed
    success_message = "Your password has been changed successfully."
    # Redirect URL after success (adjust as needed)

'''


@login_required
def profile(request):
    return render(request, 'registration/profile.html')




@login_required
def select_profile_icon(request):
    if request.method == 'POST':
        form = ProfileIconSelectionForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page

    else:
        form = ProfileIconSelectionForm(instance=request.user)

    return render(request, 'select_profile_icon.html', {'form': form})
