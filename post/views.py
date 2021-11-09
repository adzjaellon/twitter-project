from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.db.models import Count, Q
from .models import Post, Comment, LikeUnlike
from .forms import CommentCreateForm, PostCreateForm
from taggit.models import Tag
from user_profile.models import Profile
from itertools import chain


class Search(View):
    def get(self, request, **kwargs):
        q = request.GET.get('q')
        if q:
            queryset = Post.objects.filter(Q(body__icontains=q) | Q(tags__name__icontains=q)).distinct()
        else:
            queryset = []

        context = {
            'posts': queryset,
        }
        return render(request, 'blog.html', context)


class LikePost(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        print('like post request: ', request)
        pk = request.POST.get('pk')
        post = Post.objects.get(pk=pk)
        user = Profile.objects.get(user=request.user)

        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)

        like, created = LikeUnlike.objects.get_or_create(post=post, profile=user)

        if created:
            like.status = 'Like'
            post.save()
            like.save()
        else:
            if like.status == 'Like':
                like.status = 'Unlike'
            else:
                like.status = 'Like'
            like.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PostList(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 6
    template_name = 'blog.html'

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        users = [user for user in profile.following.all()]
        posts = []

        if profile.user not in users:
            posts.append(profile.posts.all())

        for user in users:
            prof = Profile.objects.get(user=user)
            posts.append(prof.posts.all())

        queryset = None
        if len(posts):
            queryset = sorted(chain(*posts), reverse=True, key=lambda obj: obj.created)
        return queryset


class PostTagList(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'tag_posts'
    template_name = 'post/post_tag_list.html'
    paginate_by = 4

    def get_queryset(self):
        name = self.request.resolver_match.kwargs.get('name')
        tag = get_object_or_404(Tag, name=name)
        return Post.objects.filter(tags__name__in=[tag.name])


class PostDetails(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = CommentCreateForm

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        post = get_object_or_404(Post, slug=slug)

        if self.request.user.profile not in post.author.user.following.all() and post.followers_only and self.request.user.profile != post.author:
            return None
        else:
            return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['author'] = get_object_or_404(Post, slug=slug).author
        return context

    def post(self, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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
        messages.success(self.request, 'Post has been created succesfully!')
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

    def form_valid(self, form):
        messages.success(self.request, 'Post has been updated!')
        return super().form_valid(form)


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
