from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_choices = (
        ('a', 'Admin'),
        ('u', 'User')
    )
    STATUSES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('busy', 'Busy'),
        ('vacation', 'On Vacation')
    )
    phone = models.CharField(max_length=10, help_text='Enter your phone number', null=True, blank=True)
    yog = models.CharField(max_length=100, help_text='Enter your graduation date', null=True, blank=True)
    major = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=1, choices=role_choices, default='u')
    status = models.CharField(max_length=8, help_text='Select a status for others to view', default='online', choices=STATUSES)
    bio = models.TextField(max_length=1000, help_text='Enter a brief description of yourself', blank=True)
    lastSeen = models.DateTimeField(null=True)
    home = models.ForeignKey('Home', on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/upload/', default='avatars/default.png', blank=True)
    #smokes = models.BooleanField(default=False, help_text='Do you smoke cigarettes?')
    #bedtime = models.TimeField(null=True, blank=True, help_text='What is your usual sleep-time?')
    #pet_allergies = models.NullBooleanField(null=True, blank=True, help_text='Are you allergic to pets?')

    def is_admin(self):
        return self.role in 'a'

    def has_home(self):
        return self.home is not None

    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])

    def __str__(self):
        return '%s' % (self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Home(models.Model):
    created_by = models.ForeignKey('Profile', null=False, related_name="home_created_by")
    name = models.CharField(max_length=100, help_text='Enter your Home Name')
    address = models.CharField(max_length=100, help_text='Enter your Address', null=True)
    leaseStart = models.DateField(null=True, blank=True)
    leaseEnds = models.DateField(null=True, blank=True)
    #village = models.ForeignKey('Village', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('home-detail', args=[str(self.id)])

    def __str__(self):
        return "Home: {}".format(self.name)

class Topic(models.Model):
    title = models.CharField(max_length=200, help_text="Enter a topic name")
    content = MarkdownxField()
    forum = models.ForeignKey('Forum', on_delete=models.CASCADE, null=False, related_name='topics')
    created_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField()

    @property
    def formatted_markdown(self):
        return markdownify(self.content)

    def __str__(self):
        return 'Topic: %s' % self.title

    def get_absolute_url(self):
        return reverse('topic-detail', args=[str(self.id)])

class Forum(models.Model):
    title = models.CharField(max_length=200, help_text="Enter a forum name")
    description = models.TextField(max_length=1000, help_text='Enter a description for this forum')
    home = models.OneToOneField('Home', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('forum-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

@receiver(post_save, sender=Home)
def create_home_forum(sender, instance, created, **kwargs):
    if created:
        Forum.objects.create(home=instance)

@receiver(post_save, sender=Home)
def save_home_forum(sender, instance, **kwargs):
    instance.forum.title = instance.name
    instance.forum.save()

class Chore(models.Model):
    title = models.CharField(max_length=200, help_text='Enter a chore name')
    description = models.CharField(max_length=500, help_text='Enter description')
    created_on = models.DateField()
    deadline = models.DateField(help_text='When is this chore due?')
    #owners

    @property
    def almost_due(self):
        if (self.deadline - timezone.now().date()).days < 2:
            return True
        else:
            return False

    def __str__(self):
        return 'Chore: %s' % self.title

    def get_absolute_url(self):
        return reverse('chore-detail', args=[str(self.id)])

class Event(models.Model):
    title = models.CharField(max_length=200, help_text='Enter an event name')
    description = models.CharField(max_length=500, help_text='Enter description')
    created_on = models.DateTimeField()
    start_time = models.DateField(help_text='When is this event going to start?')
    end_time = models.DateField(help_text='When is this event going to end?')
    home = models.ForeignKey('Home', on_delete=models.CASCADE, related_name='events')

    @property
    def almost_due(self):
        if (self.end_time - self.start_time).days < 2:
            return True
        else:
            return False

    def __str__(self):
        return 'Event: %s' % self.title

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])

# Unfinished / unimplemented models

#class Post(models.Model):
#    title = models.CharField(max_length=200, help_text='Enter a post name')
#    content = models.CharField(max_length=500, help_text='Enter content')
#    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)
#    created_by = models.ForeignKey('Profile', on_delete=models.CASCADE, null=False, related_name='op')
#    created_on = models.DateTimeField()

#    def __str__(self):
#        return 'Post: %s' % self.title

#    def get_absolute_url(self):
#        return reverse('post-detail', args=[str(self.id)])

#class Transaction(models.Model):
#    title = models.CharField(max_length=200, help_text='Enter a transaction name')
#    description = models.CharField(max_length=500, help_text='Enter description')
#    created_on = models.DateField()
#    deadline = models.DateField(help_text='When is this transaction due?')
#    amount = models.IntegerField()
    # debtors
    # creditors
    # change 'amount' issue with whole numbers
    # transaction split 

#    def __str__(self):
#        return 'Transaction: %s' % self.title

#    def get_absolute_url(self):
#        return reverse('transaction-detail', args=[str(self.id)])

#class Reminder(models.Model):
#    title = models.CharField(max_length=200, help_text='Enter a reminder name')
#    description = models.CharField(max_length=500, help_text='Enter description')
#    created_on = models.DateField()
#    deadline = models.DateField(help_text='When is this reminder due?')
    # owners

#    def __str__(self):
#        return 'Reminder: %s' % self.title

#    def get_absolute_url(self):
#        return reverse('reminder-detail', args=[str(self.id)])

#class Village(models.Model):
#    title = models.CharField(max_length=200, help_text="Enter a village name")
#    forum = models.OneToOneField('Forum', on_delete=models.CASCADE, null=False, default=1)

#    def __str__(self):
#        return 'Village: %s' % self.title

#    def get_absolute_url(self):
#        return reverse('village-detail', args=[str(self.id)])

#class Review(models.Model):
#    reviewed = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, related_name='reviewed_user')
#    reviewedBy = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewer') # added blank option for anonyomous reviews. Maybe changed later
#    review = models.TextField(max_length=1000, help_text='Enter your review here', default='')

#    def get_absolute_url(self):
#        return reverse('home-detail', args=[str(self.id)])

#    def __str__(self):
#        return '%s reviewed %s' % (self.reviewedBy, self.reviewed)
