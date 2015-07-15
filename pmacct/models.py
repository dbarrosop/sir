from django.db import models
import datetime


class FlowManager(models.Manager):

    def aggregate_bytes_per_as(self, hours=0):
        return self.model.objects.get_latest_flows(hours).values('as_dst').annotate(
            sum_bytes=models.Sum('bytes_exp')).order_by('-sum_bytes')

    def aggregate_bytes_per_prefix(self, hours=0):
        return self.model.objects.get_latest_flows(hours).values('ip_dst', 'mask_dst', 'as_dst').annotate(
            sum_bytes=models.Sum('bytes_exp')).order_by('-sum_bytes')

    def aggregate_bytes_per_prefix_in_as(self, asn, hours=0):
        return self.model.objects.get_latest_flows(hours).filter(as_dst=asn).values('stamp_inserted').annotate(
            sum_bytes=models.Sum('bytes_exp')).order_by('stamp_inserted')

    def get_dates(self):
        dates = [d['stamp_inserted']
                 for d in self.model.objects.all().values('stamp_inserted').order_by('stamp_inserted').distinct()]
        return dates

    def get_latest_date(self):
        return self.get_dates()[-1]

    def get_latest_flows(self, hours=0):
        date = self.get_latest_date() - datetime.timedelta(hours=hours)
        return self.model.objects.filter(stamp_inserted__gte=date)

    def get_latest_flows_per_prefix(self, ip_dst, mask_dst, hours=0):
        date = self.get_latest_date() - datetime.timedelta(hours=hours)
        return self.model.objects.filter(stamp_inserted__gte=date).filter(ip_dst=ip_dst).filter(mask_dst=mask_dst)


class Flow(models.Model):
    stamp_inserted = models.DateTimeField()
    as_dst = models.PositiveIntegerField()
    ip_dst = models.GenericIPAddressField()
    mask_dst = models.PositiveSmallIntegerField()
    packets_exp = models.PositiveIntegerField(db_column='packets')
    bytes_exp = models.PositiveIntegerField(db_column='bytes')
    objects = FlowManager()

    class Meta:
        db_table = 'acct'
        managed = False
        get_latest_by = 'stamp_inserted'
        ordering = ['-stamp_inserted', '-bytes_exp']

    def __unicode__(self):
        return u'{}, {}, {}, {}, {}, {}'.format(
            self.stamp_inserted, self.as_dst, self.ip_dst, self.mask_dst, self.packets_exp, self.bytes_exp)
