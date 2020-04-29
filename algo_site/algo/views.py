from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.views.decorators.csrf import requires_csrf_token
from django.http import JsonResponse
from django.utils import timezone

from .judge import jud
from .models import Question, Record, Solution, Sol_vote, Sol_comment
from register.models import User

import json

import os
import shutil
import sys

judge_path = "/home/pengpeng/workplace/algo/algo_site/algo/judge/judge_space"


def check_session(request):
    if "email" in request.session and "password" in request.session:
        u = User.objects.get(email = request.session["email"])
        res = {
            "exist" : True,
            "uid" : u.pk          
        }
        return res
    else:
        res = {
            "exist": False,
        }

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
def question_view(request, q_id):
    rst = check_session(request)
    context = {}
    if rst["exist"]:
        q = Question.objects.get(pk = q_id)
        context['u'] = User.objects.get(pk = rst["uid"])
        context['q'] = Question.objects.get(pk = q_id)
        context['t_l'] = q.time_limit / 1000
        context['m_l'] = round(q.memory_limit / 1024, 2)
        context['t_l'] = q.time_limit / 1000

        return render(request, "algo/question.html", context)
    else:
        #TODO
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

    u = User.objects.get(pk = uid)
    subm = Record.objects.create(q_id = q, u_id = u, status = res["result"], code = code, lang = lang, time =  timezone.now(), 
        timeused = res["timeused"], memoryused = res["memoryused"])
    subm.save()

    return JsonResponse(res) 


def submission_view(request, q_id):
    res = check_session(request)
    q = Question.objects.get(pk = q_id)
    context = {}
    if res["exist"]:
        context = {}
        context["u"] = User.objects.get(pk = res["uid"])
        context["record_list"] = Record.objects.filter(q_id = q_id, u_id = res["uid"] ).order_by("-time")
        context['q'] = q
        return render(request, "algo/submission.html", context)
    else:
        return JsonResponse("res")

def record_item_view(request, record_id, q_id):
    res = check_session(request)
    q = Question.objects.get(pk = q_id)
    record = Record.objects.get(pk = record_id)
    context = {
        "u" : User.objects.get(pk = res["uid"]),
        "q" : q,
        "cur" : record
    }
    return render(request, "algo/record_item.html", context)
        
        
def solution_view(request):
    rst = check_session(request)

    u = User.objects.get(pk = rst["uid"])   
    sol_list = Solution.objects.order_by("-time", "vote")
    context = {}
    context["sol_list"] = sol_list
    context["u"] = u;
    return render(request, "algo/solution.html", context)   

@requires_csrf_token
def solution_item_view(request, sol_id):
    rst = check_session(request)

    u = User.objects.get(pk = rst["uid"])  
    sol_obj = Solution.objects.get(pk = sol_id)

    context = {}
    try:
        sol_vote_obj = Sol_vote.objects.filter(sol_id = sol_obj, u_id = u)[0]
    except:
        context["vote_exist"] = False
    else:
        context["vote_exist"] = True
        context["sol_vote"] = sol_vote_obj
        print(str(sys._getframe().f_lineno) + " sol_vote existed", sol_vote_obj.up, sol_vote_obj.down)

    comment_list = Sol_comment.objects.filter(sol_id = sol_obj)
    context.update({
        "u" : u,
        "sol" : sol_obj,
        "aid" : sol_obj.author_id.pk,
        "content" : json.dumps(sol_obj.content),
        "comment_list": comment_list
    })

    return render(request, "algo/solution_item.html", context)


def write_solution_view(request):
    rst = check_session(request)

    u = User.objects.get(pk = rst["uid"])
    context = {}
    context["u"] = u
    return render(request, "algo/write_sol.html", context)

