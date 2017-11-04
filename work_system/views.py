from work_system.models import *
from django.contrib.auth import authenticate, logout, login
from django.middleware.csrf import get_token
from datetime import datetime, timedelta
from .Josn import *
from django.contrib.auth.models import User
import simplejson
from work_system.Josn import json
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
import re


def initialization(request):
    login_return = {}
    users = User.objects.get(username=request.user.username)
    login_return.update({'announcement': Announcement.objects.all()[0].notice_content,
                         'user': {'ID': users.username,
                                  'name': users.last_name, 'workPlace': users.personal.work_area,
                                  'job': users.groups.all()[0].name, 'workDay': users.personal.week_day,
                                  'work_phone': users.personal.work_phone}})
    personal = []
    personals = Personal.objects.filter(week_day=int(datetime.today().weekday()))
    for x in personals:
        personal.append(
            {'work_number': x.work_number, 'name': x.name, 'person_phone': x.phone_number, 'area': x.work_area,
             'work_phone': x.work_phone})
    extra_works = Extra_Work.objects.filter(extra_work_time=(str(datetime.now().date()) + ':16.30'), status=1)
    for x in extra_works:
        a = Personal.objects.get(work_number=x.work_number)
        personal.append(
            {'work_number': a.work_number, 'name': a.name, 'person_phone': a.phone_number, 'area': x.extra_area
                , 'work_phone': a.work_number})
    login_return.update({'works': personal})
    work_orders = Work_Situation.objects.filter(status=0).exclude(situation_order=0)
    work_order_1 = 0
    work_orders_2 = 0
    work_orders_3 = 0
    work_orders_4 = 0
    for x in work_orders:
        if x.situation_order == 3:
            work_order_1 += 1
        elif (x.situation_order == 1 and x.operator == '中国移动') or (x.situation_order == 2 and x.operator == '中国移动'):
            work_orders_2 += 1
        elif (x.situation_order == 1 and x.operator == '中国移动') or (x.situation_order == 2 and x.operator == '中国电信'):
            work_orders_3 += 1
        elif (x.situation_order == 1 and x.operator == '中国移动') or (x.situation_order == 2 and x.operator == '中国联通'):
            work_orders_4 += 1
    login_return.update({'work_orders': {'telecom': work_order_1, 'mobile': work_orders_2, 'unicom': work_orders_4,
                                         'complaints': work_orders_3}})
    try:
        check = Check_In.objects.filter(work_number=request.user.username).order_by('id').reverse()[0]
    except:
        login_return.update({'check': False, 'place': ''})
    else:
        if check.check == 0:
            login_return.update({'check': True, 'place': check.check_in_area})
        else:
            login_return.update({'check': False, 'place': ''})
    return login_return


@permission_required('work_system.change_announcement')
def change_announcement(request):
    try:
        req = simplejson.loads(request.body)
        a = Announcement.objects.all()[0]
        a.notice_content = req['content']
    except:
        return json.post_error
    else:
        a.save()
        return json.success({'content': a.notice_content})


def is_login(request):
    csrf_token = get_token(request)
    login_return = {'csrf_token': csrf_token}
    if request.user.is_authenticated():
        login_return.update({'is_login': True})
        login_return.update(initialization(request))
        return json.success(login_return)
    else:
        login_return.update({'is_login': False})
        return json.failure(login_return)


@login_required
def try_logout(request):
    logout(request)
    return json.ok


def try_login(request):
    if request.method == 'POST':
        try:
            req = simplejson.loads(request.body)
            username = req['username']
            password = req['password']
            user = authenticate(username=username, password=password)
        except:
            return json.post_error
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
                    login_return = {}
                    login_return.update(initialization(request))
                    return json.success(login_return)
                else:
                    return json.what_error('username&password error')
            else:
                return json.what_error('username&password error')
    else:
        return json.no_post


