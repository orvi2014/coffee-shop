from __future__ import unicode_literals
from django.conf import settings

from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _


class Order(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    cup_count = models.IntegerField()
    lat = models.CharField(_("lat"), max_length=255)
    long = models.CharField(_("long"), max_length=255)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __unicode__(self):
        return smart_unicode(self.name)
