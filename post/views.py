from django.shortcuts import render

def index(request):
    return render(request, 'index.html', context={})

def blog(request):
    return render(request, 'blog.html', context={})
