import re
from django.core.exceptions import ValidationError

def validate_password_strength(password):
    """
    Validate password complexity requirements.

    Password must meet the following criteria:
    - At least 8 characters long.
    - Contains at least 1 uppercase letter (A-Z).
    - Contains at least 1 lowercase letter (a-z).
    - Contains at least 1 digit (0-9).
    - Contains at least 1 special character (e.g., !@#$%^&*(),.?":{}|<>).

    Args:
        password (str): The password to validate.

    Raises:
        ValidationError: If the password does not meet the complexity requirements.

    Examples:
        >>> validate_password_strength('Password123!')
        'Password123!'  # Valid password

        >>> validate_password_strength('pass123')
        ValidationError: Password must contain at least 1 uppercase letter.

        >>> validate_password_strength('PASSWORD!')
        ValidationError: Password must contain at least 1 lowercase letter.

        >>> validate_password_strength('Password')
        ValidationError: Password must contain at least 1 digit.

        >>> validate_password_strength('Password1')
        ValidationError: Password must contain at least 1 special character.
    """
    if password is None:
        raise ValidationError("There must be a Password")
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least 1 uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least 1 lowercase letter.")
    if not re.search(r'[0-9]', password):
        raise ValidationError("Password must contain at least 1 digit.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least 1 special character.")
    return password  # Return validated password.

def validate_image_size(image):
        max_size = 2 * 1024 * 1024  # 2 MB
        if image.size > max_size:
            raise ValidationError("Image file too large ( > 2MB )")


