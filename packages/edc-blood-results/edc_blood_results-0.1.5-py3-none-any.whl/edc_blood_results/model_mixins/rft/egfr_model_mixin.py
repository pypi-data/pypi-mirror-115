from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable.choices import REPORTABLE
from edc_reportable.units import EGFR_UNITS


class EgfrModelMixin(models.Model):
    # eGFR
    egfr_value = models.DecimalField(
        verbose_name="eGFR",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="(system calculated)",
    )

    egfr_units = models.CharField(
        verbose_name="units",
        max_length=15,
        default=EGFR_UNITS,
        null=True,
        blank=True,
    )
    egfr_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    egfr_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
