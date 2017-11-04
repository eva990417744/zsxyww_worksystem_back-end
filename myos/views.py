import platform
import psutil
from decimal import Decimal
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
import simplejson
import re
from django.contrib.auth import authenticate, logout, login
from datetime import datetime, timedelta


def is_login(request):
    if request.user.is_authenticated():
        return JsonResponse({'success': 'success'})
    else:
        return JsonResponse({'false': 'false'})


def try_login(request):
    if request.method == 'POST':
        try:
            req = simplejson.loads(request.body)
            username = req['username']
            password = req['password']
            user = authenticate(username=username, password=password)
        except:
            return JsonResponse({'error', 'error'})
        else:
            if user is not None:
                if user.is_active:
                    try:
                        if req['longtime']:
                            request.session.set_expiry(datetime.now() + timedelta(days=365))
                    except:
                        time = req['time']
                        if time == False:
                            request.session.set_expiry(0)
                        else:
                            request.session.set_expiry(691200)
                    login(request, user)
                    return JsonResponse({'success': 'success'})
                else:
                    return JsonResponse({'error', 'error'})
            else:
                return JsonResponse({'error', 'error'})
    else:
        return JsonResponse({'error', 'error'})


def try_logout(request):
    logout(request)
    return JsonResponse({'success': 'success'})


def change(what):
    what = int(what)
    what = what / 2 ** 20
    what = int(Decimal(what).quantize(Decimal('0.00')))
    return what


def system(request):
    p = platform.uname()
    system = {'system': p[0], 'kernel': p[2], 'architecture': p[4]}
    return JsonResponse({'system': system})


def now(request):
    now = {'cpu': psutil.cpu_count(), 'cpu_use': psutil.cpu_percent(0.1), 'pid': [],
           'swap_total': change(psutil.swap_memory()[0]),
           'swap_free': change(psutil.swap_memory()[2]), 'swap_percent': psutil.swap_memory()[3],
           'memory_total': change(psutil.virtual_memory()[1]), 'memory_used': change(psutil.virtual_memory()[3]),
           'memory_percent': psutil.virtual_memory()[2], 'net_sent': change(psutil.net_io_counters()[0]),
           'net_recv': change(psutil.net_io_counters()[1]), 'disk': []}
    for x in psutil.pids():
        p = psutil.Process(x)
        pid = {'name': p.name(), 'status': p.status(), 'pid': x,
               'memory': str(Decimal(p.memory_percent()).quantize(Decimal('0.00'))) + "%"}
        now['pid'].append(pid)
    for x in psutil.disk_partitions():
        now['disk'].append(
            {'disk_total': change(psutil.disk_usage(x[1])[0]), 'disk_used': change(psutil.disk_usage(x[1])[1]),
             'disk_percent': psutil.disk_usage(x[1])[3]})
    sorted(now['pid'], key=order)
    now['pid'].reverse()
    return JsonResponse({'now': now})


def nametopid(x):
    num = []
    for r in psutil.process_iter():
        aa = str(r)
        f = re.compile(x, re.I)
        if f.search(aa):
            num.append(aa.split('pid=')[1].split(',')[0])
    return num

def order(s):
    return s['memory']


def killprocesstree(request):
    req = simplejson.loads(request.body)
    x = str(req['pid'])
    select = req['select']
    if select:
        if x.isdigit():
            try:
                for pid in psutil.pids():
                    if psutil.Process(int(pid)).ppid() == int(x):
                        psutil.Process(int(pid)).terminate()
                psutil.Process(int(x)).terminate()
            except Exception:
                return JsonResponse({'error': 'input the right pid'})
        else:
            try:
                for pid in psutil.pids():
                    if str(psutil.Process(int(pid)).ppid()) in nametopid(x):  # if 'a' in theList:
                        psutil.Process(int(pid)).terminate()
                for i in nametopid(x):
                    psutil.Process(int(i)).terminate()
            except Exception:
                return JsonResponse({'error': 'input the right pname!'})
    else:
        if x.isdigit():
            psutil.Process(int(x)).terminate()
            return JsonResponse({'error': 'input the right pid'})
        else:
            for i in nametopid(x):
                psutil.Process(int(i)).terminate()
            return JsonResponse({'error': 'input the right pname!'})

    now = {'cpu': psutil.cpu_count(), 'cpu_use': psutil.cpu_percent(0.1), 'pid': [],
           'swap_total': change(psutil.swap_memory()[0]),
           'swap_free': change(psutil.swap_memory()[2]), 'swap_percent': psutil.swap_memory()[3],
           'memory_total': change(psutil.virtual_memory()[1]), 'memory_used': change(psutil.virtual_memory()[3]),
           'memory_percent': psutil.virtual_memory()[2], 'net_sent': change(psutil.net_io_counters()[0]),
           'net_recv': change(psutil.net_io_counters()[1]), 'disk': []}
    for x in psutil.pids():
        p = psutil.Process(x)
        pid = {'name': p.name(), 'status': p.status(), 'pid': x,
               'memory': str(Decimal(p.memory_percent()).quantize(Decimal('0.00'))) + "%"}
        now['pid'].append(pid)
    for x in psutil.disk_partitions():
        now['disk'].append(
            {'disk_total': change(psutil.disk_usage(x[1])[0]), 'disk_used': change(psutil.disk_usage(x[1])[1]),
             'disk_percent': psutil.disk_usage(x[1])[3]})
    sorted(now['pid'], key=order)
    now['pid'].reverse()
    return JsonResponse({'now': now})
