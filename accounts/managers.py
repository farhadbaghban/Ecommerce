from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, full_name, password):
        if not email:
            raise ValueError("user must have email")
        if not phone_number:
            raise ValueError("user must have phone_number")
        if not full_name:
            raise ValueError("user must have full_name")
        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, full_name, password):
        user = self.create_user(email, phone_number, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
