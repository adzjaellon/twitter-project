from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Post, Comment
from django.views.generic.edit import FormMixin
from .forms import CommentCreateForm, PostCreateForm
from django.db.models import Count, Q


def search(request):
    q = request.GET.get('q')
    if q:
        queryset = Post.objects.all().filter(Q(body__icontains=q) | Q(tags__name__icontains=q)).distinct()

    context = {
        'posts': queryset
    }
    return render(request, 'blog.html', context)


class PostList(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 6
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.order_by('-created')[:3]
        context['common_tags'] = Post.tags.values('name').annotate(count=Count('name')).order_by('-count')
        return context


class PostDetails(FormMixin, DetailView):
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


class CommentUpdate(UpdateView):
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


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'comment/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse('post:post-details', kwargs={'slug': self.get_object().post.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_user'] = self.get_object().author.user
        context['post_slug'] = self.get_object().post.slug
        return context
