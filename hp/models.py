from django.db import models
from work_system.models import Personal
from django.contrib.auth.models import User

# Create your models here.


'''
class Personal(models.Model):
    user = models.OneToOneField(User, null=True)
    work_number = models.CharField(default=0, max_length=10)
    work_area = models.CharField(max_length=30, null=True)
    week_day = models.IntegerField(default=0)
    phone_number = models.CharField(default=911, max_length=20)
    name = models.CharField(default=0, max_length=30)
    work_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
'''


class Summary:
    Buff_Lv = ('工作积极', '表现良好', '加班', '态度积极', '贡献想法')
    DeBuff_Lv1 = ('值班没带工作证', '遗漏报修', '工单超时', '私活影响值班', '不签到', '值班联系不上', 'Other1')
    DeBuff_Lv2 = ('不接电话', '工单被投诉', '不回短信', '旷工', '不能单刷',
                     '对女生言行不当', '私自以网维名义发布消息', '查到路由不反映', '攻击网络',
                     '使用路由器影响正常上网',
                     '态度消极', '泄露资料', '被教职员工投诉', 'Other2')
    DeBuff_Lv3 = ('认知不清', '泄露私人号码', '借出工作证', '丢失工作证',
                     '宣传路由', '出售IP', '分裂', 'Other3')


class HP(models.Model):
    user = models.OneToOneField(User, null=False)
    value = models.IntegerField(default=50)
    add_time = models.DateTimeField(auto_now_add=True)
    change_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username+' HP:'+str(self.value)

    def debuff(self, buff_name):
        q = DeBuff.objects.filter(name="%s" % buff_name)
        return q

    def buff(self, buff_name):
        q = DeBuff.objects.filter(name="%s" % buff_name)
        return q

    #class Meta:
        #app_label = 'hp'



class DeBuff(models.Model):
    key = models.ForeignKey(HP)

    debuff_summary = (
        ('Level1', (
            ('没带工作证', '没带工作证'),
            ('遗漏报修', '遗漏报修'),
            ('工单超时', '工单超时'),
            ('私活影响值班', '私活影响值班'),
            ('不签到', '不签到'),
            ('值班联系不上', '值班联系不上'),
            ('Other1', 'Other'),
        ),
         ),
        ('Level2', (
            ('不接电话', '不接电话'),
            ('工单被投诉', '工单被投诉'),
            ('不回短信', '不回短信'),
            ('旷工', '旷工'),
            ('不能单刷', '不能单刷'),
            ('对女生言行不当', '对女生言行不当'),
            ('私自以网维名义发布消息', '私自以网维名义发布消息'),
            ('查到路由不反映', '查到路由不反映'),
            ('攻击网络', '攻击网络'),
            ('使用路由器影响正常上网', '使用路由器影响正常上网'),
            ('态度消极', '态度消极'),
            ('泄露资料', '泄露资料'),
            ('被教职员工投诉', '被教职员工投诉'),
            ('Other2', 'Other2')
        )
         ),
        ('Level3', (
            ('认知不清', '认知不清'),
            ('泄露私人号码', '泄露私人号码'),
            ('借出工作证', '借出工作证'),
            ('丢失工作证', '丢失工作证'),
            ('宣传路由', '宣传路由'),
            ('出售IP', '出售IP'),
            ('分裂', '分裂'),
            ('Other3', 'Other3')
        )
         )
    )

    debuff_reason = models.CharField(choices=debuff_summary, max_length=150)
    debuff_details = models.CharField(max_length=150,default='none',blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    hp_decrease = models.IntegerField(default=10)

    def __str__(self):
        return self.debuff_reason

    def delete(self, *args, **kwargs):
        q = self.key
        if self.debuff_reason in Summary.DeBuff_Lv1:
            q.value += 10
        elif self.debuff_reason in Summary.DeBuff_Lv2:
            q.value += 20
        elif self.debuff_reason in Summary.DeBuff_Lv3:
            q.value += 30
        q.save()
        super(DeBuff, self).delete(*args, **kwargs)

    #class Meta:
        #app_label = 'DeBuff'


class Buff(models.Model):
    key = models.ForeignKey(HP)

    buff_summary = (
        ('工作积极', '工作积极'),
        ('表现良好', '表现良好'),
        ('加班', '加班'),
        ('态度积极', '态度积极'),
        ('贡献想法', '贡献想法')
    )

    add_time = models.DateTimeField(auto_now_add=True)
    buff_reason = models.CharField(choices=buff_summary, max_length=150)
    buff_details = models.CharField(max_length=150, default='none', blank=True)
    hp_increase = models.IntegerField(default=5)

    def delete(self, *args, **kwargs):
        q = self.key
        q.value -= 5
        q.save()
        super(Buff, self).delete(*args, **kwargs)

    def __str__(self):
        return self.buff_reason

    #class Meta:
        #app_label = 'Buff'
