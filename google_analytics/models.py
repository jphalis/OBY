from django.db import models


class Analytics(models.Model):
    analytics_code = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return u"{}".format(self.analytics_code)

    class Meta:
        verbose_name_plural = "Analytics"
