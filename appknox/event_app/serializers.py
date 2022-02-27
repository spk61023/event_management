from django.contrib.auth.models import User
from rest_framework import serializers

from .models import BookedSeat, Event, Seat, Show, Theatre


class EventSerializer(serializers.ModelSerializer):  # create class to serializer model
    created_by = serializers.ReadOnlyField(source='User.username')
    class Meta:
        model = Event
        fields = '__all__'

class TheatreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields = '__all__'

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class BookedSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedSeat
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    Events = serializers.PrimaryKeyRelatedField(many=True, queryset=Event.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'Events')

class EventTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class UserRegisteredEvents(serializers.ModelSerializer):
    ''' user registered events'''
    class Meta:
        model = Event
        fields = ()

class UserBookTicket(serializers.ModelSerializer):
    ''' user views ticket '''
    class Meta:
        model = BookedSeat
        fields = ()

class UserBookedSeat(serializers.ModelSerializer):
    ''' call this after booking seat '''
    class Meta:
        model = BookedSeat
        fields = ()
