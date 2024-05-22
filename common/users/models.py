from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.base import BaseModel
from common.manager import CustomUserManager


class Gender(models.IntegerChoices):
    MALE = 1, _('Male')
    FEMALE = 2, _('Female')


class UserRole(models.IntegerChoices):
    ADMIN = 1, _('Admin')
    CLIENT = 2, _('Client')
    MANAGER = 3, _('Manager')


class User(AbstractUser, BaseModel):
    last_name = None  # type: ignore[assignment]
    first_name = None  # type: ignore[assignment]
    email = None

    name = models.CharField(_("Name of User"), max_length=255)
    phone = models.CharField(_("Phone Number"), max_length=14, unique=True, null=True, blank=True)
    birthday = models.DateField(_("Birthday"), blank=True, null=True, default=timezone.now)
    photo = models.ImageField(_("Photo of User"), upload_to="userImages", blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=UserRole.choices, default=UserRole.CLIENT)
    gender = models.PositiveSmallIntegerField(choices=Gender.choices, default=Gender.MALE)

    objects = CustomUserManager()

    EMAIL_FIELD = None
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name
