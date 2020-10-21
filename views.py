from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.http import Http404
from rest_framework.parsers import MultiPartParser, JSONParser
from PIL import Image
import numpy as np

from .models import Person
from .serializers import PersonSerializer, IdSerializer

class PersonView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request):
        persons = Person.objects.values_list('ID', flat=True)
        serializer = IdSerializer(persons, many=True)
        return Response({"persons": serializer.data})

    def post(self, request):
        person = request.data.get('person')
        serializer = PersonSerializer(data=person)

        if serializer.is_valid():
            new_person = serializer.save()
            return Response({"ID": new_person.ID}, status=200)
        else:
            return Response(serializer.errors, status=400)

    def put(self, request):
        image = request.data.get('image')
        ID = request.data.get('ID')
        if not ID or not image:
            return Response({"message": "No image or no ID", status=400})
        else:
            vector = vector_from_image(image)
            person = get_object_or_404(Person, pk=ID)
            person.vector = vector
            person.save()
            return Response({"message": "Succes", status=200})





class PersonDetailView(APIView):

    def get(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)

        return Response({"message": "Name : {0}, Surname: {1} , Vector : {2}".format(person.name, person.surname, person.vector)})

    def delete(self, request, person_id):
        person = get_object_or_404(Person, pk=person_id)
        person.delete()

        return Response({"message": "Person {0} {1} has been deleted".format(person.name, person.surname)})

class CompareView(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        ID_1 = request.data.get('ID_1')
        ID_2 = request.data.get('ID_2')
        if not ID_1 or not ID_2:
            return Response({"message": "Not all ID's in request", status=400})
        else:
            person_1 = get_object_or_404(Person, pk=ID_1)
            person_2 = get_object_or_404(Person, pk=ID_2)
            result = euclidean_distance(person_1.vector, person_2.vector)
            return Response({'Euclidian distance':"{0}".format(result), status=200})
        

def vector_from_image(image):
    image_from_bytes = Image.frombytes('RGB', (300,300), image, 'raw')
    arr = np.array(image_from_bytes)
    vector = arr.shape
    normal_vector = [x/255 for x in vector]
    return normal_vector

def euclidean_distance(vector_1, vector_2):
    return np.sqrt((vector_1[0]-vector_2[0])**2 +(vector_1[1]-vector_2[1])**2+(vector_1[2]-vector_2[2])**2)