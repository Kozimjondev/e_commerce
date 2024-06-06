import random
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.validators import phone_number_validator

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
    username = None

    name = models.CharField(_("Name of User"), max_length=255)
    phone = models.CharField(_("Phone Number"), max_length=14, unique=True, null=True, blank=True,
                             validators=[phone_number_validator()])
    birthday = models.DateField(_("Birthday"), blank=True, null=True, default=timezone.now)
    photo = models.ImageField(_("Photo of User"), upload_to="userImages", blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=UserRole.choices, default=UserRole.CLIENT)
    gender = models.PositiveSmallIntegerField(choices=Gender.choices, default=Gender.MALE)

    objects = CustomUserManager()

    EMAIL_FIELD = None
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name


class Code(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userCode")
    code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.code

    def generate_code(self):
        number = str(random.randint(100000, 999999))
        self.code = number
        self.save()
        return self.code
