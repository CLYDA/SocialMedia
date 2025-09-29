from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    list_display=[ 'username', 'email', 'first_name', 'last_name','date_of_birth', 'job', 'phone']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('date_of_birth','bio', 'photo', 'job', 'phone')}),
    )

def make_deactivation(modeladmin, request, queryset):
    result = queryset.update(active = False)
    modeladmin.message_user(request, f'{result} post deactivated successfully')
 
make_deactivation.short_description = "رد پست انتخاب شده"


def make_activation(modeladmin, request, queryset):
    result = queryset.update(active = True)
    modeladmin.message_user(request, f'{result} post Actived successfully')
 
make_activation.short_description = "تایید پست انتخاب شده"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'created','description']
    ordering = ['created']
    search_fields = ['description']
    actions = [make_deactivation,make_activation ]
