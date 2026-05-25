from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q

from .models import (
    Profile,
    Department,
    ClassGroup,
    Subject,
    Teacher,
    Student,
    CourseEnrollment,
    AttendanceRecord,
    FeeStructure,
    Payment,
    Exam,
    Result,
    Announcement,
    Message,
    AuditLog,
)
from .serializers import (
    ProfileSerializer,
    DepartmentSerializer,
    ClassGroupSerializer,
    SubjectSerializer,
    TeacherSerializer,
    StudentSerializer,
    StudentRegistrationSerializer,
    CourseEnrollmentSerializer,
    AttendanceRecordSerializer,
    FeeStructureSerializer,
    PaymentSerializer,
    ExamSerializer,
    ResultSerializer,
    AnnouncementSerializer,
    MessageSerializer,
    AuditLogSerializer,
)


class IsAdminOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        role = getattr(getattr(request.user, 'profile', None), 'role', None)
        return role == Profile.Roles.TEACHER


class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']


class ClassGroupViewSet(viewsets.ModelViewSet):
    queryset = ClassGroup.objects.all()
    serializer_class = ClassGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'year']


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related('user', 'department').all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrTeacher]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'user__email']


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.select_related('department', 'teacher').all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'code']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user', 'department', 'class_group').all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'student_id', 'registration_number', 'course']
    filterset_fields = ['department', 'class_group', 'year_of_study', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(getattr(user, 'profile', None), 'role', None) == Profile.Roles.TEACHER:
            return self.queryset
        return self.queryset.filter(user=user)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdminOrTeacher])
    def approve(self, request, pk=None):
        student = self.get_object()
        if student.status == Student.Status.APPROVED:
            return Response({'detail': 'Student is already approved.'}, status=status.HTTP_400_BAD_REQUEST)
        student.status = Student.Status.APPROVED
        student.is_approved = True
        student.save()
        return Response(self.get_serializer(student).data)


class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = CourseEnrollment.objects.select_related('student', 'subject').all()
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrTeacher]
    filter_backends = [filters.SearchFilter]
    search_fields = ['student__student_id', 'subject__title']


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.select_related('student', 'subject', 'recorded_by').all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrTeacher]
    filter_backends = [filters.SearchFilter]
    search_fields = ['student__student_id', 'subject__title']


class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.select_related('department').all()
    serializer_class = FeeStructureSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('student').all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrTeacher]


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related('department', 'subject').all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.select_related('student', 'exam').all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrTeacher]


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.select_related('created_by').all().order_by('-created_at')
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            return queryset.filter(is_public=True)
        return queryset


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('sender', 'receiver').all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(sender=user) | Q(receiver=user))

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrTeacher]


class DashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total_students = Student.objects.count()
        approved_students = Student.objects.filter(status=Student.Status.APPROVED).count()
        pending_students = Student.objects.filter(status=Student.Status.PENDING).count()
        total_teachers = Teacher.objects.count()
        messages = Message.objects.filter(receiver=request.user, is_read=False).count()

        return Response({
            'total_students': total_students,
            'approved_students': approved_students,
            'pending_students': pending_students,
            'total_teachers': total_teachers,
            'unread_messages': messages,
        })
