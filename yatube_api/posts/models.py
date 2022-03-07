from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200
    )
    slug = models.SlugField(
        'slug группы',
        unique=True
    )
    description = models.TextField('Описание')

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        blank=True,
        null=True,
        verbose_name='Подписчик',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        blank=True,
        null=True,
        verbose_name='Автор',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='%(app_label)s_%(class)s_user-follow-constraint'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='could_not_follow_itself'
            )

        ]

    def __str__(self):
        return self.user.username