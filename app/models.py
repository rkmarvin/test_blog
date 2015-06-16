from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from test_blog.settings import CURRENT_DOMAIN


class Subscription(models.Model):
    follower = models.ForeignKey(User, related_name="follower_user")
    masters = models.ManyToManyField(User, related_name="master_user")

    @classmethod
    def get_masters(cls, follower):
        subscr = cls.objects.filter(follower=follower).first()
        if subscr:
            return subscr.masters.all()
        return []

    def is_master(self, master):
        return master in self.masters.all()

    @classmethod
    def get_followers(cls, master):
        return Subscription.objects.filter(masters=master)


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
        recipients = [s.follower.email for s in Subscription.get_followers(self.user)]
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