from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.views import View

from .models import Post,Like,Comment




class SignUpView(View):
    def post(self, request):
        username = request.POST.username
        email = request.POST.email
        password = request.POST.password
            
        user = User.objects.create_user(username,email,password)
        if user is not None:
            login(request, user)
        else:
            return HttpRequest("Could not create the user")

class LoginView(View):
    def post(self, request):
        username = request.POST.username
        password = request.POST.password
        
        user = authenticate(username= username, password= password)
        if user is not None:
            login(request, user)
            ## AFTER LOGIN

            return HttpRequest("Logged in!")
        else:
            return HttpResponse("Please try again later, error occured!")

class ForgotPasswordView(View):
    def post(self,request):
        username = request.POST.username
        new_password = request.POST.new_password

        user = User.objects.get(username= username)
        if user is not None:
            user.set_password(new_password)
            user.save()
        else:
            return HttpResponse("User does not exist")

class LogoutView(View):
    def post(self,request):
        logout(request)

class PostImageView(View):
    def post(self,request):
        if request.user.is_authenticated:

            post = Post(request,request.FILES)
            if post.is_valid():
                post.save()
                return HttpResponse("Post saved!")
            else:
                return HttpsResponse(post.errors())
        else:
            return HttpResponse("Requires Logging in!")
class CommentView(View):
    def post(self,request,pk):
        if request.user.is_authenticated:
            post = Post.objects.get(pk=pk)
            comment = Comment(post,request,request.POST)
            if comment.is_valid():
                comment.save()
                return HttpResponse("Comment Saved")
            else:
                return HttpResponse(comment.errors())
        else:
            return HttpResponse("Requires Logging in!")
class ReplyView(View):
    def post(self, request,pk):
        if request.user.is_authenticated:
            comment = Comment.objects.get(pk=pk)
            reply = Reply(comment,request,request.POST)
            if reply.is_valid():
                reply.save()
                return HttpRepsonse("Reply saved")
            else:
                return HttpResponse(reply.errors)
        else:
            return HttpResponse("Requires Logging in!")

class LikePost(View):
    def post(self, request, pk):
        if request.user.is_authenticated:
            post = Post.objects.get(pk= pk)
            like = Like(request,post,request.POST)
            if like.is_valid():
                like.save()
                return HttpResponse("You liked it!")
            else:
                return HttpResponse(like.erros)

class Feed(View):
    def get(self, request):
        if request.user.is_authenticated:
            posts = Post.objects.all().exclude(user= request.user)
            comments = []
            likes = []
            replies = []
            for post in posts.values():
                comments_temp = []
                replies_temp_1 = []
                liked_users = []

                comments_query_set = Comment.objects.filter(post= post.pk)
                for comment in comments_query_set.values():
                    comments_temp.append(comment)
                    replies_query_set = Reply.objects.filter(comment= comment.pk)
                    replies_temp_2 = []
                    for reply in replies_query_set.values():
                        replies_temp_2.append(reply)
                    replies_temp_1.append(replies_temp_2)
                
                likes_query_set = Like.objects.filter(post=post.pk)
                for like in liked_query_set.values():
                    liked_users.append(like.user)
