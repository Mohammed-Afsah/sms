from django.utils.text import slugify

import uuid
def generate_slug(title:str)->str:

    """
    A function to get generated slug for recipe model return str
    """

    from .models import Recipe
    title=slugify(title)

    while(Recipe.objects.filter(slug=title).exists()):
       title=f'{slugify(title)}-{str(uuid.uuid4())[:4]}'
    return title