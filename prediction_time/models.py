from django.db import models
from django.db.models import Model
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS



class contact(models.Model):
    contact_name = models.CharField(max_length=100)
    contact_message = models.CharField(max_length=1000)
    contact_email = models.EmailField()
    

    def __unicode__(self):
        return u'%s %s %s' % (self.contact_name,self.contact_email,self.contact_message)
