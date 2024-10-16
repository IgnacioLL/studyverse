from django.urls import path

from accounts import views
from accounts.views.signup import activate

app_name = "accounts"


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signout/", views.signout, name="signout"),
    path("activate/<uidb64>/<token>", activate, name="activate")
]
