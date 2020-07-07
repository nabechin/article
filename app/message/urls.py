from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


app_name = 'messages'
router = DefaultRouter()
router.register('message', views.SendMessageView)

urlpatterns = [
    path('', views.TalkRoomView.as_view(), name='talkroom'),
    path('<int:talkroom>', views.MessageView.as_view(), name="message"),
    path('talkroom/<int:sender>',
         views.UserOwnTalkRoomView.as_view(), name='talkroom'),
    path('', include(router.urls)),
]
