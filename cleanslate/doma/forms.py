from django import forms
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from .models import User, Home, Forum, Topic, Chore, Event, Profile # Village, Transaction, Review, Reminder, Post,
from markdownx.fields import MarkdownxFormField

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'yog', 'major', 'bio', 'status']
    HOMES = [(None, '')]
    for home in Home.objects.all():
        HOMES += [(home.id, home.name)]
    home = forms.ChoiceField(help_text='Which home do you want to be in?', choices=HOMES, required=False)
    avatar = forms.ImageField(required=False)

    def clean_avatar(self):
        if self.cleaned_data['avatar']:
            avatar = self.cleaned_data['avatar']
            try:
                w, h = get_image_dimensions(avatar)
                max_width = max_height = 250
                if w > max_width or h > max_height:
                    raise forms.ValidationError(
                        "Please use an image that is {} x {} pixels or smaller.".format(max_width, max_height)
                    )
                main, sub = avatar.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'gif', 'png']):
                    raise forms.ValidationError(
                        "Please use a JPEG, GIF or PNG image."
                    )
                if len(avatar) > (1000 * 1024):
                    raise forms.ValidationError(
                        u'Avatar file size may not exceed 50k.')
            except AttributeError:
                """
                Handles case when we are updating the user profile
                and do not supply a new avatar
                """
                pass
            return avatar
        else:
            return None

class EditChoreForm(forms.Form):
    title = forms.CharField(help_text = 'Enter a chore name')
    description = forms.CharField(help_text = 'Enter a description')
    deadline = forms.DateField(help_text = 'When is this chore due?', widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_deadline(self):
        if self.cleaned_data['deadline'] < datetime.date.today():
            raise ValidationError(_('Invalid date - deadline cannot be in the past'))
        return self.cleaned_data['deadline']

class CreateChoreForm(forms.Form):
    title = forms.CharField(help_text = 'Enter a chore name')
    description = forms.CharField(help_text = 'Enter a description')
    deadline = forms.DateField(help_text = 'When is this chore due?', widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_title(self):
        data = self.cleaned_data['title']
        # Check title is not longer than 200 characters
        if len(data) > 200:
            raise ValidationError(_('Invalid title - cannot be longer than 200 characters'))
        return data

    def clean_description(self):
        data = self.cleaned_data['description']
        # Check description is not longer than 500
        if len(data) > 500:
            raise ValidationError(_('Invalid description - cannot be longer than 500 characters'))
        return data

    def clean_created_on(self):
        data = self.cleaned_data['created_on']
        # Check date is not in future.
        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - created_on cannot be in the future'))
        return data

    def clean_deadline(self):
        data = self.cleaned_data['deadline']
        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - deadline cannot be in the past'))
        return data

class CreateUserForm(forms.Form):
    username = forms.CharField(help_text = 'Enter a username')
    email = forms.EmailField(help_text = 'Enter an email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User

class EditUserForm(forms.Form):
    username = forms.CharField(help_text = 'Enter a username')
    email = forms.EmailField(help_text = 'Enter an email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User

class CreateHomeForm(forms.Form):
    name = forms.CharField(max_length=100, help_text='Enter your Home Name')
    address = forms.CharField(max_length=100, help_text='Enter your Address')
    leaseStart = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    leaseEnds = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class EditHomeForm(forms.Form):
    name = forms.CharField(max_length=100, help_text='Enter your Home Name')
    address = forms.CharField(max_length=100, help_text='Enter your Address')
    leaseStart = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    leaseEnds = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class CreateTopicForm(forms.Form):
    title = forms.CharField(help_text='Enter a topic name')
    content = MarkdownxFormField(help_text='Enter the content of the topic. You can use markdown (e.g. ###H3 Header)')

class EditTopicForm(forms.Form):
    title = forms.CharField(help_text='Enter a topic name')
    content = MarkdownxFormField(help_text='Enter the content of the topic. You can use markdown (e.g. ###H3 Header)')

class CreateEventForm(forms.Form):
    title = forms.CharField(help_text='Enter an event name')
    description = forms.CharField(widget=forms.Textarea, help_text='Enter a description of the event')
    start_time = forms.DateField(help_text='When is this event going to start?', widget=forms.DateInput(attrs={'type': 'date'}))
    end_time = forms.DateField(help_text='When is this event going to end?', widget=forms.DateInput(attrs={'type': 'date'}))

class EditEventForm(forms.Form):
    title = forms.CharField(help_text='Enter an event name')
    description = forms.CharField(widget=forms.Textarea, help_text='Enter a description of the event')
    start_time = forms.DateField(help_text='When is this event going to start?', widget=forms.DateInput(attrs={'type': 'date'}))
    end_time = forms.DateField(help_text='When is this event going to end?', widget=forms.DateInput(attrs={'type': 'date'}))
