from re import search
from django.contrib import admin
from blog.models import Post, Category, Tag, Comment, Reply
from markdownx.admin import MarkdownxModelAdmin

# 管理画面でコメントを確認できるようにする
class ReplyInline(admin.StackedInline):
    model = Reply

class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]


# デフォルトでは管理画面にtitleしか表示されないので、他の項目も表示できるようにする
class PostAdmin(MarkdownxModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at', 'is_published')

    # 管理画面でtitleとcontentで検索できるようにする
    search_fields = ('title', 'content')

    # 管理画面でcategoryで検索できるようにする。タプルの要素が1つの場合は、最後のカンマが必要なのを注意
    list_filter = ('category',)


# 管理画面でmodels.pyの内容を表示できるようにする
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply)
