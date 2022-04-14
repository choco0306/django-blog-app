from ensurepip import version
from statistics import mode
from tabnanny import verbose
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Category(models.Model):
    name = models.CharField(verbose_name="カテゴリー", max_length=255)
    slug = models.SlugField(verbose_name="URL", unique=True)

    # 管理画面でタイトルを表示する
    def __str__(self):
        return self.name
    
    # 管理画面で日本語表示にする
    class Meta():
        verbose_name = "カテゴリー"
        # 複数でもカテゴリーと表示されるようにする
        verbose_name_plural = "カテゴリー"


class Tag(models.Model):
    name = models.CharField(verbose_name="タグ", max_length=255)
    slug = models.SlugField(verbose_name="URL", unique=True)
    
    # 管理画面でタイトルを表示する
    def __str__(self):
        return self.name

    # 管理画面で日本語表示にする
    class Meta():
        verbose_name = "タグ"
        # 複数でもタグと表示されるようにする
        verbose_name_plural = "タグ"


# カテゴリーと記事は1対他なのでForeignKeyを使う
# タグと記事は他対他なのでManyToManyFieldを使う
class Post(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=200)
    # content = models.TextField(verbose_name="本文")
    content = MarkdownxField(verbose_name="本文")
    image = models.ImageField(verbose_name="画像", upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="作成日", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日", auto_now=True)
    is_published = models.BooleanField(verbose_name="公開設定", default=False)
    category = models.ForeignKey(Category, verbose_name="カテゴリー", on_delete=models.PROTECT, null=True, blank=True)
    tag = models.ManyToManyField(Tag, verbose_name="タグ", blank=True)

    # markdownを使えるようにする
    def convert_markdown_to_html(self):
        return markdownify(self.content)

    # 管理画面でタイトルを表示する
    def __str__(self):
        return self.title

    # 管理画面で日本語表示にする
    class Meta():
        verbose_name = "記事"
        # 複数でも記事と表示されるようにする
        verbose_name_plural = "記事"


# ブログに対してコメントをつける機能追加
class Comment(models.Model):
    name = models.CharField(verbose_name="名前", max_length=100)
    text = models.TextField(verbose_name="本文")
    created_at = models.DateTimeField(verbose_name="作成日", auto_now_add=True)
    # ブログ記事とコメントは1対他の関係なのでForeignKeyを使う。
    # on_delete=models.CASCADEとすることでブログが削除されたらコメントも削除される
    post = models.ForeignKey(Post, verbose_name="記事", on_delete=models.CASCADE)

    # 先頭10文字を表示
    def __str__(self):
        return self.text[:10]

    # 管理画面で日本語表示にする
    class Meta():
        verbose_name = "コメント"
        # 複数でもコメントと表示されるようにする
        verbose_name_plural = "コメント"


# コメントに対する返信モデル
class Reply(models.Model):
    name = models.CharField(verbose_name="名前", max_length=100)
    text = models.TextField(verbose_name="本文")
    created_at = models.DateTimeField(verbose_name="作成日", auto_now_add=True)

    comment = models.ForeignKey(Comment, verbose_name="コメント", on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:10]
    
    # 管理画面で日本語表示にする
    class Meta():
        verbose_name = "返信"
        # 複数でも返信と表示されるようにする
        verbose_name_plural = "返信"
