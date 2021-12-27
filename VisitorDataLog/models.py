from django.db import models


class VisitorUser(models.Model):
    usernm = models.CharField(max_length=50)
    signupdt = models.DateTimeField()
    u_segmt = models.CharField(max_length=5)
