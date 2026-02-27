import logging
from celery import shared_task

from Blog.settings import OPENROUTER_API_KEY
from openrouter import OpenRouter
from Posts.models import Post

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=30,
    retry_kwargs={'max_retries': 3}
)
def generate_post_summary_task(post_slug: str) -> None:
    post = Post.objects.get(slug=post_slug)

    logger.debug(f"Requesting to AI {post_slug}") 

    with OpenRouter(api_key=OPENROUTER_API_KEY) as client:
        response = client.chat.send(
        model="gpt-4o-mini",
        messages=[
             {
                "role": "system", "content": "You are a helpful assistant \
                that generates a summary of an article."
             },
             {
                "role": "user", "content": f"Generate a summary  \
                of the following article: {post.content}"
             }
        ]
    )

    logger.debug("Done. AI response is in application")

    summary = response.choices[0].message.content

    post.summary = summary
    post.save(update_fields=['summary'])

    logger.debug(f"SUMMARY SAVED IN DATABASE FOR post id :{post.id}")
