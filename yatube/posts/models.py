from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(verbose_name="Назавние группы",
                             max_length=200)
    slug = models.SlugField(verbose_name="Уникальная slug сылка",
                            unique=True)
    description = models.TextField(verbose_name="Описнаие группы")

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='posts')
    group = models.ForeignKey(Group,
                              verbose_name='Группы',
                              blank=True,
                              null=True,
                              related_name='posts_group',
                              on_delete=models.SET_NULL, )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{str(self.text)[:15]}'
