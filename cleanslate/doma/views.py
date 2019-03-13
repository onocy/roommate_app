from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import EditProfileForm, EditChoreForm, CreateChoreForm, CreateUserForm, CreateHomeForm, EditUserForm, CreateTopicForm, EditTopicForm, CreateEventForm, EditHomeForm, EditEventForm
from doma.models import User, Profile, Home, Forum, Topic, Chore, Event#,Review, Reminder, Transaction, Village, Post,
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db import IntegrityError
from django.utils import timezone
import datetime

@login_required
def home(request):
    """
    View function for home page of site.
    """
    from itertools import zip_longest
    def grouper(iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)
    user_groups = list(grouper(Profile.objects.filter(home = request.user.profile.home), 2))

    message_board = request.user.profile.home.forum
    topics = Topic.objects.filter(forum = message_board).order_by('-created_on')
    topics = topics[:3]
    return render(
        request,
        'home.html',
        context = {
        #'num_topics': num_topics,
        'user_groups': user_groups,
        'topics': topics}
    )

@login_required
def forum(request):
    message_board = request.user.profile.home.forum
    topics = Topic.objects.filter(forum = message_board).order_by('-created_on')
    return render(
        request,
        'message_board.html',
        context={'topics': topics}
    )


@login_required
def profile(request):
    """
    View function for individual profiles on site.
    """
    if request.user.is_authenticated:
        chosen_user = User.objects.get(pk=request.user.id)
        status = chosen_user.profile.status
        lastSeen = chosen_user.profile.lastSeen
        bio = chosen_user.profile.bio
        email = chosen_user.email
        avatar = chosen_user.profile.avatar
        return render(
            request,
            'profile.html',
                context = {
                'username' : chosen_user.username,
                'status' : status,
                'bio': bio,
                'email': email,
                'lastSeen': lastSeen,
                'avatar': avatar,
            }
        )
    else:
        return render(
            request,
            'profile.html',
                context = {
                'username': "anonymous",
                'status': "Online",
                'bio': "This user has no bio",
                'email': ""
                }
        )
    return render(
        request,
        'profile.html',
        context={}
    )

@login_required
def calendar(request):
    """
    View function for Calendar
    """
    events = Event.objects.all()
    return render(
        request,
        'calendar.html',
        context={'events': events}
    )

@login_required
def reminders(request):
    """
    View function for reminders (Later- not a separate page)
    """
    events = Event.objects.all()
    #transactions = Transaction.objects.all()
    chores = Chore.objects.all()
    return render(
        request,
        'reminders_list.html',
        context={
                'events': events,
                #'transactions':transactions,
                'chores':chores
            }
    )

@login_required
def finance(request):
    """
    View function for reminders (Later- not a separate page)
    """
    finance = Transaction.objects.all()
    return render(
        request,
        'finance_list.html',
            context={
                'transactions': finance
            }
    )

