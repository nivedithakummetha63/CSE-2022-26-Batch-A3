from django.contrib import admin
from .models import ChatRoom, Message, BlockedUser, UserReport


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_users', 'created_at']
    search_fields = ['users__username']
    list_filter = ['created_at']
    filter_horizontal = ['users']
    
    def get_users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    get_users.short_description = 'Users'


@admin.register(BlockedUser)
class BlockedUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'blocker', 'blocked', 'created_at']
    list_filter = ['created_at']
    search_fields = ['blocker__username', 'blocked__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Block Information', {
            'fields': ('blocker', 'blocked', 'created_at')
        }),
    )


@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'reporter', 'reported_user', 'reason', 'is_resolved', 'created_at']
    list_filter = ['reason', 'is_resolved', 'created_at']
    search_fields = ['reporter__username', 'reported_user__username', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('reporter', 'reported_user', 'created_at')
        }),
        ('Report Details', {
            'fields': ('reason', 'description', 'is_resolved')
        }),
    )
    
    actions = ['mark_as_resolved', 'mark_as_unresolved']
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
        self.message_user(request, f"{queryset.count()} reports marked as resolved.")
    mark_as_resolved.short_description = "Mark selected reports as resolved"
    
    def mark_as_unresolved(self, request, queryset):
        queryset.update(is_resolved=False)
        self.message_user(request, f"{queryset.count()} reports marked as unresolved.")
    mark_as_unresolved.short_description = "Mark selected reports as unresolved"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'room', 'message_type', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['sender__username', 'content']
    readonly_fields = ['timestamp']
