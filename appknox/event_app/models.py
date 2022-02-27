import uuid

from django.db import models
from user_app.models import User

LOCATION_CHOICES =  (
                        ('','Select the location'),
                        ('Bengaluru','Bengaluru'),
                        ('Mumbai','Mumbai'),
                        ('Pune','Pune'),
                    )

EVENT_CHOICES   =   (
                        ('','Select the tag'),
                        ('Trading','Trading'),
                        ('Conference','Conference'),
                        ('Networking','Networking'),
                    )

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=True) #title of the movie
    description = models.CharField(max_length=755, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE) #if admin CRUD event
    attendees = models.ManyToManyField(User,related_name='attendee',blank=True) #attendees for the event
    event_type = models.CharField(choices = EVENT_CHOICES, max_length = 100, null = True, blank = True)
    def __str__(self):
        return self.title

class Theatre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    location = models.CharField(choices = LOCATION_CHOICES, max_length = 100, null = True, blank = True)
    capacity = models.IntegerField(default=5, blank = True, null = True)
    def __str__(self):
        return "Theatre = "+str(self.name)+" location = "+str(self.location)

class Show(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_details')
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name='theatre_details')
    capacity = models.IntegerField(default=10, blank = True, null = True)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    def __str__(self):
        disply = "Event = "+str(self.event)+" Theatre = "+str(self.theatre.name)+" Capacity = "+str(self.capacity)
        return disply


class Seat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    no = models.IntegerField(default=1, blank = True, null = True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='show_details')
    def __str__(self):
        return "Seat no = "+str(self.no)+", show = "+str(self.show.event.title)

class BookedSeat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='seat_details')
    timestamp = models.DateTimeField(auto_now_add = True)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='booked_user')
    def __str__(self):
        return str(self.seat)

