from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, UpdateView
from .models import Profile
from django.shortcuts import redirect, reverse
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class RegisterUser(View):
    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can log in now.')
            return redirect('profile:login')

        context = {
            'form': form
        }
        return render(request, 'registration/register.html', context)

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        context = {
            'form': form
        }
        return render(request, 'registration/register.html', context)


class FollowUser(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST.get('pk')
        print('pk', pk)
        view_profile = Profile.objects.get(pk=pk)

        if view_profile.user in my_profile.following.all():
            my_profile.following.remove(view_profile.user)
        else:
            my_profile.following.add(view_profile.user)
        return redirect(reverse('profile:profile-details', kwargs={'slug': view_profile.slug}))


class ProfileList(ListView):
    model = Profile
    template_name = 'user_profile/profiles_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'user_profile/profile_details.html'
    context_object_name = 'profile'

    def get_object(self, **kwargs):
        slug = self.kwargs.get('slug')
        return Profile.objects.get(slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_profile = Profile.objects.get(user=self.request.user)
        view_profile = self.get_object()
        followed = [True if view_profile.user in my_profile.following.all() else False]

        context['my_profile'] = my_profile
        context['view_profile'] = view_profile
        context['follow'] = followed
        context['following'] = my_profile.following.all().count()
        context['followers'] = Profile.objects.filter(following=my_profile.user).count()
        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'user_profile/profile_update.html'
    context_object_name = 'profile'
    form_class = ProfileUpdateForm

    def get_success_url(self):
        return reverse('profile:profile-details', kwargs={'slug': self.get_object().slug})