@login_required
def personal_change(request):
    try:
        if Check_In.objects.filter(work_number=request.user.username).order_by('id').reverse()[0].check == 0 or (
                        timedelta(
                            hours=datetime.now().hour, minutes=datetime.now().minute) >= timedelta(minutes=0,
                                                                                                   hours=16) and timedelta(
                    hours=datetime.now().hour, minutes=datetime.now().minute) < timedelta(minutes=0, hours=18)):
            return json.what_error('no change time')
    except:
        if (timedelta(hours=datetime.now().hour, minutes=datetime.now().minute) >= timedelta(minutes=0,
                                                                                             hours=16) and timedelta(
            hours=datetime.now().hour, minutes=datetime.now().minute) < timedelta(minutes=0, hours=18)):
            return json.what_error('no change time')
    try:
        personal = User.objects.get(username=request.user.username).personal
        req = simplejson.loads(request.body)
        work_area = req['area']
        work_day = req['work_day']
        phone_number = req['phone_number']
        work_number = req['work_number']
        is_save = False
    except:
        return json.post_error
    else:
        if work_area != personal.work_area:
            personal.work_area = work_area
            is_save = True
        if work_day != personal.week_day:
            personal.week_day = work_day
            is_save = True
        if phone_number != personal.phone_number:
            personal.phone_number = phone_number
            is_save = True
        if work_number != personal.work_number:
            personal.work_phone = work_number
            is_save = True
        if is_save:
            personal.save()
            return json.what_success('change success')
        else:
            return json.what_error('no change')


@login_required
def password_change(request):
    try:
        user = User.objects.get(username=request.user.username)
        req = simplejson.loads(request.body)
        if user.check_password(req['old_password']):
            user.set_password(req['new_password'])
            user.save()
        else:
            return json.error
    except:
        return json.post_error
    else:
        return json.what_success('change success')


@login_required
def extra_work_add(request):
    try:
        if Extra_Work.objects.filter(work_number=request.user.username).order_by('id').reverse()[0].status == 0:
            return json.what_error('had extra_work')
    except:
        pass
    try:
        req = simplejson.loads(request.body)
        if datetime.now().date() == datetime.strptime(req['date'], '%Y-%m-%d').date() and timedelta(
                hours=int(datetime.now().hour), minutes=int(datetime.now().minute)) > timedelta(minutes=00,
                                                                                                hours=16) or datetime.now().date() + timedelta(
            days=1) < datetime.strptime(req['date'], '%Y-%m-%d').date() or datetime.now().date() > datetime.strptime(
            req['date'], '%Y-%m-%d').date():
            return json.what_error('time error')
        else:
            new_extra_work = Extra_Work.objects.create(user=User.objects.get(username=request.user.username),
                                                       extra_work_time=req['date'] + ':16.30',
                                                       work_number=request.user.username, status=0, extra_area=''
                                                       , refuse_reason='')
    except:
        return json.post_error
    else:
        new_extra_work.save()
        return json.success({'states': 0, 'registerDay': new_extra_work.extra_work_time})


@login_required
def personal_extra_work_view(request):
    try:
        extra_work = Extra_Work.objects.filter(work_number=request.user.username).order_by('id').reverse()[0]
    except:
        return json.success({'states': '', 'registerDay': '', 'passPlace': ''})
    else:
        if extra_work.status == 0:
            return json.success({'states': 0, 'registerDay': extra_work.extra_work_time})
        elif extra_work.status == 1:
            return json.success(
                {'states': 1, 'passPlace': extra_work.extra_area, 'registerDay': extra_work.extra_work_time})
        else:
            return json.success(
                {'states': 2, 'whyReject': extra_work.refuse_reason, 'registerDay': extra_work.extra_work_time})


@permission_required('work_system.change_announcement')
def extra_work_view(request):
    try:
        extra_work = Extra_Work.objects.filter(status=0)
        extra_work_return = []
        for x in extra_work:
            extra_work_return.append(
                {'id': x.id, 'add_time': x.add_time, 'status': 0, 'extra_work_time': x.extra_work_time,
                 'name': x.user.last_name, 'work_number': x.user.username})
    except:
        return json.error
    else:
        return json.success({'extra_work': extra_work_return})


