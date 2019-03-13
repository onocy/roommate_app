from django.contrib import admin

from .models import Profile
from .models import Home
from .models import Forum
from .models import Topic
from .models import Chore
from .models import Event
#from .models import Review
#from .models import Reminder
#from .models import Transaction
#from .models import Post
#from .models import Village

admin.site.register(Profile)
admin.site.register(Home)
admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Chore)
admin.site.register(Event)
#admin.site.register(Review)
#admin.site.register(Reminder)
#admin.site.register(Transaction)
#admin.site.register(Post)
#admin.site.register(Village)
