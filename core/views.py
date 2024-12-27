###  Libraries and stuff ############################################################
from random import choice
## For the quiz
from sqlite3 import connect

from django.conf import settings as django_set
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from requests import get

from friends.models import *
# Some model objects
from landing import models
from landing.models import AUser
from notification.utils import *  # For notifications

from .models import LearningSource, UserProfile

######################################################################

# Home/Dashboard page
@login_required(login_url="login")
def home(request):
    context={}
    user = AUser.objects.get(pk=request.user.pk)
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    context["langtolearn"]=user_profile.learn_lang
    return render(request,"main/dashboard.html",context)

# Profile view
@login_required(login_url="login")
def profile(request):
    context={}
    user = AUser.objects.get(pk=request.user.pk)
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    context["langtolearn"]=user_profile.learn_lang
    return render(request,"main/func/profile.html",context)

# A Specific profile -> Other user's profile
@login_required(login_url="login")
def profileSpecific(request,username):
    context={}
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    context['isFriend']=False
    context['friendRequestPending']=False
    
    user = AUser.objects.get(pk=request.user.pk)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    context["langtolearn"]=user_profile.learn_lang

    otherUser=AUser.objects.get(username=username)
    userFriendList=FriendList.objects.get(user=request.user)

    if userFriendList.isFriend(otherUser):
        context['isFriend']=True
    elif FriendRequest.objects.filter(sender=request.user, receiver=otherUser, isActive=True):
        context['friendRequestPending']=True
    try:
        context['profile']=UserProfile.objects.get(user_url=username)
    except Exception as e:
        print(e)
        
    return render(request,"main/func/profileSpecific.html",context)

# Edit own profile
@login_required(login_url="login")
def editProfile(request):
    context={}
    user = AUser.objects.get(pk=request.user.pk)

    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    context["langtolearn"]=user_profile.learn_lang

    if request.method=="POST":
        displayName=request.POST.get("display_name")
        shortDescription=request.POST.get("short_bio")
        longDescription=request.POST.get("long_bio")
        gender=request.POST.get("gender")
        user_profile = UserProfile.objects.get(user=user)

        if request.FILES.get('avatar'):
            avatar_file = request.FILES['avatar']
            user_profile.avatar.save(avatar_file.name, avatar_file)
        if displayName!=None:
            user_profile.display_name = displayName
        if shortDescription!=None:
            user_profile.short_bio = shortDescription
        if longDescription!=None:
            user_profile.long_bio = longDescription
        if gender!=None:
            user_profile.gender=gender.upper()

        user_profile.save()
        return render(request,'main/func/profile.html',context)

    return render(request,'main/edit/editProfile.html',context)

# Notifications page
@login_required(login_url="login")
def notifications(request):
    context={}
    user = AUser.objects.get(pk=request.user.pk)
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    context["langtolearn"]=user_profile.learn_lang
    return render(request,"main/func/notifications.html",context)


# Friends page
@login_required(login_url="login")
def friends(request):
    context={}
    user = AUser.objects.get(pk=request.user.pk)
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    context["langtolearn"]=user_profile.learn_lang
    return render(request,"main/func/friends.html",context)


# Feedback page
@login_required(login_url="login")
def feedback(request):
    context={}
    user = AUser.objects.get(pk=request.user.pk)
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    context["langtolearn"]=user_profile.learn_lang
    return render(request,"main/func/feedback.html",context)


# Contacts page
@login_required(login_url="login")
def contact(request):
    context={}
    user = AUser.objects.get(pk=request.user.pk)
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    context["langtolearn"]=user_profile.learn_lang
    return render(request,"main/func/contact.html",context)


# Events page
@login_required(login_url="login")
def events(request):
    context={}
    user = AUser.objects.get(pk=request.user.pk)
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    context['learning_sources']=LearningSource.objects.all()
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    context["langtolearn"]=user_profile.learn_lang
    return render(request,"main/func/events.html",context)


# Settings page
@login_required(login_url="login")
def settings(request):
    context={}
    user = AUser.objects.get(pk=request.user.pk)
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)

    user = AUser.objects.get(pk=request.user.pk)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        language=request.POST.get("language")
        langToLearn=request.POST.get("learn_lang")
        user_profile.language = language
        user_profile.learn_lang = langToLearn
        user_profile.save()

    context["lang"]=user_profile.language
    context["langtolearn"]=user_profile.learn_lang

    return render(request,"main/func/settings.html",context)

