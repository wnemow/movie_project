from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model


User = get_user_model()


class Creator(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slug = models.SlugField(primary_key=True, blank=True, max_length=120)
    name = models.CharField(max_length=101, blank=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.last_name + ' ' + slugify(self.last_name) 
        if not self.slug:
            self.slug = slugify(self.first_name) + '_' + slugify(self.last_name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'Creator'
        verbose_name_plural = 'Creators'


class Movie(models.Model):
    STATUS_CHOICES = (
        ('archieve', 'Archived'),
        ('avail', 'Available')
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING
    )
    title = models.CharField(max_length=70)
    creator = models.ForeignKey(
        to=Creator,
        related_name='movie_creators',
        on_delete=models.CASCADE
    )
    desc = models.CharField(max_length=200)
    image = models.ImageField(upload_to='movie_images')
    year_publ = models.CharField(max_length=4)
    length = models.CharField(max_length=20,null=True)
    slug = models.SlugField(primary_key=True, blank=True, max_length=80)
    status = models.CharField(choices=STATUS_CHOICES, max_length=9)
    genre = models.ManyToManyField(
        to='Genre',
        related_name='movie_genre'
    )
    price_som = models.PositiveSmallIntegerField(null=True, default=0)   #
    movie_count = models.PositiveSmallIntegerField(null=True, default=1)   #

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class Genre(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING
    )
    genre =models.CharField(max_length=20, unique=True)
    slug = models.SlugField(primary_key=True, blank=True, max_length=25)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.genre)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.genre
    
    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = "Genres"
