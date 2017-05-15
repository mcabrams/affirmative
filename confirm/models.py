from django.db import models


class Confirmation(models.Model):
    confirmed = models.BooleanField(default=False)
    info = models.CharField(max_length=512)

    def confirm(self):
        self.confirmed = True
        self.save()
