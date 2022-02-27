
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
#api-view imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user_app.models import User

from .models import BookedSeat, Event, Seat, Show, Theatre
from .permissions import IsOwnerOrReadOnly
from .serializers import (BookedSeatSerializer, EventSerializer,
                          EventTestSerializer, SeatSerializer, ShowSerializer,
                          TheatreSerializer)

#https://learndjango.com/events/django-docker-and-postgresql-tutorial

#Refer below link for rest api
#https://www.bezkoder.com/django-rest-api/
#admin API's
class ListCreateEventAPIView(ListCreateAPIView):
    ''' Create & View Events'''
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        # Assign the user who created the Event
        serializer.save(created_by=self.request.user)

class RetrieveUpdateDestroyEventAPIView(RetrieveUpdateDestroyAPIView):
    ''' Retrieve Update &  Destroy Event '''
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
##########
class ListCreateTheatreAPIView(ListCreateAPIView):
    ''' Create & View Theatre'''
    serializer_class = TheatreSerializer
    queryset = Theatre.objects.all()
    permission_classes = [IsAdminUser]

class RetrieveUpdateDestroyTheatreAPIView(RetrieveUpdateDestroyAPIView):
    ''' Retrieve Update &  Destroy Theatre '''
    serializer_class = TheatreSerializer
    queryset = Theatre.objects.all()
    permission_classes = [IsAdminUser]
##########
class ListCreateShowAPIView(ListCreateAPIView):
    ''' Create & View Theatre'''
    serializer_class = ShowSerializer
    queryset = Show.objects.all()
    permission_classes = [IsAdminUser]

class RetrieveUpdateDestroyShowAPIView(RetrieveUpdateDestroyAPIView):
    ''' Retrieve Update &  Destroy Theatre '''
    serializer_class = ShowSerializer
    queryset = Show.objects.all()
    permission_classes = [IsAdminUser]
##########
class ListCreateSeatAPIView(ListCreateAPIView):
    ''' Create & View Theatre'''
    serializer_class = SeatSerializer
    queryset = Seat.objects.all()
    permission_classes = [IsAdminUser]

class RetrieveUpdateDestroySeatAPIView(RetrieveUpdateDestroyAPIView):
    ''' Retrieve Update &  Destroy Theatre '''
    serializer_class = SeatSerializer
    queryset = Seat.objects.all()
    permission_classes = [IsAdminUser]
##########
class ListCreateBookedSeatAPIView(ListCreateAPIView):
    ''' Create & View Theatre'''
    serializer_class = BookedSeatSerializer
    queryset = BookedSeat.objects.all()
    permission_classes = [IsAdminUser]

class RetrieveUpdateDestroyBookedSeatAPIView(RetrieveUpdateDestroyAPIView):
    ''' Retrieve Update &  Destroy Theatre '''
    serializer_class = BookedSeatSerializer
    queryset = BookedSeat.objects.all()
    permission_classes = [IsAdminUser]
##########
class EventsList(APIView):
    def get(self, request):
        queryset = Event.objects.all()
        serializer = EventTestSerializer(queryset,many=True)
        return Response(serializer.data)

    def post():
        pass


class UserViewAllEvents(APIView):
    ''' User view all events'''
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def get(self, request):
        queryset = Event.objects.all()
        serializer = EventTestSerializer(queryset,many=True)
        return Response(serializer.data)

class UserBookEventTicket(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        booked_seat   =   None
        seat    =   None
        status = None
        message = None
        try:
            params  =   json.loads(request.body)
            seat_id =   params["seat_id"]
            user_id =   params["user_id"]
            print("PARAMS : "+str(params))
        except Exception as e:
            print("BAD BODY : "+str(e))
            return JsonResponse("bad params", status = 400, safe = False)

        try:
            seat = get_object_or_404(Seat, id = seat_id)
            print("seat",seat.id)
        except Exception as e:
            print("Error",e)
        try:
            user   =   User.objects.get(id = user_id)
        except Exception as e:
            print(e)
        try:
            is_booked = BookedSeat.objects.filter(seat = seat)
            if not is_booked.exists():
                booked_seat = BookedSeat(seat = seat,booked_by = user)
                booked_seat.save()
                booked_seat_serializer = BookedSeatSerializer(booked_seat, many = False)
                try:
                    #check delta time
                    booked_seat_detail = BookedSeat.objects.get(seat = seat)
                    show = Show.objects.get(id = seat.show.id)
                    print(show.id)
                    result=  show.start_date_time - booked_seat_detail.timestamp
                    total_seconds = result.total_seconds()
                    print("total_seconds", total_seconds)
                    if abs(total_seconds) <= 3600:
                        print("Yay! booked seat in time slot")
                        message = booked_seat_serializer.data
                        status = 201
                    else:
                        print("delete booked seat update response")
                        booked_seat_detail.delete()
                        message = "Sorry, ticket wasn't booked in the timeframe!"
                        status = 403
                except Exception as e:
                    print("Time block",e)
                try:
                    #add attendees
                    event = Event.objects.get(id = seat.show.event.id)
                    print("event",event)
                    event.attendees.add(user)
                    event.save()
                except Exception as e:
                    print(e)
            else:
                print("is_booked else ",is_booked.exists())
                status = 409 #conflict
                message = "seat is already booked"
        except Exception as e:
            status = 400
            message = str(e)
        data_   =   {
                        "status"    :   status,
                        "message"      :  message
                    }
        print("data_",data_)
        return JsonResponse(data = data_, status = status, safe = False)


class UserViewTicket(RetrieveUpdateAPIView):
    ''' User view registered events'''
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print('view ticket',request.user)
        try:
            params  =   json.loads(request.body)
            ticket_id =   params["ticket_id"]
            print("PARAMS : "+str(params))
        except Exception as e:
            print("BAD BODY : "+str(e))
            return JsonResponse("bad params", status = 400, safe = False)
        try:
            booked_seat = BookedSeat.objects.get(id = ticket_id)
            details =   {
                            "ticket_id" : str(booked_seat.id),
                            "show_name": str(booked_seat.seat.show.event.title),
                            "seat_no"   : str(booked_seat.seat.no),
                            "show_starts_at": (booked_seat.seat.show.start_date_time).strftime("%d/%m/%Y %H:%M:%S"),
                            "booked_on" : (booked_seat.timestamp).strftime("%d/%m/%Y %H:%M:%S")
                        }
            message = details
            status = 200
        except Exception as e:
            message = "Error "+str(e)
            status = 400
        return JsonResponse(data = message, status = status, safe = False)

class UserViewAllRegisteredEvents(RetrieveUpdateAPIView):
    ''' User view registered events'''
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print('view ticket',request.user)
        try:
            params  =   json.loads(request.body)
            booked_by =   params["booked_by"]
            print("PARAMS : "+str(params))
        except Exception as e:
            print("BAD BODY : "+str(e))
            return JsonResponse("bad params", status = 400, safe = False)
        try:
            event = Event.objects.filter(attendees = booked_by)
            event_serializer = EventSerializer(event, many = True)
            message = event_serializer.data
            status = 200
        except Exception as e:
            message = "Error "+str(e)
            status = 400
        return JsonResponse(data = message, status = status, safe = False)

