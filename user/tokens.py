import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()


# <!-- SECOND VERSION -->
# <!-- <div style="background-color: #c2c2c2; padding: 15px;">
#     <h2 style="margin: 0; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: #5865F2; color: #ffffff;">Verify Email</h2>
#     <div style="margin: 0; padding: 15px; background-color: #ffffff;">
#         <p>Hi {{ user.name }},</p>
#         <p>You created an account on Delight.com, you need to verify your email. Please click on the button below to verify your email.</p>
#         <a href="{{ request.scheme }}://{{ domain }}{% url 'verify-email-confirm' uidb64=uid token=token %}" style="border: 0; color: #ffffff; background-color: #5865F2; padding: 15px; font-weight: bold; text-decoration: none; border-radius: 5px;">
#             Verify Email
#         </a>
#         <p style="margin-top: 40px;">Or you can copy the link below to your browser</p>
#         <p>{{ request.scheme }}://{{ domain }}{% url 'verify-email-confirm' uidb64=uid token=token %}</p>
#         <p>The Delight Team</p>
#     # <!-- </div> --> -->