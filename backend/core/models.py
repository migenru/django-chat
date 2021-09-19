import random
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models


def generate_font_color():
    color_rgb = tuple([random.randint(0, 128) for i in range(3)])
    return "#{0:02x}{1:02x}{2:02x}".format(*color_rgb)


class ChatUser(models.Model):
    nickname = models.CharField(max_length=255, blank=False)
    font_color = models.CharField(max_length=7, blank=False, editable=False)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return self.nickname


@receiver(pre_save, sender=ChatUser)
def my_callback(sender, instance, *args, **kwargs):
    instance.font_color = generate_font_color()



class ChatMessage(models.Model):
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)

    class Meta:
        ordering = ['-timestamp']
