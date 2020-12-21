from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics,status
from .models import Room
from .serializers import RoomSerializers, CreateRoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
# Create your views here.

# def Home(request):
#     return HttpResponse("HELLO")

class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers



class GetRoom(APIView):
    serializer_class = RoomSerializers
    lookup_url_kwarg= 'code'
    def get(self, request, formate=None):
        code= request.GET.get(self.lookup_url_kwarg)
        if code!=None:
            room= Room.objects.filter(code=code)
            if(len(room)>0):
                data= RoomSerializers(room[0]).data
                data['is_host'] = self.request.session.session_key==room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_400_NOT_FOUND)
        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_NOT_FOUND)

class JoinRoom(APIView):
    lookup_url_kwarg= 'code'
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.lookup_url_kwarg , None)
        if code!=None:
            room_result= Room.objects.filter(code= code)
            if len(room_result)>0:
                room = room_result[0]
                self.request.session['room_code'] = code
                return Response({"message": "Room Joined"}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid Code"}, status=status.HTTP_400_NOT_FOUND)
        return Response({"Bad Request": "Invalid Post Data"}, status=status.HTTP_400_BAD_REQUEST)



class CreateAPIView(APIView):
    serializer_class = CreateRoomSerializer
    def post(self, request, formate= None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data= request.data)
        
        if serializer.is_valid():
            guest_can_pause =serializer.data.get('guest_can_pause')
            vote_to_skip = serializer.data.get('vote_to_skip')
            host = self.request.session.session_key
            queryset  = Room.objects.filter(host= host)
   
            if queryset.exists():
             
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.vote_to_skip = vote_to_skip
                room.save(update_fields = ['guest_can_pause','vote_to_skip'])
                # return Response(RoomSerializers(room).data, status=status.HTTP_200_OK)
                self.request.session['room_code'] =room.code
            else:
                room = Room(host =host, guest_can_pause= guest_can_pause, vote_to_skip= vote_to_skip)
                room.save()
                self.request.session['room_code'] =room.code

            return Response(RoomSerializers(room).data, status=status.HTTP_200_OK)





class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data= {
            'code': self.request.session.get('room_code')
        }
        return JsonResponse(data, status=status.HTTP_200_OK) 



class LeaveRoom(APIView):
    def post(self, request, format=None):
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')
            host_id = self.request.session.session_key
            room_results= Room.objects.filter(host= host_id)
            if len(room_results)>0:
                room =room_results[0]
                room.delete()
        return Response({'Message' : "Success"}, status= status.HTTP_200_OK)