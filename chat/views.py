from django.shortcuts import render
from .models import chatmsg
def index(request):
	return render(request,'index.html')

def room(request,room_name):
	other=room_name
	me=request.user.username
	print(room_name)
	print(me)
	r1=room_name.split('@')
	r1=r1[0].split('.')[0]
	r2=me.split('@')
	r2=r2[0].split('.')[0]
	ans=str(r1)+str(r2)
	a=list(ans)
	a.sort()
	ans=''
	for i in a:
		ans+=i

	room_name=ans
	msg=chatmsg.objects.filter(roomname=room_name)
	return render(request, 'room.html', {
        'room_name': room_name,
        'msg':msg,
        'other':other
    })