from django.urls import path

from shortnet.views import RedirectView


app_name = "shortnet"

urlpatterns = [path("<slug:short>/", RedirectView.as_view(), name="index")]
