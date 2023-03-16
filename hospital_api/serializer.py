from rest_framework import serializers
from .models import Doctor, Assistant, Patient, Treatment,Assignment,Prescription,TreatmentApplied
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Group
from rest_framework import serializers



class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields ='__all__'

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
class PatientSerializer(serializers.ModelSerializer):
    Treatment = TreatmentSerializer(read_only=True)
    class Meta:
        model = Patient
        fields = '__all__'
       
class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class TreatmentAppliedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TreatmentApplied
        
        fields = ['assistant', 'treatment', 'drug', 'dosage','patient']
    
    def validate_dosage(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError('Dosage has to be between 0 and 10.')
        return value
