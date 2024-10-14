from django.shortcuts import render, redirect, get_object_or_404
from chatapp.models import Chat, Message
from accounts.models import User

def chat_list(request):
    chats = Chat.objects.filter(participants=request.user)
    return render(request, 'chat/chat_list.html', {'chats': chats})


def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = Message.objects.filter(chat=chat).order_by('timestamp')

    if request.method == 'POST':
        message_text = request.POST.get('message')
        author = request.user
        message = Message.objects.create(chat=chat, author=author, message=message_text)
        return redirect('chat_detail', chat_id=chat_id)
    return render(request, 'chat/chat_detail.html', {'chat': chat, 'messages': messages})

def chat_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        participant_ids = request.POST.getlist('participants')
        participants = User.objects.filter(id__in=participant_ids)
        chat = Chat.objects.create(name=name)
        chat.participants.add(request.user, *participants)
        return redirect('chat_detail', chat_id=chat.id)
    users = User.objects.exclude(id=request.user.id)


    return render(request, 'chat/chat_create.html', {'users': users})