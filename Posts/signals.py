import logging
from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from Posts.models import Post

from Posts.tasks import generate_post_summary_task

logger = logging.getLogger(__name__)

# TODO: Controll post size that not too big for generating summery via AI. 
# TODO: If this secion enable , got this :
    # TypeError: generate_post_summary_task() takes 1 positional argument but 2 were given
@receiver(post_save, sender=Post)
def generate_summary(sender, instance, created, **kwargs):
    pass
#    if created:
#        print("THIS IS INSTANCE :" , instance.slug)
#        transaction.on_commit(
#            lambda: generate_post_summary_task.delay(instance.slug)
#        )
