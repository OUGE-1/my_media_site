from django.db import models

class Collection(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='合集名称')
    description = models.TextField(blank=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合集'
        verbose_name_plural = '合集'

class Video(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='videos/')
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='videos',
        verbose_name='所属合集'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Audio(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='audio/')
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audios',
        verbose_name='所属合集'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
