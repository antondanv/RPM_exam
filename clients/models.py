from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Client(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Полное имя")
    email = models.EmailField(max_length=100, unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Телефон",
    )
    registration_date = models.DateField(
        default=timezone.localdate,
        verbose_name="Дата регистрации",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['phone'],
                condition=~Q(phone=''),
                name='unique_non_empty_client_phone',
            )
        ]

    def __str__(self):
        return self.full_name

    def clean(self):
        errors = {}

        self.full_name = (self.full_name or '').strip()
        self.email = (self.email or '').strip().lower()
        self.phone = (self.phone or '').strip()

        if not self.full_name:
            errors['full_name'] = 'Полное имя клиента не может быть пустым.'

        if self.email:
            domain = self.email.split('@')[-1]
            if '@' not in self.email or '.' not in domain:
                errors['email'] = 'Email должен содержать @ и домен с точкой.'

            email_exists = Client.objects.filter(email=self.email).exclude(pk=self.pk).exists()
            if email_exists:
                errors['email'] = 'Клиент с таким email уже существует.'

        if self.phone:
            phone_exists = Client.objects.filter(phone=self.phone).exclude(pk=self.pk).exists()
            if phone_exists:
                errors['phone'] = 'Клиент с таким телефоном уже существует.'

        if self.registration_date and self.registration_date > timezone.localdate():
            errors['registration_date'] = 'Дата регистрации не может быть больше текущей даты.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