@login_required
def edit_user_profile(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    new_profile=get_object_or_404(Profile, pk = pk)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_profile.phone = form.cleaned_data['phone']
            new_profile.yog = form.cleaned_data['yog']
            new_profile.major = form.cleaned_data['major']
            new_profile.status = form.cleaned_data['status']
            new_profile.bio = form.cleaned_data['bio']
            if form.cleaned_data['home']:
                new_profile.home = Home.objects.get(pk = form.cleaned_data['home'])
            if form.clean_avatar():
                new_profile.avatar = form.clean_avatar()
            if new_profile.save():
                messages.success(request, 'You successfully updated your profile settings.')
            return HttpResponseRedirect(reverse(profile))
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = EditProfileForm(initial=model_to_dict(new_profile))

    return render(request, 'form.html', {'form': form})

@login_required
def edit_chore(request, pk):
    updated_chore = get_object_or_404(Chore, pk = pk)
    if request.method == 'POST':
        form = EditChoreForm(request.POST)
        if form.is_valid():
            updated_chore.title = form.cleaned_data['title']
            updated_chore.description = form.cleaned_data['description']
            if form.clean_deadline():
                updated_chore.deadline = form.clean_deadline()
            updated_chore.save()

            return HttpResponseRedirect(reverse(reminders))
    else:
        form = EditChoreForm(initial=model_to_dict(updated_chore))
    return render(request, 'form.html', {'form': form, 'chore': updated_chore})

@login_required
def create_chore(request):
    if request.method == 'POST':
        form = CreateChoreForm(request.POST)
        if form.is_valid():
            chore = Chore.objects.create(
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                created_on = timezone.now(),
                deadline = form.cleaned_data['deadline']
            )
            if chore.save():
                messages.success(request, 'You successfully created a chore.')
            return HttpResponseRedirect(reverse(reminders))
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = CreateChoreForm()
    return render(request, 'form.html', {'form': form})

@login_required
def delete_chore(request, pk):
    if request.method == 'POST':
        chore = get_object_or_404(Chore, pk = pk)
        chore.delete()

        return HttpResponseRedirect(reverse(reminders))
    return render(request, 'chore_delete_form.html', {})

def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                new_user = User.objects.create_user(username = form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
                messages.success(request, 'You successfully created a new user. Sign in now.')
                return HttpResponseRedirect(reverse(profile))
            except IntegrityError as e:
                messages.error(request, "You have not met Django's built in attribute requirements. Try using a stronger password and a longer username.")
                return render(request, 'form.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors in the form.')
            return render(request, 'form.html', {'form': form})
    else:
        form = CreateUserForm()
    return render(request, 'form.html', {'form': form})

def edit_user(request, pk):
    updated_user = User.objects.filter(pk = pk)[0]
    if request.method == 'POST':
        form = EditUserForm(request.POST)
        if form.is_valid():
            updated_user.username = form.cleaned_data['username']
            updated_user.email = form.cleaned_data['email']
            updated_user.set_password(form.cleaned_data['password'])
            if updated_user.save():
                update_session_auth_hash(request, updated_user)
                messages.success(request, 'You successfully updated your account settings.')
            return HttpResponseRedirect(reverse(profile))
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = EditUserForm(initial = model_to_dict(updated_user))
    return render(request, 'form.html', {'form': form})

@login_required
def create_home(request):
    if request.method == 'POST':
        form = CreateHomeForm(request.POST)
        if form.is_valid():
            new_home = Home.objects.create(name = "", address = "", created_by = request.user.profile)
            new_home.name = form.cleaned_data['name']
            new_home.address = form.cleaned_data['address']
            new_home.leaseStart = form.cleaned_data['leaseStart']
            new_home.leaseEnds = form.cleaned_data['leaseEnds']
            new_home.save()
            request.user.profile.home = new_home
            request.user.profile.save()
            return HttpResponseRedirect(reverse(home))
    else:
        form = CreateHomeForm()
    return render(request, 'form.html', {'form': form})

@login_required
def edit_home(request, pk):
    updated_home = Home.objects.filter(pk = pk)[0]
    if request.method == 'POST':
        form = EditHomeForm(request.POST)
        if form.is_valid():
            updated_home.name = form.cleaned_data['name']
            updated_home.address = form.cleaned_data['address']
            updated_home.leaseStart = form.cleaned_data['leaseStart']
            updated_home.leaseEnds = form.cleaned_data['leaseEnds']
            if updated_home.save():
                messages.success(request, 'You successfully updated the home.')
            return HttpResponseRedirect(reverse(home))
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = EditHomeForm(initial = model_to_dict(updated_home))
    return render(request, 'form.html', {'form': form})

@login_required
def create_topic(request):
    if request.method == 'POST':
        form = CreateTopicForm(request.POST)
        if form.is_valid():
            new_topic = Topic.objects.create(
                title = form.cleaned_data['title'],
                content = form.cleaned_data['content'],
                forum = request.user.profile.home.forum,
                created_by = request.user.profile,
                created_on = timezone.now()
            )
            if new_topic.save():
                messages.success(request, 'You successfully created a new topic.')
            return HttpResponseRedirect(reverse(home))
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = CreateTopicForm()
    return render(request, 'form.html', {'form': form})

@login_required
def edit_topic(request, pk):
    updated_topic = Topic.objects.filter(pk = pk)[0]
    if request.method == 'POST':
        form = EditTopicForm(request.POST)
        if form.is_valid():
            updated_topic.title = form.cleaned_data['title']
            updated_topic.content = form.cleaned_data['content']
            if updated_topic.save():
                messages.success(request, 'You successfully updated the topic.')
            return HttpResponseRedirect(reverse(home))
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = EditTopicForm(initial = model_to_dict(updated_topic))
    return render(request, 'form.html', {'form': form})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            new_event = Event.objects.create(
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                start_time = form.cleaned_data['start_time'],
                end_time = form.cleaned_data['end_time'],
                home = request.user.profile.home,
                created_on = timezone.now()
            )
            if new_event.save():
                messages.success(request, 'You successfully created a new event.')
            return HttpResponseRedirect(reverse(calendar))
        else:
            messages.error(request, 'Please correct the errors in the form')
    else:
        form = CreateEventForm()
    return render(request, 'form.html', {'form': form})

@login_required
def edit_event(request, pk):
    updated_event = Event.objects.filter(pk = pk)[0]
    if request.method == 'POST':
        form = EditEventForm(request.POST)
        if form.is_valid():
            updated_event.title = form.cleaned_data['title']
            updated_event.description = form.cleaned_data['description']
            updated_event.start_time = form.cleaned_data['start_time']
            updated_event.end_time = form.cleaned_data['end_time']
            if updated_event.save():
                messages.success(request, 'You successfully updated the event.')
            return HttpResponseRedirect(reverse(reminders))
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = EditEventForm(initial = model_to_dict(updated_event))
    return render(request, 'form.html', {'form': form})
