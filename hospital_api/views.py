from django.contrib.auth import authenticate
from .serializer import TreatmentAppliedSerializer, PrescriptionSerializer, DoctorSerializer , PatientSerializer, AssistantSerializer, TreatmentSerializer,AssignmentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate,login
from .models import Doctor, Patient, Assistant, Prescription, Treatment, Assignment,TreatmentApplied
from rest_framework import generics
from rest_framework import status
from .permissions import IsGeneralManager, IsDoctor, IsAssistant
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework.views import APIView

# Login endpoint
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        return Response({'detail': 'Authentication successful'})
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Doctor Management endpoints (done by the General manager)
# Create doctor 
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsGeneralManager])
def create_doctor(request):
    # create a new user with the role of a doctor
    user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password']
    )
    doctor_data = {
        'user': user.id,
        'specialty': request.data['specialty'],
        'name': request.data['name'],
        'patients':request.data['patients'],
        'id':user.id,
    }
    my_group = Group.objects.get(name='Doctor') 
    my_group.user_set.add(user)
    serializer = DoctorSerializer(data=doctor_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorList(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsGeneralManager]


class DoctorUpdate(generics.UpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated,IsGeneralManager]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated,IsGeneralManager]

class DoctorDelete(generics.DestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsGeneralManager]

# Patient management endpoints (done by Doctor or General manager)

class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated,IsGeneralManager]

class PacientCreate(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated,IsDoctor|IsGeneralManager]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientsAssignedToDoctor(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    def list(self, request, *args, **kwargs):
        try:
            # Get the authenticated doctor user
            user = self.request.user.id
            doctor_user = Doctor.objects.get(id=user)
            
            # Get the patients assigned to the doctor
            patients = doctor_user.patients.all()
            
            # Serialize and return the patient data
            serializer = self.get_serializer(patients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            # Handle case where doctor user is not found
            return Response({"error": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)
        except:
            # Handle all other exceptions
            return Response({"error": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PatientLists(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated,IsGeneralManager]
   
class PatientDelete(generics.DestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated,IsGeneralManager]

# Assistant management endpoints (done by the General manager)

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsGeneralManager])
def create_assistant(request):
    # create a new user with the role of a assitant
    user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password']
    )
    assistant_data = {
        'id':user.id,
        'name': request.data['name'],
        'user': user.id
    }
    my_group = Group.objects.get(name='Assistant') 
    my_group.user_set.add(user)
    serializer = AssistantSerializer(data=assistant_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssistantList(generics.ListCreateAPIView):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [IsAuthenticated,IsGeneralManager]

class AssistantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [IsAuthenticated,IsGeneralManager]

class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated,IsGeneralManager]

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated,IsGeneralManager]

#Treatment management (done by Doctor or General manager)

class TreatmentList(generics.ListCreateAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = [IsAuthenticated,IsDoctor|IsGeneralManager]

class Treatment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = [IsAuthenticated,IsDoctor|IsGeneralManager]

#The treatment recommended by a doctor to a Patient (done by the Doctor) 
class PrescriptionListCreateView(generics.ListCreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated,IsDoctor]

class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated,IsDoctor]

#Treatment applied by an Assistant (Assistant only)

class TreatmentAppliedView(generics.CreateAPIView):
    serializer_class = TreatmentAppliedSerializer
    permission_classes = [IsAuthenticated,IsAssistant]
    def create(self, request,  *args, **kwargs):
        drug = request.data.get('drug')
        dosage = request.data.get('dosage')
        treatment=request.data.get('treatment')
        patient_id = request.data.get('patient')
        user = self.request.user.id
        assistant_user = Assistant.objects.get(id=user)
        patient = generics.get_object_or_404(Patient, pk=patient_id)
        assignments = Assignment.objects.filter(assistant=assistant_user)
        patients_assign = Patient.objects.filter(assignment__in=assignments)
        if patient not in patients_assign:
            return Response({'error': 'The assistant has no access to this patient'}, status=status.HTTP_400_BAD_REQUEST)
        if not drug or not dosage:
            return Response({'error': 'drug, dosage and treatment are required'}, status=status.HTTP_400_BAD_REQUEST)
        data = {'assistant': assistant_user.pk, 'drug': drug, 'dosage': dosage,'treatment':treatment,'patient':patient_id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class DoctorReportAPIView(APIView):
    permission_classes = [IsAuthenticated,IsGeneralManager]
    def get(self, request):
        
        if not request.user.groups.filter(name='General Manager').exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        doctors = Doctor.objects.prefetch_related('patients').all()
        serialized_data = DoctorSerializer(doctors, many=True).data
        patient_count = Patient.objects.count()
        prescription_count = Prescription.objects.count()
        assignment_count = Assignment.objects.count()
        statistics_data = {
            'patient_count': patient_count,
            'prescription_count': prescription_count,
            'assignment_count': assignment_count,
        }
        
        report_data = {
            'doctors': serialized_data,
            'statistics': statistics_data,
        }
        
        return Response(report_data)

class TreatmentAppliedReport(generics.RetrieveAPIView):
    
    queryset = TreatmentApplied.objects.all()
    serializer_class = TreatmentAppliedSerializer
    permission_classes = [IsAuthenticated,IsDoctor|IsGeneralManager]
    def retrieve(self, request,patient_pk=None, *args, **kwargs):
        patient = generics.get_object_or_404(Patient, pk=patient_pk)
        patient_id = patient.id
        treatments = TreatmentApplied.objects.filter(patient_id=patient_id)
        serializer = self.get_serializer(treatments, many=True)
        return Response(serializer.data)

