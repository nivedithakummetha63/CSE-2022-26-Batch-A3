from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import os
from .models import ChatRoom, Message, BlockedUser, UserReport
@login_required
def chat_home(request):
    blocked_users = BlockedUser.objects.filter(blocker=request.user).values_list('blocked_id', flat=True)
    rooms = ChatRoom.objects.filter(users=request.user).exclude(users__in=blocked_users).distinct()
    chat_rooms = []
    for room in rooms:
        other_user = room.users.exclude(id=request.user.id).first()
        if other_user:
            chat_rooms.append({
                'id': room.id,
                'other_user': other_user
            })
    return render(request, 'chat/chat_home.html', {
        'rooms': chat_rooms
    })
@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Check if user is blocked
    if BlockedUser.objects.filter(blocker=other_user, blocked=request.user).exists():
        return redirect('chat_home')

    # Check if room already exists between both users
    room = ChatRoom.objects.filter(users=request.user)\
                           .filter(users=other_user)\
                           .first()

    if not room:
        room = ChatRoom.objects.create()
        room.users.add(request.user, other_user)

    return redirect('chat_room', room_id=room.id)


# ------------------ CHAT ROOM ------------------
@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)

    # Check if user is part of this room
    if request.user not in room.users.all():
        return redirect('chat_home')

    # Find the other user in the room
    other_user = room.users.exclude(id=request.user.id).first()

    # Check if other user has blocked current user
    if BlockedUser.objects.filter(blocker=other_user, blocked=request.user).exists():
        return redirect('chat_home')

    messages = room.messages.all().order_by('timestamp')

    if request.method == "POST":
        content = request.POST.get('message', '').strip()
        file = request.FILES.get('file')
        
        if content or file:
            message = Message.objects.create(
                room=room,
                sender=request.user,
                content=content if content else '',
                message_type='file' if file else 'text',
                file=file if file else None
            )
        
        return redirect('chat_room', room_id=room.id)

    # Check if current user has blocked the other user
    is_blocked = BlockedUser.objects.filter(blocker=request.user, blocked=other_user).exists()

    return render(request, 'chat/chat_room.html', {
        'room': room,
        'messages': messages,
        'other_user': other_user,
        'is_blocked': is_blocked
    })


# ------------------ BLOCK USER ------------------
@login_required
@require_POST
def block_user(request, user_id):
    try:
        user_to_block = get_object_or_404(User, id=user_id)
        
        # Don't allow blocking yourself
        if user_to_block == request.user:
            return JsonResponse({'success': False, 'error': 'Cannot block yourself'})
        
        # Create or get existing block
        blocked_user, created = BlockedUser.objects.get_or_create(
            blocker=request.user,
            blocked=user_to_block
        )
        
        return JsonResponse({'success': True, 'blocked': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ------------------ UNBLOCK USER ------------------
@login_required
@require_POST
def unblock_user(request, user_id):
    try:
        user_to_unblock = get_object_or_404(User, id=user_id)
        
        # Remove block if exists
        BlockedUser.objects.filter(
            blocker=request.user,
            blocked=user_to_unblock
        ).delete()
        
        return JsonResponse({'success': True, 'blocked': False})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ------------------ REPORT USER ------------------
@login_required
@require_POST
def report_user(request, user_id):
    try:
        data = json.loads(request.body)
        reason_text = data.get('reason', '').strip()
        
        if not reason_text:
            return JsonResponse({'success': False, 'error': 'Reason is required'})
        
        user_to_report = get_object_or_404(User, id=user_id)
        
        # Don't allow reporting yourself
        if user_to_report == request.user:
            return JsonResponse({'success': False, 'error': 'Cannot report yourself'})
        
        # Create report
        report = UserReport.objects.create(
            reporter=request.user,
            reported_user=user_to_report,
            reason='other',  # Default to 'other' since we're getting free text
            description=reason_text
        )
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ------------------ FILE DOWNLOAD ------------------
@login_required
def download_file(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user has access to this message
    if request.user not in message.room.users.all():
        return redirect('chat_home')
    
    if message.file:
        response = HttpResponse(message.file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{message.file_name}"'
        return response
    
    return redirect('chat_home')
