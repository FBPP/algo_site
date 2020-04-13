#!/usr/bin/env python
# coding=utf-8

import subprocess 
import os
from algo.models import Question
import shlex

def compile(solution_id,language):
    build_cmd = {      
        "g++"    : "g++ main.cpp -O2 -Wall -lm --static -DONLINE_JUDGE -o main",
        "python3": 'python3 -m py_compile main.py',
    }
    p = subprocess.Popen(build_cmd[language], shell = True, cwd = "/home/pengpeng/windows_shared/algo_site/algo/judge/judge_space", 
        stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err =  p.communicate()#获取编译错误信息
    print(type(err))
    if p.returncode != 0: #返回值为0,编译成功
        return {"status" : "Compile Error", "text" : err}
    return {"text" : ""}

def run(q_id, cmd, data_count, u_id, cin_fd, cout_fd):
    q = Question.objects.get(pk = q_id)
    tl = ((q.time_limit) + 10) / 1000.0
    ml = q.memory_limit * 1024
    max_rss = 0
    max_vms = 0
    total_time = 0
    for i in range(data_count):
        args = shlex.split(cmd)
        p = subprocess.Popen(args, env = {"PATH" : "/judge_space"}, 
            cwd = "/home/pengpeng/windows_shared/algo_site/algo/judge/judge_space", stdin = cin_fd, 
            stdout = cout_fd)
        start = time.time()
        pid = p.pid
        glan = psutil.Process(pid)
        while True:
            time_to_now = time.time() - start + total_time
            if psutil.pid_exists(pid) is False:
                program_info["take_time"] = time_to_now * 1000
                program_info["take_memory"] = max_rss / 1024.0
                program_info["result"] = "Runtime Error"
                return program_info
            rss, vms = glan.get_memory_info()
            if p.poll() == 0:
                end = time.time()
                break
            if max_rss < rss:
                max_rss = rss
                print('max_rss = %s' %max_rss)
            if max_vms < vms:
                max_vms = vms
            if time_to_now > time_limit or max_rss > mem_limit:
                program_info["take_time"] = time_to_now * 1000  
                program_info["take_memory"] = max_rss / 1024.0
                if time_to_now > time_limit:
                    program_info["result"] = "Time Limit Exceeded"
                else:
                    program_info['result'] = "Memory Limit Exceeded"
                glan.terminate()
                return program_info
        logging.debug("max_rss = %s" %max_rss)
        logging.debug("max_vms = %s" %max_vms)
    program_info["take_time"] = total_time * 1000
    program_info["take_memory"] = max_rss / 1024.0
    program_info["result"] = "Finish"
    return program_info

def judge_result(problem_id,solution_id,data_num):
    currect_result = os.path.join(config.data_dir, str(problem_id), 'data%s.out'%data_num)
    user_result = os.path.join(config.work_dir, str(solution_id),'out%s.txt'%data_num)
    try:
        curr = file(currect_result).read().replace('\r','').rstrip()#删除\r,删除行末的空格和换行
        user = file(user_result).read().replace('\r','').rstrip()
    except:
        return False
    if curr == user:       #完全相同:AC
        return "Accepted"
    if curr.split() == user.split(): #除去空格,tab,换行相同:PE
        return "Presentation Error"
    if curr in user:  #输出多了
        return "Output limit"
    return "Wrong Answer"  #其他WA
    return {"status" : "Finish", "text" : err} 


    
    
