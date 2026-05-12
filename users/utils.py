from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from random import randint


from .constants import IMAGE_SIZE, MIN_BRIGHTNESS, MAX_BRIGHTNESS, AVATAR_LETTER_COLOR

User = get_user_model()


def handle_clean_phone(phone, instance):
    if (not phone.startswith('8')) and (not phone.startswith('+7')):
        raise ValidationError('Формат номера телефона - 8XXXXXXXXXX  или \
                                +7XXXXXXXXXX')
    if phone.startswith('8'):
        phone = phone.replace('8', '+7', 1)

    if len(phone) != 12:
        raise ValidationError('Формат номера телефона - 8XXXXXXXXXX  или \
                                +7XXXXXXXXXX')

    if (not phone == instance.phone) and (User.objects.filter(phone=phone).exists()):
        raise ValidationError('Пользователь с таким номером \
        телефона уже существует')

    return phone


def handle_clean_github_url(github_url):
    if not github_url:
        return None
    github_url = github_url.lower()
    website_part = github_url.split('://', 1)[-1]
    if not website_part.startswith('github.com'):
        raise ValidationError('Ссылка должна вести на github')

    return github_url


def assign_user_avatar(user_instance):
    # мягкие цвета, на которых виден белый
    image = Image.new(
        "RGB",
        IMAGE_SIZE,
        (
            randint(MIN_BRIGHTNESS, MAX_BRIGHTNESS),
            randint(MIN_BRIGHTNESS, MAX_BRIGHTNESS),
            randint(MIN_BRIGHTNESS, MAX_BRIGHTNESS),
        ),
    )
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=64)
    text = user_instance.name[0]
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    x = (IMAGE_SIZE[0] - text_width) // 2
    y = IMAGE_SIZE[1] // 4
    draw.text((x, y), text, AVATAR_LETTER_COLOR, font=font)
    buffer = BytesIO()
    image.save(buffer, format='PNG')

    image_file = ContentFile(buffer.getvalue())

    user_instance.avatar.save(f'avatar_{user_instance.id}.png', image_file, save=True)
