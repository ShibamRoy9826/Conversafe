########## Libraries and Stuff ################################################
from django.contrib import admin
from django.urls import path,include
# All views for the routes
from landing import views as landingView
from notification import views as notificationView
from core import views as mainView
from chat import views as chatView
from AIChat import views as AIView
from friends import views as friendView
from django.conf import settings # settings
from django.conf.urls.static import static 
##############################################################################

urlpatterns = [
	path('admin/', admin.site.urls),
	path('',landingView.landing,name="landing"),
	path("login/",landingView.Login, name="login"),
	path("signup/",landingView.signup, name="signup"),

	# Auth
	path('verification/', include('verify_email.urls')),
	path('resetPassword/<uidb64>/<token>', landingView.resetPass, name='resetPassword'),
	path("forgot-password/",landingView.forgotPassword,name="resetPassword"),
 
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

	# Login required
	path('home/',mainView.home,name="home"),
	path('profile/',mainView.profile,name="profile"),
	path('friends/',friendView.friends,name="friends"),
	path('notifications/',mainView.notifications,name="notifications"),
	path('contact/',mainView.contact,name="contact"),
	path('feedback/',mainView.feedback,name="feedback"),
	path('editProfile/',mainView.editProfile,name="edit_profile"),
	path('events/',mainView.events, name="events"),
	path('settings/',mainView.settings,name="settings"),
	path("logout/",mainView.logOut,name="logout"),

	path('startQuiz/',mainView.startQuiz,name="quiz"),
	path('startVocab/',mainView.startVocab,name="vocab_quiz"),
	path('wordSearch/',mainView.wordSearch,name="vocab_quiz"),

	# Chat
	# path('rooms/',chatView.rooms,name="roomList"), # Only for debugging
	path('chat/<slug:slug>/',chatView.room,name="chatRoom"),
	path('findRoom/',chatView.findRoom,name="findRoom"),
	path('privateRoomMenu/',chatView.privateRoomCreator,name="privateRoomMenu"),                                            
	path('chat/<slug:slug>/',chatView.room,name="chatRoom"),  
	path('chat/private/<slug:slug>/',chatView.roomJoinPrivate,    name="chatRoomPrivate"),                                      
	path('createPrivateRoom/',chatView.createPrivateRoom,name=    "chatRoomCreatePrivate"),                                     
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
