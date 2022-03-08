from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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


class Post(models.Model):
    text = models.TextField('Текст поста')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )
    group = models.ForeignKey(
        Group,
        related_name='group_posts',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Группа'
    )

    def __str__(self):
        return self.text


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

    following = models.ForeignKey(
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
                fields=('user', 'following'),
                name='%(app_label)s_%(class)s_user-follow-constraint'
            ),
        ]

    def __str__(self):
        return self.user.username
