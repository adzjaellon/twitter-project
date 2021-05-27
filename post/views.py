from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post, Comment
from django.views.generic.edit import FormMixin
from .forms import CommentCreateForm, PostCreateForm
from django.db.models import Count, Q
from taggit.models import Tag
from user_profile.models import Profile
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from django.utils.text import slugify


def search(request):
    q = request.GET.get('q')
    if q:
        queryset = Post.objects.all().filter(Q(body__icontains=q) | Q(tags__name__icontains=q)).distinct()

    context = {
        'posts': queryset,
        'latest_posts': Post.objects.order_by('-created')[:3],
        'common_tags': Post.tags.values('name').annotate(count=Count('name')).order_by('-count')
    }
    return render(request, 'blog.html', context)


class PostList(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog.html'

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        users = [user for user in profile.following.all()]
        posts = []
        if profile.user not in users:
            posts.append(profile.post_set.all())

        for user in users:
            prof = Profile.objects.get(user=user)
            posts.append(prof.post_set.all())

        queryset = None
        if len(posts):
            queryset = sorted(chain(*posts), reverse=True, key=lambda obj: obj.created)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.order_by('-created')[:3]
        context['common_tags'] = Post.tags.values('name').annotate(count=Count('name')).order_by('-count')
        return context


class PostTagList(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'tag_posts'
    template_name = 'post/post_tag_list.html'
    paginate_by = 4

    def get_queryset(self):
        name = self.request.resolver_match.kwargs.get('name')
        tag = get_object_or_404(Tag, name=name)
        return Post.objects.filter(tags__name__in=[tag.name])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.order_by('-created')[:3]
        context['common_tags'] = Post.tags.values('name').annotate(count=Count('name')).order_by('-count')
        return context


class PostDetails(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = CommentCreateForm

    def post(self, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.order_by('-created')[:3]
        context['common_tags'] = Post.tags.values('name').annotate(count=Count('name')).order_by('-count')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.instance.post = self.get_object()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'post/post_create.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse('post:home')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.instance.slug = slugify(self.request.user.id) + slugify(get_random_string(18))
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'post/post_update.html'

    def get_success_url(self):
        return reverse('post:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_author'] = self.get_object().author.user
        context['post_slug'] = self.get_object().slug
        return context


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'

    def get_success_url(self):
        return reverse('post:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_author'] = self.get_object().author.user
        context['post_slug'] = self.get_object().slug
        return context


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = 'comment/comment_update.html'

    def get_success_url(self):
        return reverse('post:post-details', kwargs={'slug': self.get_object().post.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_user'] = self.get_object().author.user
        context['post_slug'] = self.get_object().post.slug
        return context


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse('post:post-details', kwargs={'slug': self.get_object().post.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_user'] = self.get_object().author.user
        context['post_slug'] = self.get_object().post.slug
        return context
