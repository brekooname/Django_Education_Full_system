from distutils.command.upload import upload
from email.policy import default
from email.quoprimime import quote
from enum import unique
from pyexpat import model
from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
# Create your models here.
class Categories(models.Model):
    icon = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Author(models.Model):
    author_profile = models.ImageField(upload_to='author')
    name = models.CharField(max_length=100,null=True)
    position = models.CharField(max_length=100,null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name + " - " + self.position

class Level(models.Model):
    
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Language(models.Model):
    
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Course(models.Model):

    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT','DRAFT'),
    )

    featured_image = models.ImageField(upload_to='featured_img',null=True)
    featured_video = models.CharField(max_length=300,null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    level = models.ForeignKey(Level,on_delete=models.CASCADE,null=True)
    language = models.ForeignKey(Language,on_delete=models.CASCADE,null=True)
    deadline = models.CharField(max_length=300,null=True)
    certificate = models.BooleanField(default=False,null=True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True)
    slug = AutoSlugField(populate_from='title',unique=True,null=True,default=None)
    status = models.CharField(choices=STATUS,max_length=100,null=True)

    def __str__(self):
        return self.title

class What_you_learn(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    point = models.CharField(max_length=200)

    def __str__(self):
        return self.point

class Requirement(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    point = models.CharField(max_length=200)

    def __str__(self):
        return self.point

class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)

    def __str__(self) :
        return self.name + " - " + self.course.title

class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to='yt_thumbnail',null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=200)
    time_duration = models.FloatField(null=True)
    preview = models.BooleanField(default=False)

    def __str__(self):
            return self.title

class Usercourse(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + self.course.title

class Payment(models.Model):

    order_id = models.CharField(max_length=100,null=True,blank=True)
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    user_course = models.ForeignKey(Usercourse,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " - " + self.course.title

class User_Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="userprofileimg",null=True)
    
    def __str__(self):
        return self.user.username
    
class Blog(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField( max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog-image',null=True)
    description = models.TextField()
    quote = models.CharField(max_length=500,null=True)
    slug = AutoSlugField(populate_from='title',unique=True,null=True,default=None)

    def __str__(self):
        return self.title + " - " + self.author.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event-image',null=True)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

class Review(models.Model):

    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True,default=None)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,null=True,blank=True,default=None)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    review_rate = models.FloatField(null=True)
    review_title = models.CharField(max_length=200,null=True)
    review_content = models.TextField()

    def __str__(self):
        return self.review_title + " - " + self.user.username