from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import redirect, reverse, HttpResponse
from .models import Profile
from .forms import UserRegisterForm, ProfileUpdateForm, EmailForm


class ContactForm(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = EmailForm(request.POST)
        if form.is_valid():
            form.user = request.user.username
            subject = form.cleaned_data['user'] + '-' + form.cleaned_data['subject']
            message = 'Email: ' + form.cleaned_data['email'] + '\n' + form.cleaned_data['message']
            try:
                send_mail(subject=subject, message=message, from_email=form.cleaned_data['email'], recipient_list=['test@test.xx', ])
                messages.success(request, 'Email has been sent succesfully!')
            except BadHeaderError:
                return HttpResponse('BadHeaderError!')
            return redirect('post:home')

        context = {
            'form': form
        }
        return render(request, 'user_profile/contact.html', context)

    def get(self, request, **kwargs):
        form = EmailForm()
        context = {
            'form': form
        }
        return render(request, 'user_profile/contact.html', context)


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
        profile = get_object_or_404(Profile, slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_profile = Profile.objects.get(user=self.request.user)
        view_profile = self.get_object()
        followed = [True if view_profile.user in my_profile.following.all() else False]

        if my_profile == view_profile:
            posts = view_profile.posts.all()
        elif my_profile in view_profile.user.following.all():
            posts = view_profile.posts.all()
        else:
            posts = view_profile.posts.exclude(followers_only=True)

        context['posts'] = posts
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
