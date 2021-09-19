from django.forms import ModelForm
from core.models import ChatUser


class NicknameForm(ModelForm):
    class Meta:
        model = ChatUser
        fields = ['nickname']
