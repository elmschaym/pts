from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now_add=True)

  class Meta:
    abstract = True


class Category(TimeStampedModel):
  name = models.CharField(max_length=128, unique=True)
  description = models.TextField(default='')

  def __unicode__(self):
    return self.name

class Employee(models.Model):
    user = models.OneToOneField(User)
    position = models.CharField(max_length=45)
    department = models.CharField(max_length=45)
    address = models.CharField(max_length=100, blank=True)
    image_path = models.FileField(upload_to='profile_pics/', default ='profile_pics/default_male.png')

    def __unicode__(self):
      return self.user.username

class Ticket(TimeStampedModel):
  choice=((1,'Open'),
           (0,'Closed'))
  flags=((1,'unRead'),
         (0,'Read'))

  subject = models.CharField(max_length=200)
  description = models.TextField(default='')
  user_requestor = models.ForeignKey(User, related_name = 'ticket_requestor')
  status = models.BooleanField(choices=choice)
  priority = models.IntegerField()
  category = models.ForeignKey(Category)
  created_by = models.ForeignKey(User, related_name = 'ticket_created')
  assign_user = models.ForeignKey(User, related_name = 'ticket_assign')
  flag = models.BooleanField(choices=flags)
  def __unicode__(self):
    return self.id

  def get_absolute_url(self):
    return reverse('tickets-detail', kwargs={'pk': self.id})

class TicketAge(TimeStampedModel):
  choices=((1,'done'),
         (0,'undone'))
  assign_user = models.ForeignKey(User)
  ticket = models.ForeignKey(Ticket)
  done = models.BooleanField(choices=choices)

class Document(TimeStampedModel):
    ticket = models.ForeignKey(Ticket)
    name = models.CharField(max_length=200)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    user    = models.ForeignKey(User)

class Comment(TimeStampedModel):
  ticket  = models.ForeignKey(Ticket)
  comment = models.TextField()
  user    = models.ForeignKey(User)
  

  def __unicode__(self):
    return self.comment


# class Attachment(TimeStampedModel):
#   ticket = models.ForeignKey(Ticket)
#   path = models.CharField(max_length=255)

#   def __unicode__(self):
#     return self.path
