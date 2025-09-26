"""Admin registrations for rusardhome."""

from django.contrib import admin

from .models import Article, ArticleLike, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at", "updated_at")
    search_fields = ("title", "content")
    list_filter = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author_name", "article", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("author_name", "author_email", "body")
    autocomplete_fields = ("article", "user")
    actions = ("approve_comments", "reject_comments")

    @admin.action(description="Approuver les commentaires sélectionnés")
    def approve_comments(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f"{count} commentaire(s) approuvé(s).")

    @admin.action(description="Retirer l'approbation des commentaires sélectionnés")
    def reject_comments(self, request, queryset):
        count = queryset.update(is_approved=False)
        self.message_user(request, f"{count} commentaire(s) mis en attente.")


@admin.register(ArticleLike)
class ArticleLikeAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "created_at")
    search_fields = ("article__title", "user__username")
    autocomplete_fields = ("article", "user")
