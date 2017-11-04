from work_system.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(Announcement)
admin.site.register(Check_In)
admin.site.register(Work_Situation)
admin.site.register(History)
admin.site.register(Extra_Work)
admin.site.register(Work_Order_Image)
admin.site.register(Experience)

class PersonalInline(admin.StackedInline):
    model = Personal
    can_delete = False
    verbose_name_plural = 'Personal'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (PersonalInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
