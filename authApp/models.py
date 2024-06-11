from django.db import models
from uuid import uuid4
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class Team(models.Model):
    team_name = models.CharField(max_length=100, null=False)
    team_type = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.team_name

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, username, password=None, password2=None):
        if not email:
            raise ValueError("User must have an email address")
        elif not phone:
            raise ValueError("User must have an phone number")
        elif not username:
            raise ValueError("User must have an username")

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, username,password=None, password2=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone=phone
        )
        user.is_admin = True
        # team = Team.objects.create(team_name=team_name, team_type=team_type)
        # user.team = team
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, unique=True)
    username = models.CharField(max_length=20, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Add this field
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    team = models.ForeignKey(Team, related_name='team', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin