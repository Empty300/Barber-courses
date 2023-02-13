from django.contrib import admin

from users.models import User, EmailVerification


@admin.register(User)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('username', 'status', 'date_joined')
    fields = ('id', 'username', 'email', 'status', 'date_joined', 'is_verified_email')
    readonly_fields = ('id', 'date_joined')

@admin.register(EmailVerification)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user',)
    fields = ('user', 'code')

