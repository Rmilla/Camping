from django.test import TestCase
from rest_framework.test import APIClient
from .serializer.camping_serializer import CampingSerializer
from .models.camping import Camping

# Create your tests here.

class CampingSerializerTestCase(TestCase):
    def setUp(self):
        self.camping = Camping.objects.create(name="Test Camping", location="Test Location")
    #teste la serialization
    def test_serialization(self):
        serializer = CampingSerializer(self.camping)
        expected_data = {
            'name': 'Test Camping',
            'location': 'Test Location'
            }
        self.assertEqual(serializer.data, expected_data)
    #teste la deserialization
    def test_deserialization(self):
        data = {
            'name': 'Test Camping',
            'location': 'Test Location'
        }
        serializer = CampingSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        camping = serializer.save()
        self.assertEqual(camping.name, 'Test Camping')

