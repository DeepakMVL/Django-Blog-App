from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
#DUMMY DATA
"""posts = [
    {
    'author' : 'Benjamin Franklin',
    'title' : '"For the Want of a Nail"',
    'content' : 'First post content',
    'date_posted' : 'October 27th 2021'
    },
    {
    'author' : 'Tagore',
    'title' : '"Gitanjali"',
    'content' : 'Second post content',
    'date_posted' : 'October 27th 1919'
    }
]"""
# Create your views here.
'''def home(request):
    context={
    'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)'''

class PostListView(ListView):
    model=Post
    template_name='blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by = 3

#should get posts only from a certain user
#url has to contain the name of the user that needs to be passed, so specify the user name in url pattern itself
class UserPostListView(ListView):
    model=Post
    template_name='blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name='posts'
    #ordering=['-date_posted']
    paginate_by = 3
    #to modify the query set that this listview returns, we can override the method and change the query set
    def get_queryset(self):
        user = get_object_or_404 (User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields = ['title','content']
#we write this due to the integrity error NOT NULL constraint failed blog_author_id
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request,'blog/about.html',{"title":"About"})
