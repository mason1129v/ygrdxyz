from django.contrib import admin
from chat.models import *
# Register your models here.

class MessAdmin(admin.ModelAdmin):
    list_display =('MID','MCont')
    ordering = ('MID',)

admin.site.register(messbrd, MessAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display =('MID','MAC')
    ordering = ('MID',)

admin.site.register(member, MemberAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display =('PID','PName', 'PDetail')
    ordering = ('PID',)
admin.site.register(product, ProductAdmin)