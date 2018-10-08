from django.contrib import admin
from search.models import User, Search


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username', 'repos', 'followers', 'type', 'user_thumb')
    search_fields = list_display[:-1]
    list_filter = ('type',)


class SearchAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Search, SearchAdmin)
