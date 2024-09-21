from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            first_name=first_name,
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    first_name = models.CharField(
        max_length=123,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=123,
        verbose_name='Фамилия',
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name='Номер телефона',
        unique=True
    )
    wallet = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Баланс',
        default=0.00
    )
    created_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Обычный пользователь'),
            (2, 'Менеджер'),
            (3, 'Бухгалтер')
        ),
        default=1,
        verbose_name='Статус пользователя'
    )
    cover = models.ImageField(
        upload_to='media/user_covers/',
        blank=True,
        null=True,
        verbose_name='Фото профиля'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Почта пользователя'
    )
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'email']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin

    @property
    def full_name(self):
        if self.last_name:
            return f"{self.last_name} {self.first_name}"
        return self.first_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
