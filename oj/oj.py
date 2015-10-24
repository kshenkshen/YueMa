#!/usr/bin/env python2
# coding=utf8

import bottle
import json
import time
import hashlib
import base64
import os
import subprocess
import shutil
import threading
import random
import re

from threading import Thread
from bottle import post, get, request, response
from apscheduler.schedulers.background import BackgroundScheduler

LIMIT_RUN_PATH = './limitrun.sh'
ROOT_DIR = './problems/'
TEMP_DIR = ROOT_DIR + 'temp/'
IO_DIR = ROOT_DIR + 'io/'

JUDGE_QUEUE = []
PROBLEMS_STATUS = {}
STATUS_W_LOCK = threading.RLock()

random.seed(time.time())


def _py_judge(pid, filename):
    ret_dict = {'ac': False,
                'err_code': 0,
                'message': None,
                'results': []}

    for i in range(2):
        run_proc = subprocess.Popen([LIMIT_RUN_PATH,
                                     "/usr/bin/python2", filename],
                                    stdin=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    stdout=subprocess.PIPE,
                                    shell=False)

        in_str = open("%s%s.input%d" % (IO_DIR, pid, i)).read()
        run_proc.stdin.write(in_str)
        run_proc.stdin.close()
        run_proc.wait()

        retcode = run_proc.returncode
        run_result = run_proc.stdout.read().rstrip()

        if retcode != 0:
            ret_dict['results'].append({'ac': False,
                                        'err_code': 1,
                                        'message': run_result})
            continue

        right_ans = open("%s%s.output%d" % (IO_DIR, pid, i)).read().rstrip()

        if right_ans != run_result:
            ret_dict['results'].append({'ac': False,
                                        'err_code': 2,
                                        'message': 'wrong answer'})
            continue

        ret_dict['results'].append({'ac': True})

    for result in ret_dict['results']:
        if not result['ac']:
            ret_dict['ac'] = False
            return ret_dict

    ret_dict['ac'] = True
    return ret_dict


def _c_judge(pid, filename):
    ret_dict = {'ac': False,
                'err_code': 0,
                'message': None,
                'results': []}

    # compile
    run_proc = subprocess.Popen(["/usr/bin/gcc",
                                 '-O2',
                                 '-o', re.sub('\.c$', '', filename),
                                 filename],
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE,
                                shell=False)

    run_proc.wait()
    retcode = run_proc.returncode
    run_result = run_proc.stdout.read()

    if retcode != 0:
        ret_dict['ac'] = False
        ret_dict['err_code'] = 1
        ret_dict['message'] = run_result
        return ret_dict

    for i in range(2):
        # execute
        run_proc = subprocess.Popen([LIMIT_RUN_PATH,
                                     re.sub('\.c$', '', filename)],
                                    stdin=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    stdout=subprocess.PIPE,
                                    shell=False)

        in_str = open("%s%s.input%d" % (IO_DIR, pid, i)).read()
        run_proc.stdin.write(in_str)
        run_proc.stdin.close()
        run_proc.wait()
        run_result = run_proc.stdout.read().rstrip()
        right_ans = open("%s%s.output%d" % (IO_DIR, pid, i)).read().rstrip()

        if right_ans != run_result:
            ret_dict['results'].append({'ac': False,
                                        'err_code': 2,
                                        'message': 'wrong answer'})
            continue

        ret_dict['results'].append({'ac': True})

    for result in ret_dict['results']:
        if not result['ac']:
            ret_dict['ac'] = False
            return ret_dict

    ret_dict['ac'] = True
    return ret_dict


def judge(pid, fid, code_str, lang):
    submit_dir = TEMP_DIR + fid + '/'
    if not os.path.exists(os.path.dirname(submit_dir)):
        os.makedirs(os.path.dirname(submit_dir))

    if lang == 'py':
        code_filename = submit_dir + fid + '.py'
        with open(code_filename, 'w') as f:
            f.write(code_str)

        with STATUS_W_LOCK:
            PROBLEMS_STATUS.setdefault(fid, {})
            PROBLEMS_STATUS[fid]['ac'] = False
            PROBLEMS_STATUS[fid]['status_code'] = 0

        res = _py_judge(pid, code_filename)

        with STATUS_W_LOCK:
            PROBLEMS_STATUS.setdefault(fid, {})
            PROBLEMS_STATUS[fid]['ac'] = res['ac']
            PROBLEMS_STATUS[fid]['status_code'] = 1
    elif lang == 'c':
        code_filename = submit_dir + fid + '.c'
        with open(code_filename, 'w') as f:
            f.write(code_str)

        with STATUS_W_LOCK:
            PROBLEMS_STATUS.setdefault(fid, {})
            PROBLEMS_STATUS[fid]['ac'] = False
            PROBLEMS_STATUS[fid]['status_code'] = 0

        res = _c_judge(pid, code_filename)

        with STATUS_W_LOCK:
            PROBLEMS_STATUS.setdefault(fid, {})
            PROBLEMS_STATUS[fid]['ac'] = res['ac']
            PROBLEMS_STATUS[fid]['status_code'] = 1
    else:
        # TODO other langs
        pass

    shutil.rmtree(submit_dir)


def _check_queue():
    while JUDGE_QUEUE:
        args = JUDGE_QUEUE.pop(0)
        Thread(target=judge, args=args).start()


@post('/oj/submit/')
def submit():
    # {'success': bool, 'err_code': int, 'fid': str}
    try:
        req_dict = json.loads(request.body.read())
    except ValueError:
        response.status = 400
        return {'success': False,
                'err_code': 0,
                'fid': None}

    if {'pid', 'code', 'lang'} != set(req_dict.keys()):
        response.status = 400
        return {'success': False,
                'err_code': 1,
                'fid': None}

    try:
        code_str = base64.b64decode(req_dict['code'])
    except TypeError:
        return {'success': False,
                'err_code': 2,
                'fid': None}

    fid = hashlib.md5(code_str + str(time.time())).hexdigest()
    JUDGE_QUEUE.append([str(req_dict['pid']), fid, code_str, req_dict['lang']])
    return {'success': True,
            'err_code': None,
            'fid': fid}


@get('/oj/status/:fid')
def status(fid):
    # {'ac': bool, 'status_code': int}
    # status_code: 0 -> processing
    #              1 -> done
    return PROBLEMS_STATUS.get(fid, {})


@get('/oj/problems/random/:diff')
def random_pro(diff):
    # {'pid': int, 'desc': str}
    diffs = [0, 1, 2]
    if int(diff) not in diffs:
        return {'pid': None, 'desc': None}

    diff_dir = ROOT_DIR + 'problems/%s/' % diff
    if not os.path.exists(diff_dir):
        os.makedirs(diff_dir)

    pro_filename = random.choice(os.listdir(diff_dir))
    pro_desc = open(diff_dir + pro_filename).read()
    return {'pid': int(re.sub('\.txt$', '', pro_filename)),
            'desc': pro_desc}

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(_check_queue, 'interval', seconds=1)
    scheduler.start()
    app = bottle.app()
    bottle.debug(True)
    bottle.run(app=app)
