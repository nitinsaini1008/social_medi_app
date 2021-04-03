from django.db import models
from django.contrib.auth.models import User,auth

class post_1(models.Model):
	name=models.CharField(max_length=100)
	desc=models.CharField(max_length=200)
	user_data=models.ForeignKey(User,on_delete=models.CASCADE)
	likes=models.ManyToManyField(User,related_name='blog_post')

	def total_likes(self):
		return self.likes.count()

class post_2(models.Model):
	desc=models.CharField(max_length=200)
	name=models.ForeignKey(User,on_delete=models.CASCADE)
	user_img=models.ImageField(upload_to='images/')
	likes=models.ManyToManyField(User,related_name='blog_post_2')

	def total_likes(self):
		return self.likes.count()
class post_3(models.Model):
	desc=models.CharField(max_length=200)
	name=models.ForeignKey(User,on_delete=models.CASCADE)
	user_video=models.FileField(upload_to='videos/')
	likes=models.ManyToManyField(User,related_name='blog_post_3')

class friends(models.Model):
	ofuser=models.ForeignKey(User,on_delete=models.CASCADE)
	f=models.ManyToManyField(User,related_name='friends_list')

class friend_request(models.Model):
	fromuser=models.ForeignKey(User,on_delete=models.CASCADE,related_name='from_user')
	touser=models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user')
	datetime=models.DateTimeField(auto_now_add=True)

