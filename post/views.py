from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView
from .models import Post, Comment
from django.views.generic.edit import FormMixin
from .forms import CommentCreateForm, PostCreateForm


class PostList(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 6
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.order_by('-created')[:3]
        context['common_tags'] = Post.tags.most_common()[:5]
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

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.instance.post = self.get_object()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(self.request.GET('HTTP_REFERER'))


def post(request):
    return render(request, 'post.html', {})