from django.contrib import admin
from .models import Post, Author, Category, Comment
from modeltranslation.admin import TranslationAdmin


class TranslatedPostAdmin(TranslationAdmin):
    model = Post


class TranslatedCommentAdmin(TranslationAdmin):
    model = Comment


class CategoryAdmin(TranslationAdmin):
    model = Category


admin.site.register(Author)
admin.site.register(Post, TranslatedPostAdmin)
admin.site.register(Comment, TranslatedCommentAdmin)
admin.site.register(Category, CategoryAdmin)
