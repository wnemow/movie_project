from django.db import models
from django.contrib.auth import get_user_model
from apps.movie.models import Movie
User = get_user_model()
class MoviePurchases(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('finished', 'Finished')
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='orders'
    )
    book = models.ManyToManyField(
        to=Movie,
        through='OrderItems',
    )
    order_id = models.CharField(max_length=58, blank=True)
    total_sum = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order # {self.order_id}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.order_id:
            self.order_id = str(self.user.username) + str(self.total_sum)
        return self.order_id
    
    class Meta:
        verbose_name = 'Movie order'
        verbose_name_plural = 'Movies orders'

class OrderItems(models.Model):
    order = models.ForeignKey(
        to=MoviePurchases,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True
    )
    movie = models.ForeignKey(
        to=Movie,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True
    )
    movie_num = models.PositiveBigIntegerField(default=1)

    class Meta:
        verbose_name = 'Basket item'
        verbose_name_plural = 'Basket items'