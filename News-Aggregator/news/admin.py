from django.contrib import admin
from .models import Headline,EHeadline,SHeadline,PHeadline,LHeadline,ENHeadline,Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'headline__title', 'content')
    ordering = ('-created_at',)

admin.site.register(Headline)
admin.site.register(EHeadline)
admin.site.register(SHeadline)
admin.site.register(PHeadline)
admin.site.register(LHeadline)
admin.site.register(ENHeadline)

