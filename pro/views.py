from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from .models import post_1,friends,friend_request,post_2,post_3
from .forms import post_2_form,post_3_form
import requests
# from django.contrib.auth import login,authenticate,logout
import json
from django.http import HttpResponseRedirect

def home(request):
	return render(request,'home.html')

def test_1(request):
    code = request.GET['code']
    state = request.GET['state']

    url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {'grant_type':'authorization_code','code':code,
            'redirect_uri':'http://127.0.0.1:8000/test_1',
            'client_id':'client_id',
            'client_secret':'app secret'
            }
    r = requests.post(url, data=data)
    access_token = r.json()['access_token']

    url = "https://api.linkedin.com/v2/me"
    headers = {"Authorization": "Bearer "+access_token}
    r = requests.get(url, headers=headers)
    data = r.json()

    url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
    headers = {"Authorization": "Bearer "+access_token}
    r = requests.get(url, headers=headers)
    dat = r.json()

    url = "https://api.linkedin.com/v2/me?projection=(id,profilePicture(displayImage~digitalmediaAsset:playableStreams))"
    headers = {"Authorization": "Bearer "+access_token}
    r = requests.get(url, headers=headers)
    image_data = r.json()
    print(image_data)
    
    try:
        image_url = image_data['profilePicture']['displayImage~']['elements'][3]['identifiers'][0]['identifier']
        print(image_url)
    except:
        image_url=''
    fname = data['firstName']['localized']['en_US']
    lname = data['lastName']['localized']['en_US']
    id = data['id']
    email = dat['elements'][0]['handle~']['emailAddress']

    curr_user = auth.authenticate(username=email,password=id)
    if curr_user!=None:
        user = auth.authenticate(username=email, password=id)
        auth.login(request, user)
        try:
            u=friends.objects.get(ofuser=request.user)
        except:
            u=friends(ofuser=request.user)
            u.save()
        return redirect('main_page')
    else:
        user = User.objects.create_user(username=email, email=email, password=id,first_name=image_url,last_name=fname+' '+lname)
        user.save()

        user=auth.authenticate(username=email,password=id)
        auth.login(request, user)
        u=friends(ofuser=request.user)
        u.save()
    
    return redirect('main_page')
def main_page(request):
	tf=friends.objects.get(ofuser=request.user)
	tff=tf.f.all()
	f=friend_request.objects.filter(touser=request.user)
	p1=post_1.objects.filter(user_data=request.user)
	p2=post_2.objects.filter(name=request.user)
	p3=post_3.objects.filter(name=request.user)
	return render(request,'details.html',{'p1':p1,'f':f,'tff':tff,'p2':p2,'p3':p3})
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
		frnd=friends.objects.get(ofuser=request.user)
		ans='False'
		if f in frnd.f.all():
			ans='True'
		p1=post_2.objects.filter(name=f)
		return render(request,'search_fri.html',{'d':f,'ans':ans,'p1':p1})
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
	
def add_like_p1(request,id):
	p1=post_2.objects.get(id=id)
	if request.user in p1.likes.all():
		p1.likes.remove(request.user)
	else:
		p1.likes.add(request.user)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
