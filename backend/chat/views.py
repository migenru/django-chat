from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NicknameForm

from core.models import ChatMessage, ChatUser


def index(request):
    if request.method == 'POST':
        form = NicknameForm(request.POST)
        if form.is_valid():
            print('valid')
            nickname = form.cleaned_data['nickname']
            new_user = ChatUser()
            new_user.nickname = nickname
            new_user.save()
            request.session['user_id'] = new_user.pk
            request.session['user_nickname'] = new_user.nickname
            return HttpResponseRedirect('/chat/main/')

    else:
        form = NicknameForm()

    return render(request, 'chat/index.html', {'form': form})


def room(request, room_name):
    messages = ChatMessage.objects.all().order_by('timestamp')
    try:
        context = {
            'massages': messages,
            'room_name': room_name,
            'user_nickname': request.session['user_nickname'],
            'user_id': request.session['user_id']
        }
    except Exception as e:
        print(e)
        return render(request, 'chat/return.html')
    return render(request, 'chat/room.html', context)
