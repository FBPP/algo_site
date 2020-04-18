#!/usr/bin/env python
# coding=utf-8

import subprocess 
import os
from algo.models import Question
import shlex
import lorun


def compile(src, language, path, cur_name):

    build_cmd = {      
        "c++"    : "g++ " + src + " -o " + cur_name,
        "python3": 'python3 -m py_compile main.py',
    }
    print(build_cmd[language])
    
    p = subprocess.Popen(build_cmd[language], shell = True, cwd = path, 
        stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err =  p.communicate()#获取编译错误信息
    text_err = str(err, encoding="utf-8")
    print(text_err)
    if p.returncode != 0: #返回值为0,编译成功
        return {"status" : "Compile Error", "text" : text_err}
    return {}

RESULT_STR = [
    'Accepted',
    'Presentation Error',
    'Time Limit Exceeded',
    'Memory Limit Exceeded',
    'Wrong Answer',
    'Runtime Error',
    'Output Limit Exceeded',
    'Compile Error',
    'System Error'
]


def runone(in_path, out_path, ques_info, cur_name):
    temp_name = cur_name + ".out" 
    fin = open(in_path)
    cin_text = fin.read()
    fin.close()
    fin = open(in_path)
    ftemp = open(temp_name, "w")

    runcfg = {
        "args" : ["./" + cur_name],
        "fd_in" : fin.fileno(),
        "fd_out" : ftemp.fileno(),
        "timelimit" : ques_info["t_l"],
        "memorylimit": ques_info["m_l"]
    }

    print("runone", runcfg["args"])
    
    rst = lorun.run(runcfg)
    fin.close()
    ftemp.close()

    if rst["result"] == 0:
        ftemp = open(temp_name)
        fout = open(out_path)
        crst = lorun.check(fout.fileno(), ftemp.fileno())
        
        ftemp.close()

        if crst != 0:
            ftemp = open(temp_name)
            _t = ftemp.read()
            out = fout.read()
            i = len(_t) - 1
            while i >= 0 and ( _t[i] == '\n' or _t[i] == ' '):
                i -= 1
            t = _t[0 : i + 1]
            if(t == out):
                crst == 0
            else:   
                rst["result"] = crst
                rst["cout"] = t
                rst["true_cout"] = out
                ftemp.close()
                fout.close()
    rst["cin_text"] = cin_text
    os.remove(temp_name)
    print("run_one:" , rst)
    return rst

def debug(str_in, ques_info, cur_name, exec_path):
    os.chdir(exec_path)
    cin_name = cur_name + "in"
    fin = open(cin_name, "w")
    fin.write(str_in)
    fin.close()
    fin = open(cin_name, "r")

    temp_name = cur_name + ".out"
    ftemp = open(temp_name, "w")

    runcfg = {
        "args" : ["./" + cur_name],
        "fd_in" : fin.fileno(),
        "fd_out" : ftemp.fileno(),
        "timelimit" : ques_info["t_l"],
        "memorylimit": ques_info["m_l"]
    }
    rst = lorun.run(runcfg)
    fin.close()
    ftemp.close()

    rst["result"] = RESULT_STR[rst["result"]]
    ftemp = open(temp_name)
    _t = ftemp.read()
    i = len(_t) - 1
    while i >= 0 and (_t[i] == '\n' or _t[i] == ' '):
        i -= 1
    t = _t[0 : i + 1]
    rst["cout"] = t
    ftemp.close()
    os.remove(temp_name)
    os.remove(cin_name)
    print("debug:" , rst)
    return rst



def judge(td_path, td_total, ques_info, cur_name, exec_path):
    os.chdir(exec_path)

    for i in range(td_total):
        in_path = td_path + '/' + str(i) + ".in"
        out_path = td_path + '/' + str(i) + ".out"

        print(in_path)
        print(out_path)
        res = {
            "result" : "",
            "memoryused" : 0,
            "timeused" : 0,
        }
        if os.path.isfile(in_path) and os.path.isfile(out_path):
            rst = runone(in_path, out_path, ques_info, cur_name)
            rst["result"] = RESULT_STR[rst["result"]]
            if rst["result"] != "Accepted":
                print(rst)
                os.remove(cur_name)
                return rst
            res["result"] = "Accepted"
            res["memoryused"] = max(rst["memoryused"], res["memoryused"])
            res["timeused"] = max(rst["timeused"], res["timeused"])  
        else:
            print('testdata:%d incompleted' % i)
            os.remove(cur_name)
            exit(-1)
    os.remove(cur_name)
    return res


    
