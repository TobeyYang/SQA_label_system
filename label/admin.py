from django.contrib import admin
from label.models import Table, Query, Mention, FollowUp
# Register your models here.

admin.site.register((Table, Query, Mention, FollowUp))
