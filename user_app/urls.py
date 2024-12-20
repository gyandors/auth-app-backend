from django.urls import path
from .apis import RegisterAPI, LoginAPI, UpdateAPI, Setup2FAAPI, Verify2FAAPI

urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("setup-2fa/", Setup2FAAPI.as_view(), name="setup-2fa"),
    path("verify-2fa/", Verify2FAAPI.as_view(), name="verify-2fa"),
    path("update/", UpdateAPI.as_view(), name="update"),
]