@permission_required('work_system.change_announcement')
def extra_work_change(request):
    try:
        req = simplejson.loads(request.body)
        extra_work = Extra_Work.objects.get(id=req['id'])
        status = int(req['status'])
        if status == 2:
            extra_work.refuse_reason = req['reason']
        elif status == 1:
            extra_work.extra_area = req['area']
    except:
        return json.post_error
    else:
        if extra_work.status != status:
            extra_work.status = status
            extra_work.save()
            return json.what_success('add success')
        else:
            return json.what_error('no change')


@login_required
def check_in(request):
    wd = User.objects.get(username=request.user.username).personal.week_day
    try:
        ex = Extra_Work.objects.filter(work_number=request.user.username).order_by('id').reverse()[0]
        if (ex.status != 1 or ex.extra_work_time != str(datetime.now().date()) + ':16.30') and wd != int(
                datetime.today().weekday()):
            if wd == 7:
                pass
            else:
                return json.what_error('not check in time')
    except:
        if wd != int(datetime.today().weekday()):
            if wd == 7:
                pass
            else:
                return json.what_error('not check in time')
    try:
        if Check_In.objects.filter(work_number=request.user.username).order_by('id').reverse()[0].check == 0:
            return json.what_error('had been check')
    except:
        pass
    try:
        req = simplejson.loads(request.body)
        toolkit = req['toolkit']
        if toolkit == True:
            check = Check_In.objects.create(work_number=request.user.username, check_in_area=req['area'],
                                            cable=req['cable'], port_module=req['port_module'],
                                            crimping_Tool=req['crimping_Tool'],
                                            screwdriver=req['screwdriver'], crystal_Head=req['crystal_Head'],
                                            switch=req['switch'], taken_toolkit=True,
                                            measuring_line=req['measuring_line'],
                                            user=User.objects.get(username=request.user.username))
            if req['key']:
                check.key = req['key']
            else:
                check.key = False
            if req['hunt']:
                check.hunt = req['hunt']
            else:
                check.hunt = False
            if req['detailed_description']:
                check.detailed_description = req['detailed_description']
        else:
            check = Check_In.objects.create(work_number=request.user.username, check_in_area=req['area'],
                                            taken_toolkit=False, detailed_description='',
                                            cable=False, crimping_Tool=False, switch=False,
                                            crystal_Head=False, measuring_line=False, port_module=False,
                                            key=False, screwdriver=False, check=0,
                                            user=User.objects.get(username=request.user.username))
    except:
        return json.post_error
    else:
        check.save()
        return json.success({'check': True, 'place': check.check_in_area})


@login_required
def check_out(request):
    try:
        req = simplejson.loads(request.body)
        check = Check_In.objects.filter(work_number=request.user.username).order_by('id').reverse()[0]
        if check.taken_toolkit == True:
            check.cable = req['cable']
            check.port_module = req['port_module']
            check.switch = req['switch']
            check.crimping_Tool = req['crimping_Tool']
            check.crystal_Head = req['crystal_Head']
            check.measuring_line = req['measuring_line']
            check.screwdriver = req['screwdriver']

            if req['hunt']:
                check.hunt = req['hunt']
            if req['key']:
                check.key = req['key']
            if req['detailed_description']:
                check.detailed_description = req['detailed_description']
    except:
        return json.post_error
    else:
        check.check = 1
        check.save()
        return json.success({'check': False, 'place': ''})


