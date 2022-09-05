from django.contrib import admin

from .models import (
    Resource,
    Tag,
    News,
)


admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(News)