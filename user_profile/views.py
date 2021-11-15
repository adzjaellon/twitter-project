from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import redirect, reverse, HttpResponse
from .models import Profile
from .forms import UserRegisterForm, ProfileUpdateForm, EmailForm, UserUpdateForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes, DjangoUnicodeDecodeError
from .utils import activation_token
from django.contrib.sites.shortcuts import get_current_site
from decouple import config


class ContactForm(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = EmailForm(initial={'user': request.user.username}, data=request.POST)

        if form.is_valid():
            form.user = request.user.username
            subject = form.cleaned_data['user'] + '-' + form.cleaned_data['subject']
            message = 'Email: ' + form.cleaned_data['email'] + '\n' + form.cleaned_data['message'] + '\nFrom user: ' + form.cleaned_data['user']
            try:
                send_mail(subject=subject, message=message, from_email=form.cleaned_data['email'], recipient_list=['gexalif660@ecofreon.com', ])
                messages.success(request, 'Email has been sent succesfully!')
            except BadHeaderError:
                return HttpResponse('BadHeaderError!')
            return redirect('post:home')

        context = {
            'form': form
        }
        return render(request, 'user_profile/contact.html', context)

    def get(self, request, **kwargs):
        form = EmailForm(initial={'user': request.user.username})
        context = {
            'form': form
        }
        return render(request, 'user_profile/contact.html', context)


class RegisterUser(View):
    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            uidb = urlsafe_base64_encode(force_bytes(user.pk))
            token = activation_token.make_token(user)
            site = get_current_site(request).domain

            link = reverse('profile:activate', kwargs={'uidb64': uidb, 'token': token})
            activate_link = 'http://' + site + link
            subject = f'[{site}] Activate your account!'
            message = f'Yo {user.username}, use this link to activate your account: {activate_link}'

            send_mail(subject=subject, message=message, from_email=config('EMAIL'), recipient_list=[user.email])
            messages.success(request, 'Email with confirmation link has been sended!')
            return redirect('profile:login')

        context = {
            'form': form
        }
        return render(request, 'user_profile/registration/register.html', context)

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        context = {
            'form': form
        }
        return render(request, 'user_profile/registration/register.html', context)


class ActivateUser(View):
    def get(self, request, uidb64, token):
        try:
            pk = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=pk)

            if activation_token.check_token(user, token):
                if not user.is_active:
                    user.is_active = True
                    user.save()
                messages.success(request, 'Account has been activated')
        except Exception:
            pass

        return redirect('profile:login')


class FollowUser(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST.get('pk')
        view_profile = Profile.objects.get(pk=pk)

        if view_profile.user in my_profile.following.all():
            my_profile.following.remove(view_profile.user)
        else:
            my_profile.following.add(view_profile.user)
        return redirect(reverse('profile:profile-details', kwargs={'slug': view_profile.slug}))


class ProfileSearch(View):
    def get(self, request, **kwargs):
        profile = request.GET.get('profile')
        if profile:
            queryset = Profile.objects.filter(user__username__icontains=profile)
        else:
            queryset = []

        context = {
            'queryset': queryset
        }
        return render(request, 'user_profile/profile_list.html', context)


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
        context['following'] = view_profile.following.all().count()
        context['followers'] = Profile.objects.filter(following=view_profile.user).count()
        context['likes'] = view_profile.get_latest_likes
        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'user_profile/profile_update.html'
    context_object_name = 'profile'
    form_class = ProfileUpdateForm

    def get_success_url(self):
        return reverse('profile:profile-details', kwargs={'slug': self.get_object().slug})


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user_profile/user_update.html'
    context_object_name = 'user'
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse('profile:profile-details', kwargs={'slug': self.get_object().profile.slug})