def sol_submit(request):
    rst = check_session(request)

    author = User.objects.get(pk = rst["uid"])
    qid = request.POST["question_id"]
    title = request.POST["title"]
    level = request.POST["level"]
    source_link = request.POST["source_link"]
    time = timezone.now()
    content = request.POST["mark_text"]

    sol_obj = Solution.objects.create(author_id = author, qid = qid, title = title, source_link = source_link, 
                level =  level,time = time, content = content)
    sol_obj.save()
    return HttpResponseRedirect(reverse("algo:solution_item", args = (sol_obj.pk, )))

def req_sol_delete(request):
    rst = check_session(request)
    req = json.loads(request.body.decode())
    is_del = req["del"]
    res = {}
    if is_del:
        sol_id = req["sol_id"]
        sol_obj = Solution.objects.get(pk = sol_id)
        sol_obj.delete()
        res["has_deleted"] = True
        return JsonResponse(res)

def edit_sol_view(request):
    rst = check_session(request)
    u = User.objects.get(pk = rst["uid"])
    sol_id = request.POST["sol_id"]
    sol_obj = Solution.objects.get(pk = sol_id)
    context = {
        "u" : u,
        "sol" : sol_obj,
        "content" : json.dumps(sol_obj.content),
    }
    print(sol_obj)
    return render(request, "algo/edit_sol.html", context)

def sol_update_view(request):
    rst = check_session(request)

    sol_id = request.POST["sol_id"]
    qid = request.POST["question_id"]
    title = request.POST["title"]
    level = request.POST["level"]
    source_link = request.POST["source_link"]
    time = timezone.now()
    content = request.POST["mark_text"]

    sol_obj = Solution.objects.get(pk = sol_id)
    sol_obj.qid = qid
    sol_obj.title = title
    sol_obj.source_link = source_link
    sol_obj.time = time
    sol_obj.level = level
    sol_obj.content = content
    sol_obj.save()

    return HttpResponseRedirect(reverse("algo:solution_item", args = (sol_obj.pk, )))
    
def up_vote_view(request):
    rst = check_session(request)
    req = json.loads(request.body.decode())
    u = User.objects.get(pk = rst["uid"])

    flag = req["flag"]
    sol_id = req["sol_id"]
    sol_obj = Solution.objects.get(pk = sol_id)
    print(sol_obj)
    sol_obj.vote += flag
    sol_obj.save()
    
    try:
        sol_vote_obj = Sol_vote.objects.filter(sol_id = sol_obj, u_id = u)[0]
        
    except:
        vote_obj = Sol_vote.objects.create(sol_id = sol_obj,  u_id = u, up = flag)
        vote_obj.save()
    else:
        sol_vote_obj.up += flag
        sol_vote_obj.save()
    
    return HttpResponse()

def down_vote_view(request):
    rst = check_session(request)
    req = json.loads(request.body.decode())
    u = User.objects.get(pk = rst["uid"])

    flag = req["flag"]
    sol_id = req["sol_id"]
    sol_obj = Solution.objects.get(pk = sol_id)
    print(sol_obj)
    sol_obj.vote += flag
    sol_obj.save()
    
    try:
        sol_vote_obj = Sol_vote.objects.filter(sol_id = sol_obj, u_id = u)[0]
    except:
        vote_obj = Sol_vote.objects.create(sol_id = sol_obj,  u_id = u, down = flag)
        vote_obj.save()
    else:
        sol_vote_obj.down += flag
        sol_vote_obj.save()
    
    return HttpResponse()

def comment_sub_view(request):
    rst = check_session(request)
    content = request.POST["content"]
    sol_id = request.POST["sol_id"]
    print("--------",str(sol_id))
    sol_obj = Solution.objects.get(pk = sol_id)
    u = User.objects.get(pk = rst["uid"])
    sol_comm_obj = Sol_comment.objects.create(sol_id = sol_obj, u_id = u, time = timezone.now(), text = content)
    sol_comm_obj.save() 
    return HttpResponseRedirect(reverse("algo:solution_item", args = (sol_obj.pk, )))
    
    


# Create your views here.
