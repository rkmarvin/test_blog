from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from test_blog.settings import CURRENT_DOMAIN


class SubscriptionManager(models.Manager):

    def followers(self, master):
        return self.get_queryset().filter(masters=master)

    def masters(self, follower):
        subscr = self.get_queryset().filter(follower=follower).first()
        if subscr:
            return subscr.masters.all()
        return []


class Subscription(models.Model):
    follower = models.ForeignKey(User, related_name="follower_user")
    masters = models.ManyToManyField(User, related_name="master_user")

    objects = models.Manager()
    subsrc_objs = SubscriptionManager()

    def is_master(self, master):
        return master in self.masters.all()


class BlogRecord(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        new = not self.id
        super(BlogRecord, self).save(*args, **kwargs)
        if new:
            self.send_email()

    def send_email(self):
        recipients = [s.follower.email for s in Subscription.subsrc_objs.followers(self.user)]
        if recipients:
            send_mail(
                u'%s add new post' % self.user,
                u'New post available at %s' % self.get_url(),
                from_email="test_blog@a.ru",
                recipient_list=recipients
            )

    def get_url(self):
        return "%s%s" % (CURRENT_DOMAIN, reverse("blog_detail", kwargs={'pk': self.id}))



class SoubcrBlorRecorStatus(models.Model):
    user = models.ForeignKey(User)
    record = models.ForeignKey(BlogRecord)