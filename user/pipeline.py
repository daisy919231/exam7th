from user.models import CustomUser
from django.core.exceptions import ValidationError

def create_user(backend, uid, user=None, *args, **kwargs):
    if user is None:
        # Assuming that 'response' contains an 'email' field.
        response = kwargs.get('response')
        email = response.get('email')

        # Check if email is provided
        if not email:
            raise ValidationError("Email address is required.")

        # Create the user with the email address
        user = CustomUser.objects.create_user(username=uid, email=email)

    return user