"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from mysite import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authViews

urlpatterns = [
    path("", views.index, name="index"),
    path('admin/', admin.site.urls),
    path("center/", include("center.urls", namespace="center")),
    path("vaccine/", include("vaccine.urls", namespace="vaccine")),
    path("campaign/", include("campaign.urls", namespace="campaign")),
    path("vaccination/", include("vaccination.urls", namespace="vaccination")),
    path("accounts/", include("user.urls", namespace="user")),
    path("password_reset/", authViews.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        authViews.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        authViews.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        authViews.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