# Quiz page
@login_required(login_url="login")
def startQuiz(request):
    context={}
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    return render(request,"main/func/quiz.html",context)

# Vocab Quiz page
def getRandomVocab():
    connection=connect(django_set.BASE_DIR/'databases/en_US.db')
    cursor=connection.cursor()
    query = cursor.execute("""
    SELECT * FROM dictionary
    WHERE word NOT LIKE '%''%' 
    ORDER BY RANDOM()
    LIMIT 1000;""")
    data=query.fetchall()
    randomWord=data[0][0]
    randomWordMeaning=data[0][2]
    question=f"What word is related to {randomWord}?"
    options=[]
    for i in data:
        if i[0]!=randomWord:
            options.append(i[0])
        if len(options)==3:
            break

    r=get(f"https://api.datamuse.com/words?ml={randomWord}&max=3")
    related_words=eval(r.content.decode())
    if len(related_words)>1:
        correctAns=choice(related_words)['word']
    elif len(related_words)==1:
        correctAns=related_words[0]['word']
    else:
        correctAns=randomWord
    options.append(correctAns)
    meanings={}
    return {'question': question,'options':options,'correct_answer':correctAns,'meaning':randomWordMeaning}

@login_required(login_url="login")
def startVocab(request):
    context={}
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    context['questions']=[]
    for i in range(10):
        context['questions'].append(getRandomVocab())
        print(i+1,'questions fetched...')

    return render(request,"main/func/quiz_vocab.html",context)

#Word search page
def getMeaning(word):
    r=get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    content=eval(r.content.decode())[0]['meanings']
    meanings=[]
    try:
        for i in content:
            meanings.append(i['definitions'][0]['definition'])
    except Exception as e:
        meanings=[f"Sorry, no meanings found for this word:( , {str(e)}"]

    con=eval(r.content.decode())[0]['phonetics']
    audio=""
    for i in con:
        if "-us" in i['audio']:
            audio=i['audio']
    return meanings,audio


def getSimilar(word):
    r=get(f"https://api.datamuse.com/words?ml={word}&max=10")
    related_words=eval(r.content.decode())
    rel_words=[]
    try:
        for i in related_words:
            rel_words.append(i['word'])
    except KeyError:
        rel_words=['No Similar words found:(']

    return rel_words

def getSimilarSounds(word):
    r=get(f"https://api.datamuse.com/words?sl={word}&max=10")
    related_words=eval(r.content.decode())
    rel_words=[]
    try:
        for i in related_words:
            rel_words.append(i['word'])
    except KeyError:
        rel_words=['No Similar Sounding words found:(']

    return rel_words

@login_required(login_url="login")
def wordSearch(request):
    context={}
    if request.method == 'POST':
        context['notifications_unread']=['']
        context['notifications_count']=0
        query = request.POST.get('word')
        context['word_meanings'],context['phonetic']=getMeaning(query)
        context['similar_words']=getSimilar(query)
        context['similar_sounds']=getSimilarSounds(query)
        context['meaning_count']=len(context['word_meanings'])
        context['similar_count']=len(context['similar_words'])
        context['similar_sound_count']=len(context['similar_sounds'])

        return render(request,"main/func/word_search.html",context)
    else:
        context['notifications_unread']=notifs(request.user)
        context['notifications_count']=notifCount(request.user)
        context['meaning_count']=0
        context['similar_count']=0
        context['similar_sound_count']=0
        return render(request,"main/func/word_search.html",context)

@login_required(login_url="login")
def showLetters(request):
    context={}
    user = AUser.objects.get(pk=request.user.pk)
    context['notifications_unread']=notifs(request.user)
    context['notifications_count']=notifCount(request.user)
    user_profile = UserProfile.objects.get(user=user)
    context["lang"]=user_profile.language
    context["langtolearn"]=user_profile.learn_lang
    return render(request, f"main/func/letters/{context['langtolearn']}.html",context)

# Logout function
def logOut(request):
    logout(request)
    return redirect("/login/")

