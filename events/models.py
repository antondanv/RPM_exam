from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    location = models.CharField(max_length=150, verbose_name="Локация")
    event_date = models.DateTimeField(verbose_name="Дата мероприятия")
    max_guests = models.IntegerField(verbose_name="Максимальное количество гостей")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")


    def __str__(self):
        return self.title
    
    def clean(self):
        if not self.title or not self.title.strip():
            raise ValidationError({'title': 'Название не может быть пустым'})
        if self.event_date and self.event_date < timezone.now():
            raise ValidationError({'event_date': 'Дата мероприятия должна быть в будущем'})
        if self.max_guests is not None and self.max_guests <= 0:
            raise ValidationError({'max_guests': 'Количество гостей должно быть больше нуля'})

        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
