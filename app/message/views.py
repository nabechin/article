from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlencode
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TalkRoom, Message, UserOwnTalkRoom
from .serializers import MessageSerializer
from rest_framework import permissions, viewsets


class TalkRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'message.html'

    def get(self,request,*args,**kwargs):
        login_user_id = self.request.user.id
        talk_rooms = UserOwnTalkRoom.objects.all().filter(participant=login_user_id).values('talk_room')
        talk_rooms = UserOwnTalkRoom.objects.all().filter(talk_room__in=talk_rooms).exclude(participant=login_user_id)
        context = super(TalkRoomView,self).get_context_data(**kwargs)
        context['talk_rooms'] = talk_rooms
        context['login_user_id'] = login_user_id
        return render(self.request,self.template_name,context)


class MessageView(LoginRequiredMixin, TemplateView):
    template_name = 'message.html'

    def get(self,request,*args,**kwargs):
        talk_room_id = kwargs['talkroom']
        login_user_id = self.request.user.id
        messages = Message.objects.all().filter(talk_room=talk_room_id)
        talk_rooms = UserOwnTalkRoom.objects.all().filter(participant=login_user_id).values('talk_room')
        talk_rooms = UserOwnTalkRoom.objects.all().filter(talk_room__in=talk_rooms).exclude(participant=login_user_id)
        context = super(MessageView,self).get_context_data(**kwargs)
        context['talk_rooms'] = talk_rooms
        context['login_user_id'] = login_user_id
        context['messages'] = messages
        context['talkroom'] = talk_room_id
        return render(self.request,self.template_name,context)


class UserOwnTalkRoomView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        login_user = self.request.user
        talk_rooms = UserOwnTalkRoom.objects.all().filter(participant=login_user.id).values('talk_room')
        talk_rooms = UserOwnTalkRoom.objects.all().filter(talk_room__in=talk_rooms,participant=kwargs['sender'])
        if not talk_rooms:
            talk_room = TalkRoom.objects.create(last_message='')
            UserOwnTalkRoom.objects.create(participant=login_user,talk_room=talk_room)
            sender = get_user_model().objects.get(pk=kwargs['sender'])
            UserOwnTalkRoom.objects.create(participant=sender,talk_room=talk_room)
        else:
            talk_room = talk_rooms[0]
        return reverse('messages:message',args=(talk_room.id,))


class SendMessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def get_queryset(self):
        queryset = self.queryset
        talk_room_id = self.request.query_params.get('talkroom')
        if talk_room_id:
            queryset = queryset.filter(talk_room=talk_room_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    






