from django.db import models
from utils.rands import slugfy_new
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural= 'Tags'

    name= models.CharField(max_length=255)
    slug=models.SlugField(
        unique=True,
        default= None, null=True,blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural= 'Categories'

    name= models.CharField(max_length=255)
    slug=models.SlugField(
        unique=True,
        default= None, null=True,blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.name)
        return super.save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural= 'Pages'

    title= models.CharField(max_length=65)
    slug=models.SlugField(
        unique=True,
        default= None, null=True,blank=True
    )
    is_published = models.BooleanField(default=False)
    content = models.TextField()
     
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class PostManager(models.Manager):
    
    def get_published(self):
        return self.filter(is_published=True).order_by('-pk')




class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural= 'Posts'

    objects = PostManager()

    title= models.CharField(max_length=65)
    slug=models.SlugField(
        unique=True,
        default= None, null=True,blank=True
    )
    excerpt = models.CharField(max_length=150)
    is_published = models.BooleanField(default=False)
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/', blank=True)
    cover_in_post_content = models.BooleanField(
        default=True, help_text='Se marcado, exibirá a capa dentro do post'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,blank=True, null=True, default=None)
    tag = models.ManyToManyField(Tag, blank=True, default='')
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True, null=True, related_name='post_created_by')
    update_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True, null=True, related_name='post_update_by')


    def get_absolute_url(self):
        
        if not self.is_published:
            return reverse('blog:index')
        return reverse('blog:post' , args=(self.slug,))
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

