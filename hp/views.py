from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import *
from operator import attrgetter
from django.contrib.auth.decorators import permission_required
from itertools import chain
# Create your views here.


@permission_required('work_system.change_extra_work')
def index(request):
    hp_list = get_list_or_404(HP.objects.all())
    hp_list.sort(key=attrgetter('value'), reverse=True)
    return render(request, 'hp/index.html', {'hp_list': hp_list})

@permission_required('work_system.change_extra_work')
def details(request, work_number):
    tempUser = User.objects.filter(username=work_number)
    member_name = get_object_or_404(Personal.objects.filter(user = tempUser)).name
    member_hp = get_object_or_404(HP.objects.filter(user=tempUser))
    member_debuffs = DeBuff.objects.filter(key=member_hp)
    member_buffs = Buff.objects.filter(key=member_hp)
    member_all_buffs = list(chain(member_debuffs, member_buffs))
    member_all_buffs.sort(key=attrgetter('add_time'), reverse=True)
    return render(request, 'hp/details.html', {'member_hp': member_hp, 'all_buffs': member_all_buffs, 'member_name':member_name})
