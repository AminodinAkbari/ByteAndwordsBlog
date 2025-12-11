from django.db.models.signals import post_save
from django.dispatch import receiver
from Posts.models import Post

from Blog.settings import OPENROUTER_API_KEY
from openrouter import OpenRouter


# TODO: Controll post size that not too big for generating summery via AI. 
@receiver(post_save, sender=Post)
def generate_summary(sender, instance, created, **kwargs):
    print("SIGNAL called")
    if created:
        with OpenRouter(api_key=OPENROUTER_API_KEY) as client:
            response = client.chat.send(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates a summary of a post."},
                    {"role": "user", "content": f"Generate a summary of the following post: {instance.content}"}
                ]
            )
            instance.summary = response.choices[0].message.content
            instance.save()
            print("Summary saved successfully")
