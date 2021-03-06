from django.shortcuts import render, redirect
from .models import Article
from django.contrib.auth.decorators import login_required
from . import forms


def article_list(request):
    articles_to_show = Article.objects.all().order_by('date')
    return render(request, 'articles/article_list.html', {'articles': articles_to_show})


def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    return render(request, 'articles/article_details.html', {'article': article})


@login_required(login_url="/accounts/login/")
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_create.html', {'form': form})
