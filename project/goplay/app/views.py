from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View


from .models import Post, Like, Comment, Reply
from .forms import PostForm, LikeForm, CommentForm, ReplyForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm

class SignUpView(View):
    def post(self, request): 
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/app/login/')
        else:
            return HttpResponse(form.errors)

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'templates/forms/form.html', {'form': form})


class LoginView(View):
    def post(self, request):

        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username= username, password=password)
            print(user)
            if user is not None:
                login(request,user)
                return HttpResponse("Logged in!")
            else:
                return HttpResponse("User not found")

        else:
            return HttpResponse("Please try again later!")
        
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'templates/forms/form.html', {'form': form})

class ForgotPasswordView(View):
    def post(self,request):
        form = SetPasswordForm(request,request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            request.user.set_password(password)
            request.user.save()
            return HttpResponse("Password changed!")
        else:
            #print(form.errors.values())
            return HttpResponse("Error occured!")

    def get(self,request):
        form = SetPasswordForm(request)
        return render(request, 'templates/forms/form.html', {'form': form})

class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponse("Logged out!")

class PostImageView(View):
    def post(self,request):
        if request.user.is_authenticated:
            post = Post(user= request.user, file = request.FILES['file'])
            post.save()
            return HttpResponse("Post saved!")
        else:
            return HttpResponse("Requires Logging in!")

    def get(self,request):
        form = PostForm()
        return render(request, 'templates/forms/media_form.html', {'form': form})

class CommentView(View):
    def post(self,request,pk):
        if request.user.is_authenticated:
            post = Post.objects.get(pk=pk)
            comment = Comment(post=post,text= request.POST, user= request.user)
            comment.save()
            return HttpResponse("Comment Saved")
        else:
            return HttpResponse("Requires Logging in!")

    def get(self,request,pk):
        form = CommentForm()
        return render(request,'templates/forms/form.html', {'form': form})


class ReplyView(View):
    def post(self, request,pk):
        if request.user.is_authenticated:
            comment = Comment.objects.get(pk=pk)
            reply = Reply(comment= comment,user= request.user,reply= request.POST)
            reply.save()
            return HttpResponse("Reply saved")
        else:
            return HttpResponse("Requires Logging in!")

    def get(self, request,pk):
        form = ReplyForm()
        return render(request, 'templates/forms/form.html', {'form':form})

class LikePost(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            post = Post.objects.get(pk=pk)
            like = Like(user= request.user, post= post)
            like.save()
            return HttpResponse("You liked it!")
        else:
            return HttpResponse("You need to login!")

class Feed(View):
    def get(self, request):
        if request.user.is_authenticated:
            posts_set = Post.objects.all().exclude(user= request.user).values()
            posts = []
            comments = []
            likes = []
            replies = []
            #print(posts_set)
            for post in posts_set:
                #print(post)
                comments_temp = []
                replies_temp_1 = []
                liked_users = []

                comments_query_set = Comment.objects.filter(post_id= post['user_id']).values()
                for comment in comments_query_set:
                    #print(comment)
                    comment['text'] = comment['text'].split(']')[1].split("[")[1][1:-1]     #ghetto solution
                    #print(comment)
                    comments_temp.append(comment)
                    replies_query_set = Reply.objects.filter(comment_id= comment['id'])
                    replies_temp_2 = []
                    for reply in replies_query_set.values():
                        reply['reply'] = reply['reply'].split(" 'reply': ['")[1].split("]")[0][:-1]
                        #print(reply)
                        replies_temp_2.append(reply)
                    replies_temp_1.append(replies_temp_2)
                
                liked_query_set = Like.objects.filter(post_id= post["id"])
                for like in liked_query_set.values():
                    #print(like)
                    liked_users.append(like["user_id"])

                comments.append(comments_temp)
                replies.append(replies_temp_1)
                likes.append(liked_users)
                posts.append(post)

            print(posts)
            print(comments)
            print(likes)
            print(replies)
            return HttpResponse("Feed Posted!")
        else:
            return HttpResponse("Login Required!")
