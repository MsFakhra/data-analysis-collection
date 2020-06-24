from django.contrib import admin
from .models import Users
from .models import Posts
from .models import Comment
from .models import Picture

# Register your models here.
admin.site.register(Users)
admin.site.register(Posts)
admin.site.register(Comment)
admin.site.register(Picture)
