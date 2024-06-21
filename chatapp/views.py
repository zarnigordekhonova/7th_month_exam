from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from chatapp.forms import UserMessageForm, EditMessageForm
from chatapp.models import UserMessage
from Users.models import CustomUser
from django.views import View
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseForbidden
# Create your views here.


class UsersListView(View):
    def get(self, request):
        owner = request.user
        users = get_user_model().objects.exclude(id=owner.id)

        context = {
            'users': users
        }
        return render(request, 'Chat/homepage.html', context=context)


def about_us(request):
    return render(request, 'Chat/about.html')

class UserMessagesView(View):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        send_message = UserMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=request.user))
        ).order_by('-created_at')
        form = UserMessageForm()

        other_users = CustomUser.objects.exclude(id=request.user.id)
        user_last_messages = []
        for other_user in other_users:
            last_message = UserMessage.objects.filter(
                (Q(sender=request.user) & Q(receiver=other_user)) | (Q(sender=other_user) & Q(receiver=request.user))
            ).order_by('-created_at').first()
            user_last_messages.append((other_user, last_message))

        context = {
            'user': user,
            'form': form,
            'send_message': send_message,
            'user_last_messages': user_last_messages,
        }
        return render(request, 'Chat/user_messages.html', context=context)

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        form = UserMessageForm(request.POST, request.FILES)
        if form.is_valid():
            send_message = form.save(commit=False)
            send_message.sender = request.user
            send_message.receiver = user
            send_message.save()
            return redirect('chat:to_user', pk=pk)

        send_message = UserMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=request.user))
        ).order_by('-created_at')

        other_users = CustomUser.objects.exclude(id=request.user.id)
        user_last_messages = []
        for other_user in other_users:
            last_message = UserMessage.objects.filter(
                (Q(sender=request.user) & Q(receiver=other_user)) | (Q(sender=other_user) & Q(receiver=request.user))
            ).order_by('-created_at').first()
            user_last_messages.append((other_user, last_message))

        context = {
            'user': user,
            'form': form,
            'send_message': send_message,
            'user_last_messages': user_last_messages,
        }
        return render(request, 'Chat/user_messages.html', context=context)


# class SearchView(View):
#     def get(self, request):
#         query = request.GET.get('q', '').strip()
#         if query:
#             followers = CustomUser.objects.filter(
#                 Q(username__icontains=query) |
#                 Q(first_name__icontains=query) |
#                 Q(last_name__icontains=query)
#             )
#         else:
#             followers = CustomUser.objects.none()
#
#         context = {
#             'followers': followers,
#             'query': query
#         }
#
#         return render(request, 'Chat/search_results.html', context=context)


class EditMessageView(View):
    def get(self, request, pk):
        message = get_object_or_404(UserMessage, pk=pk)
        if not message.user_auth(request.user):
            messages.error(request, "Siz bu xabarni tahrirlay olmaysiz!")
            return redirect('chat:to_user', pk=message.receiver.pk)

        edit_message_form = EditMessageForm(instance=message)
        context = {
            'edit_message_form': edit_message_form,
            'message': message,
        }
        return render(request, 'Chat/edit_message.html', context=context)

    def post(self, request, pk):
        message = get_object_or_404(UserMessage, pk=pk)
        if not message.user_auth(request.user):
            messages.error(request, "Siz bu xabarni tahrirlay olmaysiz!")
            return redirect('chat:to_user', pk=message.receiver.pk)

        edit_message_form = EditMessageForm(request.POST, instance=message)
        if edit_message_form.is_valid():
            edit_message_form.save()
            messages.success(request, "Xabar muvaffaqiyatli tahrirlandi.")
            return redirect('chat:to_user', pk=message.receiver.pk)

        context = {
            'edit_message_form': edit_message_form,
            'message': message,
        }
        return render(request, 'Chat/edit_message.html', context=context)


class DeleteMessageView(View):
    def post(self, request, pk):
        message = get_object_or_404(UserMessage, pk=pk)
        if message.sender == request.user:
            message.delete()
            return redirect('chat:to_user', pk=message.receiver.pk)
        else:
            return HttpResponseForbidden('Siz bu xabarni o\'chira olmaysiz!')