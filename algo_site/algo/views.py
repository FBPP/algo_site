from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.views.decorators.csrf import requires_csrf_token
from django.http import JsonResponse

from .judge import jud
from .models import Question
from register.models import User

import os

judge_path = "/home/pengpeng/windows_shared/algo_site/algo/judge/judge_space/"

def index_view(request):
    if "email" in request.session and "password" in request.session:
        u = User.objects.get(email = request.session["email"])
        return HttpResponseRedirect(reverse("algo:lg_index", args = (u.pk, )))
    else:
        context = {}
        context["question_list"] = Question.objects.order_by("pk")
        return render(request, "algo/lg_index.html", context)

def lg_index_view(request, user_id):
    context = {}
    context["question_list"] = Question.objects.order_by("pk")
    context["u"] = User.objects.get(pk = user_id)
    return render(request, "algo/lg_index.html", context)


@requires_csrf_token
def question_view(request, user_id, q_id):
    context = {}
    context['u'] = User.objects.get(pk = user_id)
    context['q'] = Question.objects.get(pk = q_id)
    return render(request, "algo/question.html", context)

def req_debug_view(request): 
    text = request.POST["code"]
    uid = request.POST["uid"]
    qid = request.POST["qid"]

    err = jud.compile(1, "g++")
    print(type(err))
    rt = err["text"]
    if(rt):
        res = { "cout" : rt}
    
    q = Question.objects.get(pk = qid)
    path_in = judge_path + qid + ".in"
    path_out = judge_path + qid + ".out" 
    cin_fd = open(path_in, 'w')
    cin_fd.write(q.cin_example)
    cout_fd = open(path_out, 'w')

    jud.run(qid, "./main", 1, uid, cin_fd, cout_fd)

    cout_fd = open(path_out, 'r')
    out = cout_fd.read()

    res["cout" : out]

    os.remove(path_in)
    os.remove(path_out)


    return JsonResponse(res) 


# Create your views here.
