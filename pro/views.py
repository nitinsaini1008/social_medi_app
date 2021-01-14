from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from .models import post_1,friends,friend_request,post_2,post_3
from .forms import post_2_form,post_3_form
# from django.contrib.auth import login,authenticate,logout
import json
def home(request):
	return render(request,'home.html')
def main_page(request):
	tf=friends.objects.get(ofuser=request.user)
	tff=tf.f.all()
	f=friend_request.objects.all().filter(touser=request.user)
	p=post_1.objects.all().filter(user_data=request.user)
	return render(request,'details.html',{'p':p,'f':f,'tff':tff})
def add_friend(request):
	idd=request.GET['id']
	print(idd)
	try:
		u=User.objects.get(id=idd)
		f=friend_request(fromuser=request.user,touser=u)
		f.save()
		return redirect('main_page')
	except:
		print("hello\n\n\n\n")
		return HttpResponse("unable to add user"+str(idd))
def search_fri(request):
	fri=request.GET['friend']
	f=fri
	print(f)
	try:
		f=User.objects.get(username=f)
		return render(request,'search_fri.html',{'d':f})
	except:
		f='no user found'
		return render(request,'search_fri.html',{'d':f})
def add_request(request):
	idd=request.GET['id']
	try:
		u=User.objects.get(id=idd)
		fr=friends.objects.get(ofuser=request.user)
		fr.f.add(u)
		fr2=friends.objects.get(ofuser=u)
		fr2.f.add(request.user)
		f=friend_request.objects.all().filter(fromuser=u)
		if f is not None:
			f.delete()
		return redirect('main_page')
	except:
		return HttpResponse("unable to add user")
def details(request):
	email=request.GET['email']
	username=request.GET['username']
	phoneNumber=request.GET['phoneNumber']
	photoURL=request.GET['photoURL']
	user=auth.authenticate(username=email,password=email)
	if user is not None:
		auth.login(request,user)
		try:
			u=friends.objects.get(ofuser=request.user)
		except:
			u=friends(ofuser=request.user)
			u.save()
		return redirect('main_page')

	else:
		user=User.objects.create_user(username=email,password=email,first_name=photoURL,last_name=username)
		user.save()
		user=auth.authenticate(username=email,password=email)
		auth.login(request,user)
		u=friends(ofuser=request.user)
		u.save()
		return redirect('main_page')

def add_post_1(request):
	d={'name':request.user.username}
	return render(request,'add_post_1.html',d)
def add_post_1_post(request):
	name=request.POST['name']
	desc=request.POST['desc']
	s=name+desc+request.user.username
	p=post_1(name=name,desc=desc,user_data=request.user)
	p.save()
	return redirect('main_page')

def search_word(request):
	wd=request.GET['wd']
	u=User.objects.filter(username__icontains=wd)
	d={}
	for i in u:
		d[i.username]=i.username
	d=json.dumps(d)
	return HttpResponse(d)

def add_post_2(request):
	if request.method=='POST':
		f=post_2_form(request.POST,request.FILES)

		if f.is_valid():
			t=post_2(desc=f.cleaned_data['desc'],name=request.user,user_img=f.cleaned_data['user_img'])
			t.save()
			return HttpResponse('success')
			print(f.cleaned_data)
			return HttpResponse(f.cleaned_data['user_img'])
			f.save()
			return redirect('home')
	else:
		f=post_2_form()
	return render(request,'post_2.html',{'f':f})
def add_post_3(request):
	if request.method=='POST':
		f=post_3_form(request.POST,request.FILES)

		if f.is_valid():
			t=post_3(desc=f.cleaned_data['desc'],name=request.user,user_video=f.cleaned_data['user_video'])
			t.save()
			return HttpResponse('success')
			print(f.cleaned_data)
			return HttpResponse(f.cleaned_data['user_img'])
			f.save()
			return redirect('home')
	else:
		f=post_3_form()
	return render(request,'post_3.html',{'f':f})

def show_post_2(request,idd):
	try:
		idd=int(idd)
	except:
		return HttpResponse('some thing went wrong')
	try:
		u=User.objects.get(id=idd)
		f=post_2.objects.filter(name=u)
		return render(request,'show_post_2.html',{'f':f})
	except:
		return HttpResponse('user is not there')

def show_post_3(request,idd):
	try:
		idd=int(idd)
	except:
		return HttpResponse('some thing went wrong')
	try:
		u=User.objects.get(id=idd)
		f=post_3.objects.filter(name=u)
		return render(request,'show_post_3.html',{'f':f})
	except:
		return HttpResponse('user is not there')
	