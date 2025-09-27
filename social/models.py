from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager



class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    photo = models.ImageField(upload_to="account_images/", verbose_name="عکس پروفایل", blank=True, null=True)
    job = models.CharField(max_length=250, verbose_name="شغل", null=True, blank=True)
    bio = models.TextField(verbose_name="بیوگرافی", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="شماره تلفن", null=True, blank=True)
    following = models.ManyToManyField('self', through='Contact' , related_name='followers', symmetrical=False)
    


class Post(models.Model): 
    author = models.ForeignKey(User, on_delete=models.CASCADE , related_name="user_posts", verbose_name="نویسنده" )
    description = models.TextField(verbose_name="توضیحات")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_posts')
    tags = TaggableManager()
    total_likes = models.PositiveIntegerField(default=0)
    

    class Meta:
        ordering = ['-created']
        indexes = [ 
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes'])
        ]
                                             

    def get_absolute_url(self):
        return reverse('social:post_detail',args=[self.id])
    


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]   

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'  