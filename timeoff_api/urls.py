from django.urls import path
from timeoff_api.views import Leave, Policy, Policies

urlpatterns = [
    path('policy/<str:org>/', Policies.as_view()),
    path('policy/<str:org>/<str:pk>/', Policy.as_view()),
    path('leaves/<str:org>/<str:eid>/', Leave.as_view())
]
