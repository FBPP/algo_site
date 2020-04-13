from django.urls import path, include

from .import views

app_name = "algo"
urlpatterns = [
    path("", views.index_view, name = "index"),
    path("lg_index/<int:user_id>/", views.lg_index_view, name = "lg_index"),
    path("question/<int:user_id>/<int:q_id>", views.question_view, name = "question_index"),
    path("req_debug/", views.req_debug_view, name = "req_debug"),
]