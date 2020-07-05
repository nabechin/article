from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'messages'
router = DefaultRouter()
router.register('message',views.SendMessageView)

urlpatterns = [
    path('',views.TalkRoomView.as_view(),name='talkroom'),
    path('<int:talkroom>',views.MessageView.as_view(),name="message"),
    path('',include(router.urls)),
]