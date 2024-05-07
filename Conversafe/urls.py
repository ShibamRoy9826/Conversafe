"""
URL configuration for Conversafe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from landing import views as landingView
from notification import views as notificationView
from core import views as mainView
from chat import views as chatView
from AIChat import views as AIView
from friends import views as friendView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',landingView.landing,name="landing"),
    path("login/",landingView.Login, name="login"),
    path("signup/",landingView.signup, name="signup"),

    # Auth
    path('verification/', include('verify_email.urls')),
    path('resetPassword/<uidb64>/<token>', landingView.resetPass, name='resetPassword'),
    path("forgot-password/",landingView.forgotPassword,name="resetPassword"),
    
    # path("temp/",landingView.temp,name="temp"),
    # Auth reload
    path("__reload__/", include("django_browser_reload.urls")),


    # Login required
    path('home/',mainView.home,name="home"),

    # User Profiles
    path('profile/',mainView.profile,name="profile"),
    path('profile/<username>/',mainView.profileSpecific,name="profileSpecific"),

    # Friends
    path('sendFriendRequest/',friendView.sendFriendRequest,name="sendFriendRequest"),
    path('unFriend/',friendView.unFriend,name="unFriend"),
    path('cancelRequest/',friendView.CancelRequest,name="cancelRequest"),
    path('acceptReq/',friendView.AcceptRequest,name="cancelRequest"),
    path('declineReq/',friendView.DeclineRequest,name="cancelRequest"),
    path('searchUsers/',friendView.searchPeople,name="searchUsers"),



    path('friends/',friendView.friends,name="friends"),
    path('notifications/',mainView.notifications,name="notifications"),
    # path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('contact/',mainView.contact,name="contact"),
    path('feedback/',mainView.feedback,name="feedback"),
    path('editProfile/',mainView.editProfile,name="edit_profile"),
    # path('events/',mainView.events,name="events"),
    path('events/',mainView.events, name="events"),
    path('settings/',mainView.settings,name="settings"),
    path("logout/",mainView.logOut,name="logout"),

    # Fun Quiz
    path('startQuiz/',mainView.startQuiz,name="quiz"),


    # Chat
    # path('rooms/',chatView.rooms,name="roomList"),
    path('privateRoomMenu/',chatView.privateRoomCreator,name="privateRoomMenu"),
    path('chat/<slug:slug>/',chatView.room,name="chatRoom"),
    path('chat/private/<slug:slug>/',chatView.roomJoinPrivate,name="chatRoomPrivate"),
    path('createPrivateRoom/',chatView.createPrivateRoom,name="chatRoomCreatePrivate"),
    path('findRoom/',chatView.findRoom,name="findRoom"),

    # ChatWithAI
    path('chatWithAI/<slug:slug>/',AIView.AIConnect,name="AIRoomConnect"),
    path('createAIChat/',AIView.chatWithAI,name="AIChat"),

    # Deleting Notifications
    path('deleteNotif/',notificationView.deleteNotif,name="deleteNotification")


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# handler404 = 'landing.views.error404'
