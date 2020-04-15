from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.views.decorators.csrf import requires_csrf_token
from django.http import JsonResponse

from .judge import jud
from .models import Question
from register.models import User

import json

import os
import shutil

judge_path = "/home/pengpeng/workplace/algo/algo_site/algo/judge/judge_space"

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
    q = Question.objects.get(pk = q_id)
    context = {}
    context['u'] = User.objects.get(pk = user_id)
    context['q'] = Question.objects.get(pk = q_id)
    context['t_l'] = q.time_limit / 1000
    context['m_l'] = round(q.memory_limit / 1024, 2)
    context['t_l'] = q.time_limit / 1000

    return render(request, "algo/question.html", context)

def req_debug_view(request):
    rec = json.loads(request.body.decode())
    res = {
        "result" : "",
        "cout" : "",
        "true_cout" : "",
        "cin_text" : "",
        "memoryused" : 0, 
        "timeused" : 0 
    }
    code = rec["code"]
    uid = rec["uid"]
    qid = rec["qid"]
    lang = rec["lang"]
    cin_exp = rec["cin_exp"]
    cin_exp = cin_exp.strip(" ")

    cur_name =  str(uid) + "_" + str(qid)
 
    src = judge_path + '/' + cur_name + ".cpp"
    src_f = open(src, "w")
    src_f.write(code)
    src_f.close()
    err =  jud.compile(src, lang, judge_path, cur_name)
    if err:
        res["result"] = err["status"]
        res["cout"] = err["text"]
        #shutil.rmtree(path) 
        os.remove(src)
        return JsonResponse(res)

    q = Question.objects.get(pk = qid)
    ques_info = {
        "t_l" : q.time_limit,
        "m_l" : q.memory_limit
    }

    rst = jud.debug(cin_exp, ques_info, cur_name, judge_path)
    res["result"] = rst["result"]
    if rst["result"] == "Accepted" or rst["result"] == "Presentation Error" or rst["result"] == "Wrong Answer": 
        res["result"] = "Finished"
        res["cout"] = rst["cout"]
    res["cin_text"] = cin_exp
    res["memoryused"] = round(rst["memoryused"] / 1024, 2)
    res["timeused"] = rst["timeused"]
    print(res)
    return JsonResponse(res)



def req_submit_view(request): 
    rec = json.loads(request.body.decode())
    res = {
        "result" : "",
        "cout" : "",
        "true_cout" : "",
        "cin_text" : "",
        "memoryused" : 0, 
        "timeused" : 0 
    }
    code = rec["code"]
    uid = rec["uid"]
    qid = rec["qid"]
    lang = rec["lang"]

    cur_name =  str(uid) + "_" + str(qid)
 
    src = judge_path + '/' + cur_name + ".cpp"
    src_f = open(src, "w")
    src_f.write(code)
    src_f.close()
    err =  jud.compile(src, lang, judge_path, cur_name)
    if err:
        res["result"] = err["status"]
        res["cout"] = err["text"]
        #shutil.rmtree(path) 
        os.remove(src)
        return JsonResponse(res)
    
    q = Question.objects.get(pk = qid)
    ques_info = {
        "t_l" : q.time_limit,
        "m_l" : q.memory_limit
    }

    
    td_path = judge_path + "/testdate/" + str(qid)
    print(td_path)
    td_total = q.test_total
    rst = jud.judge(td_path, td_total, ques_info, cur_name, judge_path)
    
    res["result"] = rst["result"]
    if(res["result"] != "Accepted"):
        if "cout" in rst:
            res["cout"] = rst["cout"]
        if "true_cout" in rst:
            res["true_cout"] = rst["true_cout"]
        res["cin_text"] = rst["cin_text"]
        print(res)
    res["memoryused"] = round(rst["memoryused"] / 1024, 2)
    res["timeused"] = rst["timeused"]
    os.remove(src)
    return JsonResponse(res) 


# Create your views here.
