from django.urls import path
from .views import UsersListView, UserMessagesView, about_us, EditMessageView, DeleteMessageView


app_name = 'chat'
urlpatterns = [
    path('', UsersListView.as_view(), name='homepage'),
    path('message/<int:pk>/user', UserMessagesView.as_view(), name='to_user'),
    path('about/', about_us, name='about'),
    path('edit/<int:pk>/message/', EditMessageView.as_view(), name='edit'),
    path('delete/<int:pk>/message/', DeleteMessageView.as_view(), name='delete'),
]