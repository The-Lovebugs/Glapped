from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ListingReport, Product

# Update reportAmount after creating a ListingReport
@receiver(post_save, sender=ListingReport)
def update_report_count_on_save(sender, instance, **kwargs):
    product = instance.product
    product.reportAmount = product.reports.count()
    product.save()

# Update reportAmount after deleting a ListingReport
@receiver(post_delete, sender=ListingReport)
def update_report_count_on_delete(sender, instance, **kwargs):
    product = instance.product
    product.reportAmount = product.reports.count()
    product.save()