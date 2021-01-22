from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class PublishedManager(models.Manager):
        def get_queryset(self):
                return
                super(PublishedManager,self).get_queryset()\
                        .filter(status='Draft')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),)
    title = models.CharField(max_length=250)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete = models.CASCADE)
    slug = models.SlugField(max_length=250,
             unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    active = models.BooleanField(default=False)
    status = models.CharField(max_length=10,
            choices=STATUS_CHOICES,
            default='publish')
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager  
    class Meta: 
                ordering = ('-publish',)
                def __str__(self):
                    return self.title
    def approve_post(self):
        
        return self.published.filter(active=False)
    def approve_comments(self):
        return self.comments.filter(active=False)
    def get_absolute_url(self):
            return reverse('blog:post_detail',kwargs={'pk':self.pk})
    tags = TaggableManager()
    def get_cat_list(self):
        k = self.category # for now ignore this instance method
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]
class Comment(models.Model):
        post = models.ForeignKey(Post,
            on_delete=models.CASCADE,
            related_name='comments')
        name = models.CharField(max_length = 25)
        email = models.EmailField()
        body = models.TextField()
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)
        active = models.BooleanField(default=False)
        class meta:
                ordering = ('created',)
        def __str__(self):

                return f'Comment by {self.name} on {self.post}'
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete = models.CASCADE)

    class Meta:
        #enforcing that there can not be two categories under a parent with same slug
        
        # __str__ method elaborated later in post.  use __unicode__ in place of
        
        # __str__ if you are using python 2

        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"     

    def __str__(self):                           
        full_path = [self.name]                  
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email + "(" + ("not " if not self.confirmed else "") + "confirmed)"
class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='uploaded_newsletters/')

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")

    def send(self, request):
        contents = self.contents.read().decode('utf-8')
        subscribers = Subscriber.objects.filter(confirmed=True)
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        for sub in subscribers:
            message = Mail(
                    from_email=settings.FROM_EMAIL,
                    to_emails=sub.email,
                    subject=self.subject,
                    html_content=contents + (
                        '<br><a href="{}/delete/?email={}&conf_num={}">Unsubscribe</a>.').format(
                            request.build_absolute_uri('/delete/'),
                            sub.email,
                            sub.conf_num))
            sg.send(message)