@login_required
def work_situation_add(request):
    try:
        req = simplejson.loads(request.body)
        work_situation = Work_Situation.objects.create(
            work_area=req['work_area'],
            account_number=req['account_number'],
            telephone_number=req['telephone_number'],
            dormitory_number=req['dormitory_number'],
            status=req['status'],
            introduction=req['introduction'],
            operator=req['operator'],
            situation_order=0
        )
        for who in req['who']:
            work_situation.who_do.add(User.objects.get(username=who))
    except:
        return json.post_error
    else:
        his = History.objects.create(to_id=work_situation.id, to_who=0, who_do=request.user.username,
                                     name=User.objects.get(username=request.user.username).last_name)
        his.record = 'add:work_area=' + work_situation.work_area + ' account_number=' + work_situation.account_number + \
                     ' telephone_number=' + work_situation.telephone_number + ' dormitory_number=' + work_situation.dormitory_number + \
                     ' status=' + str(
            work_situation.status) + ' introduction=' + work_situation.introduction + ' operator=' + work_situation.operator
        for who in req['who']:
            his.who.add(User.objects.get(username=who))
        his.save()
        work_situation.save()
        return json.ok


@login_required
def work_situation_view(request, area):
    try:
        work = Work_Situation.objects.exclude(status=1).filter(work_area=area, situation_order=0)
        work_returns = []
        for x in work:
            work_return = {}
            work_return.update(
                {'id': x.id, 'netAccount': x.account_number, 'repairStatus': x.status,
                 'userPhone': x.telephone_number, 'userHouse': x.dormitory_number, 'userPlace': x.work_area,
                 'repairIntro': x.introduction, 'addTime': x.add_time, 'taskProperty': x.situation_order,
                 'lastChangeTime': x.last_change_time, 'netInfo': x.operator, 'works': []})
            work_returns.append(work_return)
    except:
        return json.error
    else:
        works = []
        a = Check_In.objects.filter(check_in_area=area, check=0)
        for x in a:
            works.append({'work_number': x.work_number, 'name': x.user.last_name, 'phone': x.user.personal.phone_number,
                          'area': area, 'work_phone': x.user.personal.work_phone})
        return json.success({'work_situation': work_returns, 'works': works})


@login_required
def work_situation_change(request):
    try:
        req = simplejson.loads(request.body)
        work_situation = Work_Situation.objects.get(id=req['id'])
        if work_situation.status == 1:
            return json.what_error('Has been completed')
        work_situation.status = req['status']
        work_situation.introduction = req['repairIntro']
        for who in req['who']:
            if User.objects.get(username=who) in work_situation.who_do.all():
                pass
            else:
                work_situation.who_do.add(User.objects.get(username=who))
    except:
        return json.post_error
    else:
        his = History.objects.create()
        his.to_id = work_situation.id
        his.to_who = 0
        his.record = 'change:status=' + str(work_situation.status) + ' introduction=' + work_situation.introduction
        his.who_do = request.user.username
        his.name = User.objects.get(username=request.user.username).last_name
        for who in req['who']:
            his.who.add(User.objects.get(username=who))
        his.save()
        work_situation.save()
        return json.ok


@permission_required('work_system.change_announcement')
def work_order_add(request):
    req = simplejson.loads(request.body)
    work_order = Work_Situation.objects.create(situation_order=req['situation_order'], work_area=req['area'],
                                               account_number=req['account_number'], introduction=req['introduction'],
                                               telephone_number=req['telephone_number'], operator=req['operator'],
                                               dormitory_number=req['dormitory_number'], status=req['status'])
    work_order.who_do.add(User.objects.get(username=request.user.username))

    his = History.objects.create(to_id=work_order.id, to_who=1)
    his.record = 'add:work_area=' + work_order.work_area + ' account_number=' + work_order.account_number + \
                 ' telephone_number=' + work_order.telephone_number + ' dormitory_number=' + work_order.dormitory_number + \
                 ' status=' + str(
        work_order.status) + ' introduction=' + work_order.introduction + ' operator=' + work_order.operator
    his.who_do = request.user.username
    his.name = User.objects.get(username=request.user.username).last_name
    his.who.add(User.objects.get(username=request.user.username))
    his.save()
    work_order.save()
    return json.ok


