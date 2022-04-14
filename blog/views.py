from re import template
from unicodedata import category
from webbrowser import get
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from blog.models import Post, Category, Tag, Comment, Reply
from django.http import Http404
from django.db.models import Q
from blog.forms import CommentForm, ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin

posts_per_page = 5

# 投稿一覧表示
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = 'posts'
    paginate_by = posts_per_page     # 1ページあたりの表示件数を設定

    # 更新日でソートする(新しい順にする)
    def get_queryset(self):
        posts = super().get_queryset()
        # print(posts)
        # print(posts[0])
        return posts.order_by('-updated_at')


# 記事詳細表示
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    # ログインしていないユーザの下書きへのアクセスを禁止する
    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        # print(vars(post))
        # 公開済み or ログインしているユーザ
        if post.is_published or self.request.user.is_authenticated:
            return post
        else:
            raise Http404


# カテゴリーから記事を絞り込む機能追加
class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = posts_per_page     # 1ページあたりの表示件数を設定

    def get_queryset(self):
        # トップページでアクセスのあったカテゴリーのURLを変数slugに代入
        slug = self.kwargs['slug']
        # 存在しないカテゴリーの場合は、404を返す
        self.category = get_object_or_404(Category, slug=slug)
        
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category        
        return context


# タグから記事を絞り込む機能追加
class TagPostListView(ListView):
    model = Post
    template_name = 'blog/post-list.html'
    context_object_name = 'posts'
    paginate_by = posts_per_page     # 1ページあたりの表示件数を設定

    def get_queryset(self):
        slug = self.kwargs['slug']
        self.tag = get_object_or_404(Tag, slug=slug)
        return super().get_queryset().filter(tag=self.tag)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag

        return context


# ナビゲーションバーから検索する機能追加
class SearchPostListView(ListView):
    model = Post
    template_name = 'blog/post-list.html'
    context_object_name = 'posts'
    paginate_by = posts_per_page     # 1ページあたりの表示件数を設定

    def get_queryset(self):
        self.query = self.request.GET['query'] or ""
        queryset = super().get_queryset()
        
        # タイトルと本文で検索する
        if self.query:
            queryset = queryset.filter(
                Q(title__icontains=self.query) | Q(content__icontains=self.query)
            )
        
        # 検索時ログインしていないユーザには非公開の件数を含めない
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)

        self.post_count = len(queryset)


        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['post_count'] = self.post_count

        return context


# コメントを作成
# コメントを作成するのでCreateViewを継承する
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    # デフォルトでフォームの名前はcomment_form.htmlとなっているのでtemplate_nameの設定は不要

    # formで送られてきた内容を変更する
    def form_valid(self, form):
        # formで送られてきた内容をデータベースに登録する前にform_valid内で扱えるよにする
        comment = form.save(commit=False)

        post_pk = self.kwargs['post_pk']
        post = get_object_or_404(Post, pk=post_pk)

        comment.post = post
        comment.save()
        return redirect('post-detail', pk=post_pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['post_pk']
        context['post']  = get_object_or_404(Post, pk=post_pk)
        return context


# 返信を作成
# 返信を作成するのでCreateViewを継承する
class ReplyCreateView(CreateView):
    model = Reply
    form_class = ReplyForm
    # デフォルトでフォームの名前はreply_form.htmlとなっているのでtemplate_nameで設定する必要がある
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        reply = form.save(commit=False)

        comment_pk = self.kwargs['comment_pk']
        comment = get_object_or_404(Comment, pk=comment_pk)

        reply.comment = comment
        reply.save()
        return redirect('post-detail', pk=comment.post.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['comment_pk']
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
        return context


# コメントを削除する機能追加
# LoginRequiredMixinは管理者のみが削除できるようにする
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'
    # 遷移先がpost-detail/<int:pk>のかたちにならなければならないがreverse_lazyでは出来ない
    # success_url = reverse_lazy('post-detail')

    # reverse_lazyの代わりにget_success_urlを使う
    def get_success_url(self):
        # print(self)
        # print(vars(self))
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

# 返信を削除する機能を追加
# LoginRequiredMixinは管理者のみが削除できるようにする
class ReplyDeleteView(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = 'blog/comment_delete.html'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.comment.post.pk})