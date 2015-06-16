from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView, CreateView, RedirectView, DetailView
from app.models import BlogRecord, Subscription, SoubcrBlorRecorStatus


class ListUserBlogRecordsView(ListView):

    def get_queryset(self):
        return BlogRecord.objects.filter(user=self.request.user)


class UserBlogRecordDetailView(DetailView):

    model = BlogRecord


class CreateBlogRecordView(CreateView):

    model = BlogRecord
    fields = ['title', 'text']
    success_url = "/app/blog/"

    def form_valid(self, form):
        blog_record = form.save(commit=False)
        blog_record.user = self.request.user
        blog_record.save()
        return super(CreateBlogRecordView, self).form_valid(form)


class BlogersListView(ListView):

    template_name = "app/blogers_list.html"

    def get_queryset(self):
        return User.objects.filter(~Q(id=self.request.user.id))


class SubscribeView(RedirectView):
    permanent = False
    url = '/app/blog/blogers/'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id:
            subscr = Subscription.objects.get_or_create(follower=request.user)[0]
            subscr.masters.add(User.objects.get(id=user_id))
            subscr.save()
        return super(SubscribeView, self).get(request, *args, **kwargs)


class UnSubscribeView(RedirectView):
    permanent = False
    url = '/app/blog/blogers/'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id:
            subscr = Subscription.objects.get(follower=request.user)
            subscr.masters.remove(User.objects.get(id=user_id))
            subscr.save()

            SoubcrBlorRecorStatus.objects.filter(user=request.user).delete()

        return super(UnSubscribeView, self).get(request, *args, **kwargs)


class NewsListView(ListView):

    template_name = "app/news_list.html"

    def get_queryset(self):
        masters = Subscription.get_masters(self.request.user)
        return BlogRecord.objects.filter(user__in=masters).order_by('-created')


class SetReadedView(RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        record_id = kwargs.get('record_id')
        if record_id:
            SoubcrBlorRecorStatus.objects.get_or_create(user=request.user, record_id=record_id)
        return super(SetReadedView, self).get(request, *args, **kwargs)
    
    def get_redirect_url(self, *args, **kwargs):
        self.url = self.request.META.get("HTTP_REFERER")
        if self.url:
            return super(SetReadedView, self).get_redirect_url(*args, **kwargs)
        return None

