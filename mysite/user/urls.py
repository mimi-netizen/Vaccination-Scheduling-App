from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("change-password/", views.change_password, name="change-password"),
    path("profile-view/", views.profile_view, name="profile-view"),
    path("profile-update/", views.profile_update, name="profile-update"),
    path("verify-email/", views.email_verificatin_request, name="verify-email"),
    path("email/activate/<uidb64>/<token>/", views.email_verifier, name="email-activate"),
]