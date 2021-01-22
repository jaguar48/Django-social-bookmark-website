from django.contrib import admin
from .models import Post,Comment, Category, Subscriber,Newsletter

admin.site.register(Subscriber)
admin.site.register(Newsletter)
def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)

send_newsletter.short_description = "Send selected Newsletters to all subscribers"


class NewsletterAdmin(admin.ModelAdmin):
    actions = [send_newsletter]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status','category')
    list_filter = ('status', 'created', 'publish', 'author','category')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    def approve_post(self,request,queryset):
        queryset.update(active=True)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']
    def approve_comments(self,request,queryset):
        queryset.update(active=True)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
