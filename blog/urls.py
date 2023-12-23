from django.contrib import admin
from django.urls import path
from .views import *
from .views import like_post

urlpatterns = [
    path('', AboutView.as_view(), name='about'),
    path('post_list/', PostListView.as_view(), name='post_list'),
    path('post_detail/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post_create/', PostCreateView.as_view(), name="post_create"),
    path('post_update/<int:pk>', PostUpdateView.as_view(), name="post_update"),
    path('post_delete/<int:pk>', PostDeleteView.as_view(), name="post_delete"),
    # path('draft_list/', DraftListView.as_view(), name="draft_list"),
    path('add_comment/<int:pk>', AddCommentToPost.as_view(), name="add_comment"),
    path('comment_approve/<int:pk>', CommentApproveView.as_view(), name="comment_approve"),
    path('comment_remove/<int:pk>', CommentRemoveView.as_view(), name="comment_remove"),
    path('post_publish/<int:pk>', PostPublishView.as_view(), name="post_publish"),
    path('like/<int:pk>/', like_post, name='like_post'),
]
   