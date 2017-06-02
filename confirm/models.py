from django.db import models


class Confirmation(models.Model):
    confirmed = models.BooleanField(default=False)
    src_path = models.FilePathField(path='/Volumes', allow_files=True,
                                    allow_folders=True, recursive=True,
                                    null=False, blank=False)
    dst_path = models.FilePathField(path='/Volumes', allow_files=False,
                                    allow_folders=True, recursive=True,
                                    null=False, blank=False)

    def confirm(self):
        self.confirmed = True
        self.save()
