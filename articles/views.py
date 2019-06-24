from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.utils.timezone import now
from django.contrib.auth.models import User

from .models import Article, Profile
from .forms import RegisterForm, LoginForm, ArticleForm, ProfileForm
from .utils import create_slug


def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, "profile.html", context)


def profile_edit(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {
        'form': form,
    }
    return render(request, "profile_edit.html", context)


def author_profile(request, username):
    user = User.objects.get(username=username)
    articles = user.articles.filter(draft=False).order_by("-published")
    context = {
        'user': user,
        'articles': articles,
    }
    return render(request, 'author_profile.html', context)


def draft_delete(request, article_slug):
    article = Article.objects.get(slug=article_slug)
    if request.user == article.author and article.draft:
        article.delete()

    return redirect("draft-list")


def draft_list(request):
    drafts_list = Article.objects.filter(draft=True, author=request.user)
    context = {
        'drafts': drafts_list,
        'draft_tab_status': "active"
    }
    return render(request, "draft_list.html", context)


def draft_edit(request, article_slug):
    article = Article.objects.get(slug=article_slug)
    form = ArticleForm(instance=article)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            if form.data.get("title") != article.title:
                article.slug = create_slug(article)
            article.save()
            if 'draft' not in form.data:
                article.draft = False
                article.published = now()
                article.save()
                return redirect("article-detail", article_slug=article.slug)
            return redirect('draft-list')
    context = {
        'form': form,
        'draft': article
    }
    return render(request, "draft_edit.html", context)


def article_list(request):
    articles_list = Article.objects.filter(draft=False)
    context = {
        'articles': articles_list
    }
    return render(request, "list.html", context)


def detail(request, article_slug):
    article_object = Article.objects.get(slug=article_slug)
    context = {
        'article': article_object
    }
    return render(request, "detail.html", context)


def article_create(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.slug = create_slug(article)
            if 'draft' in form.data:
                article.draft = True
            else:
                article.published = now()
            article.save()
            return redirect("article-list")
    context = {
        "form": form
    }
    return render(request, 'create.html', context)


def login_view(request):
    form = LoginForm()
    error_message = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('article-list')

        error_message = "Invalid username/password combination. Please try again."

    context = {
        'form': form,
        "error_message": error_message,
    }
    return render(request, "login.html", context)


def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            Profile.objects.create(user=user)

            login(request, user)
            return redirect("article-list")

    context = {
        "form": form,
    }
    return render(request, 'register.html', context)


def logout_view(request):
    logout(request)
    return redirect("login")
