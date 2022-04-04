from django.db import models
from django.contrib.sessions.models import Session

STATUS_NEW = 'new'
STATUS_MODERATED = 'moderated'
STATUS_CHOICES = (
    (STATUS_NEW, 'New'),
    (STATUS_MODERATED, "Moderated")
)

DEFAULT_STATUS = STATUS_NEW


class Quote(models.Model):
    text = models.TextField(max_length=200, verbose_name='Text')
    author = models.CharField(max_length=100, verbose_name="Author")
    email = models.EmailField(verbose_name='E-mail')
    rating = models.IntegerField(default=0, verbose_name='Rating')
    status = models.CharField(max_length=15, verbose_name='Status', choices=STATUS_CHOICES, default=DEFAULT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    @classmethod
    def get_moderated(cls):
        return cls.objects.filter(status=STATUS_MODERATED)

    def __str__(self):
        return f'{self.text[:20]}'

    class Meta:
        verbose_name = 'Quote'
        verbose_name_plural = 'Quotes'
        ordering = ('-created_at',)


class Vote(models.Model):
    session_key = models.CharField(max_length=40, verbose_name='Session key')
    quote = models.ForeignKey('webapp.Quote', related_name='votes', on_delete=models.CASCADE, verbose_name='Quote')
    rating = models.IntegerField(choices=((1, 'up',), (-1, 'down')), verbose_name='Rating')

    def __str__(self):
        return f'{self.quote}: {self.rating}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        ordering = ('quote', 'rating')