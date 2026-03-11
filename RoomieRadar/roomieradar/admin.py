from django.contrib import admin
from django.contrib.auth.models import User
from chat.models import BlockedUser, UserReport
from base.models import Profile


class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['user_count'] = User.objects.count()
        extra_context['profile_count'] = Profile.objects.count()
        extra_context['blocked_count'] = BlockedUser.objects.count()
        extra_context['report_count'] = UserReport.objects.count()
        return super().index(request, extra_context)

admin.site.__class__ = CustomAdminSite
