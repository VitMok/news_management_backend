from django.db import models


class Resource(models.Model):
    """ Русурс """
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название ресурса'
    )

    class Meta:
        db_table = 'resources'
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'

    def __str__(self):
        return self.name

class Tag(models.Model):
    """ Внутренний тэг новости """
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название тэга'
    )
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]
    class Meta:
        db_table = 'tags'
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name

class News(models.Model):
    """ Новость """
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Ресурс'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг'
    )
    date = models.DateField(
        verbose_name='Новостная дата',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title