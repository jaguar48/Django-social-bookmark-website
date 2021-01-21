from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage,\
PageNotAnInteger
from .models import Post, Comment, Category
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from .forms import CommentForm,PostForm, Emailshare,Contact 
from django.core.mail import send_mail, BadHeaderError
from taggit.models import Tag
from django.db.models import Count
from django.core.mail import send_mail

# Create your views here.
def post_list(request, **kwargs):
    object_list = Post.objects.all()
    tag = None
    tag_slug = kwargs.get("tag_slug")
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    print(page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    if tag:
        return render(request, 'blog/post/list.html', {'posts': posts,'tag': tag})
    else:
        return render(request, 'blog/post/list.html', {'posts': posts})
def create_post(request):
    sent = False
    if request.method == 'POST':
        forms = PostForm(data =request.POST, files=request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('/blog')
            sent = True
    else:
        forms = PostForm()
    return render(request,'blog/post/create.html',{'forms':forms })
def post_detail(request,pk):
        post = get_object_or_404(Post, pk=pk,status='published')
        # List of active comments for this post
        comments = post.comments.filter(active=True)
        new_comment = None
        if request.method == 'POST':
        # A comment was posted
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
            # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/') )
        else:
            comment_form = CommentForm()

        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
        return render(request,'blog/post/detail.html',{'post': post,'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,'similar_posts':similar_posts})

def contact(request):
    sent = False
    if request.method == 'POST':
        contact = Contact(data=request.POST)
        if contact.is_valid():
            name = contact.cleaned_data['name']
            sender = contact.cleaned_data['email']
            subject = contact.cleaned_data['subject']
            message = contact.cleaned_data['message']
            recipients = ['agrictime@gmail.com']
            try:
                send_mail(subject, message, sender, recipients)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
        sent = True
    else: 
        contact = Contact()
    return render(request, 'blog/post/contact.html', {'contact': contact, 'sent':sent})
def share(request, pk):
    post = get_object_or_404(Post, pk=pk,status='published')
    sent = False
    if request.method == 'POST':
        form = Emailshare(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, '',[cd['to']])
            sent = True
            return redirect('blog:post_detail',pk=pk)
    else:
        form = Emailshare()
    return render(request, 'blog/post/share.html', {'post': post,
        'form': form, 'sent':sent})

def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    category_queryset = list(Category.objects.all())
    all_slugs = [ x.slug for x in category_queryset ]
    parent = None
    for slug in category_slug:
        if slug in all_slugs:
            parent = get_object_or_404(Category,slug=slug,parent=parent)
        else:
            instance = get_object_or_404(Post, slug=slug)
            breadcrumbs_link = instance.get_cat_list()
            category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
            breadcrumbs = zip(breadcrumbs_link, category_name)
            return render(request, "blog/post/detail.html", {'instance':instance,'breadcrumbs':breadcrumbs})

    return render(request,"blog/post/categories.html",{'post_set':parent.post_set.all(),'sub_categories':parent.children.all()})

def post_random(request):
    poster = Post.objects.order_by("?")[:4]
    return render(request, "blog/post/random_post.html", {'poster':poster})