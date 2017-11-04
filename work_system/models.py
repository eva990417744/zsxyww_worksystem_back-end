from django.db import models
from django.contrib.auth.models import User


class Announcement(models.Model):
    notice_content = models.CharField(max_length=200, default='none')

    def __str__(self):
        return self.notice_content


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


class Extra_Work(models.Model):
    user = models.ForeignKey(User, null=True)
    work_number = models.CharField(max_length=10, default=0)
    extra_area = models.CharField(max_length=20, default='')
    status = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)
    extra_work_time = models.CharField(max_length=30, default=None)
    refuse_reason = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.work_number + str(self.add_time)


class Check_In(models.Model):
    user = models.ForeignKey(User, null=True)
    work_number = models.CharField(default=0, max_length=10)
    taken_toolkit = models.BooleanField(default=True)
    check = models.IntegerField(default=0)
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(auto_now=True)
    check_in_area = models.CharField(max_length=20)

    detailed_description = models.CharField(max_length=200, null=True)
    cable = models.BooleanField(default=True)
    crimping_Tool = models.BooleanField(default=True)
    switch = models.BooleanField(default=True)
    crystal_Head = models.BooleanField(default=True)
    measuring_line = models.BooleanField(default=True)
    port_module = models.BooleanField(default=True)
    key = models.BooleanField(default=False)
    screwdriver = models.BooleanField(default=True)
    hunt = models.BooleanField(default=False)

    def __str__(self):
        return self.work_number + str(self.check_in_time)


class Work_Situation(models.Model):
    who_do = models.ManyToManyField(User)
    add_time = models.DateTimeField(auto_now_add=True)
    last_change_time = models.DateTimeField(auto_now=True)
    work_area = models.CharField(max_length=20)
    account_number = models.CharField(max_length=20, null=True)
    telephone_number = models.CharField(max_length=20)
    dormitory_number = models.CharField(max_length=20)
    status = models.IntegerField(default=0)
    introduction = models.CharField(blank=True, default=None, max_length=200)
    situation_order = models.IntegerField(default=0)
    operator = models.CharField(default=None, max_length=200, null=True)

    def __str__(self):
        return str(self.id)+'_' +self.work_area + str(self.add_time)


class Work_Order_Image(models.Model):
    work_order = models.ForeignKey(Work_Situation)
    to_id = models.IntegerField(default=0)
    url = models.URLField(max_length=200)

    def __str__(self):
        return str(self.to_id)


class History(models.Model):
    who = models.ManyToManyField(User)
    to_id = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    record = models.CharField(max_length=400)
    to_who = models.IntegerField(default=0)
    who_do = models.CharField(max_length=400, null=True)
    name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.to_id) + '_' + self.name + '_' + str(self.time)


class Experience(models.Model):
    name = models.CharField(max_length=20)
    who_do = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    record = models.CharField(max_length=400)
    title = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.title + '_' + self.name
