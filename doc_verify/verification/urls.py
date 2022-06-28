from django.urls import path
from . import views

app_name = "verification"   

urlpatterns = [
    path("", views.document_view, name="home"),
]
