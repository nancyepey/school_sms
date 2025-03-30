import os
from django.conf import settings
from django import template

register = template.Library()

@register.filter   # ← register the template tag
def geturl(image_id):
    variant="public"
    url = settings.CLOUDFLARE_IMAGES_DOMAIN
    account_hash = settings.CLOUDFLARE_ACCOUNT_HASH
    return f"https://{url}/{account_hash}/{image_id}/{variant}"



# def get_image_url_from_cloudflare(image_id, variant="public"):
#     url = settings.CLOUDFLARE_IMAGES_DOMAIN
#     account_hash = settings.CLOUDFLARE_ACCOUNT_HASH
#     return f"https://{url}/{account_hash}/{image_id}/{variant}"

