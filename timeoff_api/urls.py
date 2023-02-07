from django.urls import path
from timeoff_api.views import Leave, Policy

urlpatterns = [
    path('policies/', Policy.as_view()),
    path('policy/<str:pk>', Policy.as_view()),
    path('leaves/<str:eid>', Leave.as_view())
]
