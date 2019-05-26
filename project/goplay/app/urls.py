from  django.urls import path
import app.views as views

urlpatterns = [
        path('login/', views.LoginView.as_view()),
        path('signup/', views.SignUpView.as_view()),
        path('forgotpassword/', views.ForgotPasswordView.as_view()),
        path('logout/', views.ForgotPasswordView.as_view()),
        path('post_image/', views.PostImageView.as_view()),
        path('comment/<int:pk>', views.CommentView.as_view()),
        path('reply/<int:pk>', views.ReplyView.as_view()),
        path('like/<int:pk>', views.LikePost.as_view()),
        path('feed', views.Feed.as_view()),
        ]
