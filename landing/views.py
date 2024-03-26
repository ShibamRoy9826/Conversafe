# Render Templates
from django.shortcuts import render

# User Auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout , get_user_model

# Redirect user
from django.shortcuts import redirect

# Models
from .models import *
from core.models import UserProfile
# Forms
from .forms import *

# Encryption, keys, and token gen
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token

# Email
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from verify_email.email_handler import send_verification_email

# Notifications
from notifications.signals import notify



# User Model
User=get_user_model()



# Landing Page
def landing(request):
	if request.user.is_authenticated:
		return redirect('/home/')
	return render(request,"index.html")



# Sign up Page
def signup(request):
	# If User is authenticated, redirect to homepage
	if request.user.is_authenticated:
		return redirect('/home/')

	# Checkform
	form=UserForm(request.POST)
	if request.POST:

		if form.is_valid():
			email=form.get_user_info()['email'].lower()
			password=form.get_user_info()['password']
			name=form.get_user_info()['username']

			# Checking if user exists
			if AUser.objects.filter(email=email.lower()).exists():
				return render(request,"auth/signup.html",{"userAlreadyExists":True})

			# Sending Verification Email
			inactive_user = send_verification_email(request, form)
			context={}
			context['text']="A Verification email has been sent to {}".format(email)
			return render(request,"auth/email/showInfo/checkEmail.html",context)
		
		return render(request,"auth/signup.html",{"form":form,"userAlreadyExists":True})
	
	return render(request,"auth/signup.html",{"userAlreadyExists":False,"form":form})



# Login Page

def Login(request):
	# If user is authenticated, redirect to homepage
	if request.user.is_authenticated:
		return redirect('/home/')

	if request.method=="POST":
		email=request.POST.get("email")
		password=request.POST.get("password")

		# Authenticating user
		user=authenticate(request, email=email, password=password)

		

		# If everything is okay...

		if user is not None:
			obj=AUser.objects.get(email=email)
			if obj.firstLogin=="No":
				obj.firstLogin="Yes"
				obj.save()
				UserProfile.objects.create(user=user)
			# 	print("PROFILE CREATED SUCCESSFULLY")
			login(request,user)
			# notify.send(request.user,recipient=request.user,verb="Welcome to Conversafe!",description="Enjoy the application and let me know through feedback! Thank you:)")
			return redirect("/home/")


		# If wrong Info or In active user
		if User.objects.filter(email=email).exists():
			if User.objects.filter(is_active=False):
				context={}
				context['text']="A Verification email has been sent to {}".format(email)
				return render(request,"auth/email/showInfo/checkEmail.html",context)

			return render(request,"auth/login.html",{"wrongInfo":True,"noUser":False})

		# If No such user exists
		return render(request,"auth/login.html",{"wrongInfo":True,"noUser":True})


	return render(request,"auth/login.html",{"wrongInfo":False,"noUser":False})


def forgotPassword(request):
	# If user is logged in, redirect to home
	if request.user.is_authenticated:
		return redirect('/home/')


	if request.method=="POST":
		email=request.POST.get("email").lower()

		# If user exists, send reset Email
		if User.objects.filter(email=email).exists():
			user = User.objects.get(email=email)

			# Activation Token
			token = account_activation_token.make_token(user)
			uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

			# Sending Email
			current_site = get_current_site(request)
			mail_subject = 'Password Reset Request'
			message = render_to_string('auth/email/emailTemplates/pwdResetTemplate.html', {
						'user': user,
						'domain': current_site.domain,
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'token': account_activation_token.make_token(user),
						'link':f"http://127.0.0.1:8000/resetPassword/{uidb64}/{token}"
					})

			message = EmailMessage(mail_subject, message, 'emails.conversafe@gmail.com', [email])
			message.content_subtype = 'html' 
			message.send()

			# Success message for the user
			context={}
			context['text']="A Verification email has been sent to {}".format(email)
			return render(request,"auth/email/showInfo/checkEmail.html",context)

		return render(request,"auth/pass/forgotPassword.html",{"noUser":True})

	return render(request,"auth/pass/forgotPassword.html",{"noUser":False})


def resetPass(request,uidb64,token):
	User = get_user_model()
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None


	if request.method=="POST":
		password=request.POST.get("password")
		
		# If user token is correct, change password
		if user is not None and account_activation_token.check_token(user, token):
			user.set_password(password)
			user.save()
			return render(request,'auth/pass/resetSuccess.html')
		else:
			return render(request,'auth/pass/resetFailed.html')

	return render(request,"auth/pass/resetPass.html")


def error404(request,exception):
	return render(request,"auth/404.html")
# Temp function for testing
def temp(request):
	return render(request,"auth/email/pass/resetSuccess.html")
