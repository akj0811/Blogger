from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Blog(models.Model):
	title = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	content = models.TextField()
	date_posted = models.DateTimeField(default = timezone.now())
	category = models.ForeignKey('blog.Category',on_delete = models.CASCADE)
	author = models.ForeignKey(User, on_delete = models.CASCADE)

	def save(self,*args,**kwargs):
		self.slug=slugify(self.title)
		super(Blog, self).save(*args,**kwargs)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('view_post', kwargs={'slug': self.slug})

class Category(models.Model):
	title = models.CharField(max_length=100, db_index=True)
	slug = models.SlugField(max_length=100, db_index=True)

	def save(self,*args,**kwargs):
		self.slug=slugify(self.title)
		super(Category, self).save(*args,**kwargs)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('home')