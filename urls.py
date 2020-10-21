from django.urls import path

from .views import PersonView, PersonDetailView, CompareView

urlpatterns = [
    path('persons/', PersonView.as_view()),
    path('persons/compare/', CompareView.as_view()),
    path('persons/<uuid:person_id>/', PersonDetailView.as_view()),
]