@login_required
def work_order_change(request):
    try:
        req = simplejson.loads(request.body)
        work_order = Work_Situation.objects.get(id=req['id'])
        if work_order.status == 1:
            json.what_error('Has been completed')
        work_order.status = req['status']
        work_order.introduction = req['introduction']
        for who in req['who']:
            if User.objects.get(username=who) in work_order.who_do.all():
                pass
            else:
                work_order.who_do.add(User.objects.get(username=who))
    except:
        return json.post_error
    else:
        his = History.objects.create()
        his.to_id = work_order.id
        his.to_who = 1
        his.record = 'change:status=' + str(work_order.status) + ' introduction=' + work_order.introduction
        his.who_do = request.user.username
        his.name = User.objects.get(username=request.user.username).last_name
        for who in req['who']:
            his.who.add(User.objects.get(username=who))
        his.save()
        work_order.save()
        return json.ok


@login_required
def work_order_view(request, area, operator):
    try:
        if operator == '投诉':
            work_order = Work_Situation.objects.filter(work_area=area, situation_order=3).exclude(status=1)
        else:
            work_order = Work_Situation.objects.exclude(status=1).filter(work_area=area, operator=operator,
                                                                         situation_order__in=[2, 1])
        work_returns = []
        for x in work_order:
            work_return = {}
            work_return.update(
                {'id': x.id, 'netAccount': x.account_number, 'repairStatus': x.status,
                 'userPhone': x.telephone_number, 'userHouse': x.dormitory_number, 'userPlace': x.work_area,
                 'repairIntro': x.introduction, 'addTime': x.add_time, 'taskProperty': x.situation_order,
                 'lastChangeTime': x.last_change_time, 'netInfo': x.operator})
            work_returns.append(work_return)
    except:
        return json.error
    else:
        works = []
        a = Check_In.objects.filter(check_in_area=area, check=0)
        for x in a:
            works.append({'work_number': x.work_number, 'name': x.user.last_name, 'phone': x.user.personal.phone_number,
                          'area': area, 'work_phone': x.user.personal.work_phone})
        return json.success({'work_order': work_returns, 'works': works})


def get_upload_token(request):
    from .get_qiniu_token import get_qiniu_token
    return JsonResponse({'upload_token': get_qiniu_token()})


@csrf_exempt
def qiniu_callback(request):
    s = str(request.body)
    id = re.search(r'\d+', s)
    b = re.search(r'\..+\'', s)
    hz = b.group(0)
    id = int(id.group(0))
    hz = hz[:-1]
    a = Work_Order_Image.objects.create(to_id=id, url='http://onhei07x4.bkt.clouddn.com/' + str(id) + '_' + str(
        datetime.now()) + hz, work_order=Work_Situation.objects.get(id=id))
    a.save()
    return JsonResponse({'key': str(id) + '_' + str(datetime.now()) + hz,
                         'payload': {'success': 'true',
                                     'url': 'http://onhei07x4.bkt.clouddn.com/' + str(id) + '_' + str(
                                         datetime.now()) + hz}})


