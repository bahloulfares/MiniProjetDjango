from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentListView,
    SignUpView,
    login_view,
    logout_view,
    custom_password_reset,
    index,
    add_like,
    delete_like,
    post_confirm_delete,
    comment_delete,
    AddCommentView,
    UserPostListView,
    UserPostUpdateView,
)


urlpatterns = [
    path('postlist/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('login/', login_view, name='login'),
    path('', index, name='index'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', custom_password_reset, name='password_reset'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('index/', index, name='acceuil'),
    path('add_like/<int:post_id>/', add_like, name='add_like'),
    path('post/<int:post_id>/unlike/', delete_like, name='delete_like'),  # Corrigez l'import de la vue
    path('post_confirm_delete/', post_confirm_delete, name='post_confirm_delete'),
    path('comments/', CommentListView.as_view(), name='comment_list'),  # Décommentez cette ligne
    path('comments/delete/<int:comment_id>/', comment_delete, name='comment_delete'),
    path('post/<int:post_id>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('my-posts/', UserPostListView.as_view(), name='user_posts'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/update/', UserPostUpdateView.as_view(), name='user_post_update'),

]
