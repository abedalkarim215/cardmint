from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils import timezone

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ['username', 'email', 'subscription', 'approved', 'subscribed_on', 'is_active']
    list_filter = ['approved', 'subscription', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']

    fieldsets = UserAdmin.fieldsets + (
        ('Subscription Info', {
            'fields': ('subscription', 'approved', 'subscribed_on'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Subscription Info', {
            'fields': ('subscription',),
        }),
    )

    actions = ['approve_selected_users']

    def approve_selected_users(self, request, queryset):
        for user in queryset:
            user.approved = True
            user.subscribed_on = timezone.now()
            user.save()
    approve_selected_users.short_description = "✅ الموافقة على المستخدمين المحددين"

admin.site.register(CustomUser, CustomUserAdmin)
