from django.db import models
from django.contrib.auth.models import User

class chatmsg(models.Model):
	roomname=models.CharField(max_length=300)
	by_user=models.ForeignKey(User,related_name='send_by_user',on_delete=models.CASCADE)
	to_user=models.ForeignKey(User,related_name='receive_by_user',on_delete=models.CASCADE)
	msg=models.CharField(max_length=1000)