from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from app.views import ListUserBlogRecordsView, CreateBlogRecordView, BlogersListView, SubscribeView, UnSubscribeView, \
    NewsListView, SetReadedView, UserBlogRecordDetailView

__author__ = 'marvin'


urlpatterns = [
    url(r'^blog/$', login_required(ListUserBlogRecordsView.as_view()), name="blog"),
    url(r'^blog/(?P<pk>\d+)/$', login_required(UserBlogRecordDetailView.as_view()), name="blog_detail"),
    url(r'^blog/add/$', login_required(CreateBlogRecordView.as_view()), name="blog_add"),
    url(r'^blog/blogers/$', login_required(BlogersListView.as_view()), name="blog_blogers"),
    url(r'^blog/blogers/subsc/(?P<user_id>\d+)/$', login_required(SubscribeView.as_view()), name="blog_subsc"),
    url(r'^blog/blogers/unsubsc/(?P<user_id>\d+)/$', login_required(UnSubscribeView.as_view()), name="blog_unsubsc"),
    url(r'^blog/news/$', login_required(NewsListView.as_view()), name="blog_news"),
    url(r'^blog/set/readed/(?P<record_id>\d+)/$', login_required(SetReadedView.as_view()), name="blog_set_readed"),
]
