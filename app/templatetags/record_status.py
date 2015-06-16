from django import template
from app.models import SoubcrBlorRecorStatus

register = template.Library()

__author__ = 'marvin'


def record_status(context, record):
    request = context['request']
    return {
        "is_readed": SoubcrBlorRecorStatus.objects.filter(user=request.user, record=record),
        "record": record,
        "request": request,
    }

register.inclusion_tag('app/record_status.html', takes_context=True)(record_status)