@permission_required('work_system.change_announcement')
def inquire(request):
    req = simplejson.loads(request.body)
    inquire_return = []
    model = req['model']
    if model == 1:
        d = datetime.strptime(req['date'], '%Y-%m-%d')
        day = Check_In.objects.filter(check_in_time__gte=d.date()).exclude(
            check_in_time__gte=(d + timedelta(days=1)).date())
        for x in day:
            inquire_return.append({'id': x.user.username, 'name': x.user.last_name, 'check': x.check,
                                   'check_in_time': x.check_in_time, 'check_area': x.check_in_area,
                                   'check_out_time': x.check_out_time, 'taken_toolkit': x.taken_toolkit,
                                   'toolkit': {'detailed_description': x.detailed_description, 'cable': x.cable,
                                               'crimping_Tool': x.crimping_Tool, 'switch': x.switch,
                                               'crystal_Head': x.crystal_Head, 'key': x.key,
                                               'measuring_line': x.measuring_line, 'port_module': x.port_module}})
        return json.success({'inquire': inquire_return})
    elif model == 2:
        s = datetime.strptime(req['start_date'], '%Y-%m-%d')
        e = datetime.strptime(req['end_date'], '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        day = History.objects.filter(time__range=(s, e))
        work = []
        for x in day:
            work.append(x.to_id)
        work = set(work)
        work = Work_Situation.objects.filter(id__in=work)
        done = 0
        undone = 0
        reported = 0
        tomorrow = 0
        for x in work:
            if x.status == 0:
                undone += 1
            elif x.status == 1:
                done += 1
            elif x.status == 2:
                reported += 1
            elif x.status == 3:
                tomorrow += 1
        return json.success({'done': done, 'undone': undone, 'reported': reported, 'tomorrow': tomorrow})
    elif model == 3:
        work = Work_Situation.objects.filter(telephone_number=req['telephone_number'])
        for x in work:
            inquire_returns = {}
            inquire_returns.update(
                {'id': x.id, 'netAccount': x.account_number, 'repairStatus': x.status,
                 'userPhone': x.telephone_number, 'userHouse': x.dormitory_number, 'userPlace': x.work_area,
                 'repairIntro': x.introduction, 'addTime': x.add_time, 'taskProperty': x.situation_order,
                 'lastChangeTime': x.last_change_time, 'netInfo': x.operator, 'history': [], 'person': []})
            for y in x.who_do.all():
                inquire_returns['person'].append({'id': y.username, 'name': y.last_name})
            for z in History.objects.filter(to_id=x.id):
                inquire_returns['history'].append(
                    {'id': z.id, 'work_number': z.who_do, 'time': z.time, 'name': z.name,
                     'record': z.record})
            inquire_return.append(inquire_returns)
        return json.success({'return': inquire_return})
    elif model == 4:
        s = datetime.strptime(req['start_date'], '%Y-%m-%d')
        e = datetime.strptime(req['end_date'], '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        history = History.objects.filter(time__range=(s, e))
        work = []
        for x in history:
            if request.user.username == x.who_do:
                work.append(x.to_id)
        work = set(work)
        work = Work_Situation.objects.filter(id__in=work)
        for a in work:
            inquire_returns = {}
            inquire_returns.update(
                {'id': a.id, 'netAccount': a.account_number, 'repairStatus': a.status,
                 'userPhone': a.telephone_number, 'userHouse': a.dormitory_number, 'userPlace': a.work_area,
                 'repairIntro': a.introduction, 'addTime': a.add_time, 'taskProperty': a.situation_order,
                 'lastChangeTime': a.last_change_time, 'netInfo': a.operator, 'history': [],
                 'person': []})
            for y in a.who_do.all():
                inquire_returns['person'].append({'id': y.username, 'name': y.last_name})
            for z in History.objects.filter(to_id=a.id):
                inquire_returns['history'].append(
                    {'id': z.id, 'work_number': z.who_do, 'time': z.time, 'name': z.name,
                     'record': z.record})
            inquire_return.append(inquire_returns)
        return json.success({'return': inquire_return})
    elif model == 5:
        s = datetime.strptime(req['start_date'], '%Y-%m-%d')
        e = datetime.strptime(req['end_date'], '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        day = History.objects.filter(time__range=(s, e))
        work = []
        for x in day:
            work.append(x.to_id)
        work = set(work)
        work = Work_Situation.objects.filter(id__in=work)
        if req['status'] == 4:
            for x in work:
                inquire_returns = {}
                inquire_returns.update(
                    {'id': x.id, 'netAccount': x.account_number, 'repairStatus': x.status,
                     'userPhone': x.telephone_number, 'userHouse': x.dormitory_number, 'userPlace': x.work_area,
                     'repairIntro': x.introduction, 'addTime': x.add_time, 'taskProperty': x.situation_order,
                     'lastChangeTime': x.last_change_time, 'netInfo': x.operator, 'history': [], 'person': []})
                for y in x.who_do.all():
                    inquire_returns['person'].append({'id': y.username, 'name': y.last_name})
                for z in History.objects.filter(to_id=x.id):
                    inquire_returns['history'].append(
                        {'id': z.id, 'work_number': z.who_do, 'time': z.time, 'name': z.name,
                         'record': z.record})
                inquire_return.append(inquire_returns)
        else:
            for x in work:
                inquire_returns = {}
                if x.status == req['status']:
                    inquire_returns.update(
                        {'id': x.id, 'netAccount': x.account_number, 'repairStatus': x.status,
                         'userPhone': x.telephone_number, 'userHouse': x.dormitory_number, 'userPlace': x.work_area,
                         'repairIntro': x.introduction, 'addTime': x.add_time, 'taskProperty': x.situation_order,
                         'lastChangeTime': x.last_change_time, 'netInfo': x.operator, 'history': [], 'person': []})
                    for y in x.who_do.all():
                        inquire_returns['person'].append({'id': y.username, 'name': y.last_name})
                    for z in History.objects.filter(to_id=x.id):
                        inquire_returns['history'].append(
                            {'id': z.id, 'work_number': z.who_do, 'time': z.time, 'name': z.name,
                             'record': z.record})
                    inquire_return.append(inquire_returns)
        return json.success({'return': inquire_return})


@login_required
def person_today(request):
    persons = []
    s = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')
    e = s + timedelta(hours=23, minutes=59, seconds=59)
    history = History.objects.filter(time__range=(s,e))
    work = []
    for x in history:
        if request.user.username == x.who_do:
            work.append(x.to_id)
    work = set(work)
    work = Work_Situation.objects.filter(id__in=work)
    for x in work:
        person = {}
        person.update({'id': x.id, 'netAccount': x.account_number, 'repairStatus': x.status,
                       'userPhone': x.telephone_number, 'userHouse': x.dormitory_number, 'userPlace': x.work_area,
                       'repairIntro': x.introduction, 'addTime': x.add_time, 'taskProperty': x.situation_order,
                       'lastChangeTime': x.last_change_time, 'netInfo': x.operator, 'history': []})
        for y in History.objects.filter(to_id=x.id):
            person['history'].append(
                {'id': y.id, 'time': y.time, 'record': y.record, 'who_do': y.who_do, 'name': y.name})
        persons.append(person)
    return json.success({'persons': persons})


@login_required
def view_today(request):
    req = simplejson.loads(request.body)
    view = []
    work = Work_Situation.objects.filter(work_area=req['area']).exclude(status=1)
    for x in work:
        view.append({'id': x.id, 'netAccount': x.account_number, 'repairStatus': x.status,
                     'userPhone': x.telephone_number, 'userHouse': x.dormitory_number, 'userPlace': x.work_area,
                     'repairIntro': x.introduction, 'addTime': x.add_time, 'taskProperty': x.situation_order,
                     'lastChangeTime': x.last_change_time, 'netInfo': x.operator})
    return json.success({'today': view})


@login_required
def experience_view(request):
    ex = Experience.objects.all().order_by('id').reverse()
    exs = []
    for e in ex:
        exs.append(
            {'name': e.name, 'id': e.id, 'number': e.who_do, 'time': e.time, 'record': e.record, 'title': e.title})
    return json.success({'experience': exs})


@login_required
def experience_add(request):
    try:
        req = simplejson.loads(request.body)
        who = Personal.objects.get(work_number=request.user.username)
        ex = Experience.objects.create(name=who.name, who_do=request.user.username, record=req['experience'],
                                       title=req['title'])
    except:
        return json.error
    else:
        ex.save()
        return json.success(
            {'experience': {'name': ex.name, 'id': ex.id, 'number': ex.who_do, 'time': ex.time, 'record': ex.record,
                            'title': ex.title}})
