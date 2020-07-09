from django.urls import path

from . import views


app_name = 'messages'

urlpatterns = [
    path('', views.TalkRoomView.as_view(), name='talkroom'),
    path('<int:talkroom>', views.MessageView.as_view(), name="message"),
    path('talkroom/<int:sender>',
         views.UserOwnTalkRoomView.as_view(), name='talkroom'),
]
