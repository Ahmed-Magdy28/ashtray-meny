import re
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

def validate_password_strength(password):
    """
    Validate password complexity requirements and enforce Django's default validators.

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
    """
    if password is None:
        raise ValidationError("Password cannot be empty.")

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

    # Optionally enforce Django's default validators (e.g., common password list)
    try:
        validate_password(password)
    except ValidationError as e:
        raise ValidationError(f"Password validation error: {', '.join(e.messages)}")

    return password  # Return the validated password

def validate_image_size(image):
        max_size = 2 * 1024 * 1024  # 2 MB
        if image.size > max_size:
            raise ValidationError("Image file too large ( > 2MB )")


