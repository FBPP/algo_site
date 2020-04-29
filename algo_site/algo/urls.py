from django.urls import path, include

from .import views

app_name = "algo"
urlpatterns = [
    path("", views.index_view, name = "index"),
    path("lg_index/<int:user_id>/", views.lg_index_view, name = "lg_index"),
    path("question/<int:q_id>", views.question_view, name = "question_index"),
    path("req_debug/", views.req_debug_view, name = "req_debug"),
    path("req_submit/", views.req_submit_view, name = "req_submit"),
    path("submission/<int:q_id>", views.submission_view, name = "submission"),
    path("record_item/<int:record_id>/<int:q_id>", views.record_item_view, name = "record_item"),
    path("solution", views.solution_view, name = "solution"),
    path("solution_item/<int:sol_id>", views.solution_item_view, name = "solution_item"),
    path("write_sol", views.write_solution_view, name = "write_sol"),
    path("sol_submit", views.sol_submit, name = "sol_submit"),
    path("req_sol_delete", views.req_sol_delete, name = "req_sol_delete"),
    path("edit_sol", views.edit_sol_view, name = "edit_sol"),
    path("sol_update", views.sol_update_view, name = "sol_update"),
    path("up_vote", views.up_vote_view, name = "up_vote"),
    path("down_vote", views.down_vote_view, name = "down_vote"),
    path("comment_sub", views.comment_sub_view, name = "comment_sub")
]