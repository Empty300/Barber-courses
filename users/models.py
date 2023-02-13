import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    STANDARD = 0
    LIGHT = 1
    OPTIMAL = 2
    FULL = 3
    STATUSES = (
        (STANDARD, 'Не оплачен'),
        (LIGHT, 'Лайт'),
        (OPTIMAL, 'Оптимальный'),
        (FULL, 'Полный'),
    )

    email = models.EmailField(blank=False, unique=True)
    is_verified_email = models.BooleanField(default=False)
    status = models.SmallIntegerField(default=STANDARD, choices=STATUSES)

    def save(self, *args, **kwargs):

        super(User, self).save(*args, **kwargs)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=self, expiration=expiration)
        record.send_verification_email()


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()



    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи {} перейдите по ссылке: {}'.format(
            self.user.username,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
