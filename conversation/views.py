from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from items.models import Item

from .forms import ConversationMessageForm
from .models import Conversation


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    # If the owner, then the user shouldnt have access to the page.
    if item.seller == request.user:
        return redirect('dashboard:index')
    # This will get all conversations related to the item, where the user is a member
    conversations = Conversation.objects.filter(
        item=item).filter(members__in=[request.user.id])

    # If there is a conversation on before, this will redirect to that conversation instead of starting a new one.
    if conversations:
        # pass
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            # This adds the seccond user
            conversation.members.add(request.user)
            conversation.members.add(item.seller)  # This adds the owner
            conversation.save()

            conversation_message = form.save(commit=False)
            # This points to the conversation
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('items:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        'form': form
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })


@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(
        members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })
