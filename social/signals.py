from django.db.models.signals import m2m_changed , post_delete
from django.dispatch import receiver
from .models import Post
from django.core.mail import send_mail

@receiver(m2m_changed, sender=Post.likes.through)
def user_liked_change(sender, instance, action, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()


@receiver(post_delete, sender=Post)
def user_liked_change(sender, instance, **kwargs):
    author = instance.author
    subject = f"your post has been deleted"
    message = f"your post has been deleted (Id:{instance.id}) "
    send_mail(
                subject,
                message,
                'arian.zafarei2016@gmail.com',
                [author.email],
                fail_silently=False,
            )
