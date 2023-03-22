from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, DateTimeField
from django.core.cache import cache
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        s_rating = self.post_set.aggregate(postRating=Sum('rating'))
        psrating = 0
        psrating += s_rating.get('postRating')

        comment_rating = self.user.comment_set.aggregate(commentRating=Sum('rating'))
        c_rating = 0
        c_rating += comment_rating.get('commentRating')

        self.ratingAuthor = s_rating * 3 + c_rating
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, max_length=128, blank=True, related_name='categories')

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    Author = models.ForeignKey(Author, on_delete=models.CASCADE)
    News = 'N'
    Article = 'A'
    CATEGORY_CHOICES = (
        (News, 'News'),
        (Article, 'Article'),
    )

    categoryContent = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default=Article)
    date = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=64)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    def get_absolute_url(self):
        return reverse('news', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'news-{self.pk}')

    def __str__(self):
        return f'{self.categoryContent,self.CATEGORY_CHOICES}'


class PostCategory(models.Model):
    through_Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    through_Category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

