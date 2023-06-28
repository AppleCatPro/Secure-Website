from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    gender = models.CharField(verbose_name='Гендер',
                              max_length=10,
                              choices=[('Ж', "Женский"), ('М', "Мужской")],
                              default='М')
    is_verified = models.BooleanField(verbose_name='is_verified', default=False)

    encryption_key = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class ConfidentialData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_encrypted = models.BooleanField(default=False)

    encryption_key = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        verbose_name = 'Confidential Data'
        verbose_name_plural = 'Confidential Data'

    def __str__(self):
        return f'Confidential Data #{self.id}'


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    success = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        return f'Audit Log #{self.id}'
