from pyexpat import model

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
    ]

    customer_name = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    order_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.customer_name or not self.customer_name.strip():
            raise ValidationError({'customer_name': 'Имя покупателя не может быть пустым'})
        if not self.product_name or not self.product_name.strip():
            raise ValidationError({'product_name': 'Название продукта не может быть пустым'})
        if self.quantity is not None and self.quantity <= 0:
            raise ValidationError({'quantity': 'Количество должно быть больше нуля'})
        if self.order_date and self.order_date > timezone.now().date():
            raise ValidationError({'order_date': 'Дата заказа не может быть в будущем'})
        
        valid_statuses = [choice[0] for choice in self.STATUS_CHOICES]
        if self.status not in valid_statuses:
            raise ValidationError({'status': f'Статус должен быть одним из: {", ".join(valid_statuses)}'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.customer_name} - {self.product_name} ({self.status})'
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'