from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom {self.id}"


class Message(models.Model):
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('file', 'File'),
        ('image', 'Image'),
    ]
    
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.message_type == 'text':
            return f"{self.sender.username}: {self.content[:20]}"
        else:
            return f"{self.sender.username}: [File: {self.file.name}]"

    @property
    def file_size(self):
        if self.file:
            return self.file.size
        return 0

    @property
    def file_name(self):
        if self.file:
            return self.file.name.split('/')[-1]
        return ""


class BlockedUser(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"


class UserReport(models.Model):
    REPORT_REASONS = [
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('inappropriate', 'Inappropriate Content'),
        ('fake', 'Fake Profile'),
        ('other', 'Other'),
    ]
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received')
    reason = models.CharField(max_length=20, choices=REPORT_REASONS, default='other')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reporter.username} reported {self.reported_user.username}"
