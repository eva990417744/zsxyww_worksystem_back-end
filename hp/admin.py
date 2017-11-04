from django.contrib import admin

# Register your models here.
from .models import HP, DeBuff, Buff, Personal

admin.site.register(HP)
admin.site.register(DeBuff)
admin.site.register(Buff)
admin.site.register(Personal)
