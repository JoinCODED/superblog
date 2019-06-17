"""superblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from articles import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.article_list, name="article-list"),
    path('articles/create/', views.article_create, name="article-create"),
    path('articles/<slug:article_slug>/', views.detail, name="article-detail"),

    path('drafts/', views.draft_list, name="draft-list"),
    path('drafts/<slug:article_slug>/', views.draft_edit, name="draft-edit"),
    path('drafts/<slug:article_slug>/delete/', views.draft_delete, name="draft-delete"),

    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name="logout"),

    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.profile_edit, name="profile-edit"),
    path('profiles/<str:username>/', views.author_profile, name="author-profile"),
]
