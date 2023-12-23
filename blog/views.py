from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from django.utils import timezone
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


# Create your views here.
class User_Signup(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sign'] = SignupForm
        return context


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

    # def get_queryset(self):
    #     queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    #     return queryset
    

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['username'] = self.request.user.username
        return kwargs

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})
  


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post



class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


# class DraftListView(LoginRequiredMixin, ListView):
#     redirect_field_name = 'blog/post_list.html'
#     model = Post

#     def get_queryset(self):
#         return Post.objects.filter(published_date__isnull=True).order_by('create_date')


##################################################################
##################################################################


# @login_required
# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'blog/comment_form.html', {'form':form})




class AddCommentToPost(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return reverse('post_detail', kwargs={'pk': post.pk})


# @login_required
# def comment_approve(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.approve()
#     return redirect('post_detail', pk=comment.post.pk)


class CommentApproveView(LoginRequiredMixin, DetailView):
    model = Comment

    def get(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        comment.approve()
        return redirect('post_detail', pk=comment.post.pk)


# @login_required
# def comment_remove(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     post_pk = comment.post.pk
#     comment.delete()
#     return redirect('post_detail', pk=post_pk)


class CommentRemoveView(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('post_detail')


    def get_object(self, queryset=None):
        obj = super().get_object()
        return obj

    def get_success_url(self):
        post_pk = self.object.post.pk
        return reverse_lazy('post_detail', kwargs={'pk':post_pk})



# @login_required
# def post_publish(request, pk):
#     post = get_object_or_404(post, pk=pk)
#     post.publish
#     return redirect('post_detail', pk=pk)


class PostPublishView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.publish()
        return redirect('post_detail', pk=post.pk)


def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user.is_authenticated:
        user = request.user
        if user in post.liked_by.all():
            post.liked_by.remove(user)
            liked = False
        else:
            post.liked_by.add(user)
            liked = True

        post.likes = post.total_likes()  # Update total likes count
        post.save()

        return JsonResponse({'liked': liked, 'count': post.total_likes()})
    else:
        # Handle the case where the user is not authenticated
        return JsonResponse({'error': 'User is not authenticated'})