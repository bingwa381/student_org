from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from .models import (
    Profile,
    Department,
    ClassGroup,
    Subject,
    Teacher,
    Student,
    StudentDocument,
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'department', 'phone', 'address', 'city', 'state', 'country', 'zip_code', 'bio', 'is_verified', 'created_at']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description']


class ClassGroupSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), source='department', write_only=True, required=False, allow_null=True)

    class Meta:
        model = ClassGroup
        fields = ['id', 'name', 'year', 'department', 'department_id']


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), source='department', write_only=True, required=False, allow_null=True)

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'department', 'department_id', 'phone', 'bio', 'is_active', 'joined_at']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        if hasattr(user, 'profile'):
            user.profile.role = Profile.Roles.TEACHER
            user.profile.save()
        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        return super().update(instance, validated_data)


class SubjectSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), source='teacher', write_only=True, required=False, allow_null=True)
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), source='department', write_only=True, required=False, allow_null=True)

    class Meta:
        model = Subject
        fields = ['id', 'title', 'code', 'department', 'department_id', 'teacher', 'teacher_id']


class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        fields = ['id', 'student', 'document', 'document_type', 'uploaded_at']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    class_group = ClassGroupSerializer(read_only=True)
    documents = StudentDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'student_id', 'registration_number', 'department', 'class_group', 'guardian_name', 'guardian_phone', 'guardian_email',
            'address', 'city', 'state', 'country', 'zip_code', 'gender', 'date_of_birth', 'phone', 'course', 'year_of_study', 'profile_picture',
            'payment_amount', 'payment_reference', 'payment_confirmed', 'is_approved', 'status', 'registered_at', 'documents',
        ]


class StudentRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    registration_number = serializers.CharField(read_only=True)
    student_id = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name', 'gender', 'date_of_birth', 'phone', 'course',
            'year_of_study', 'profile_picture', 'payment_amount', 'payment_reference', 'payment_confirmed', 'guardian_name',
            'guardian_phone', 'guardian_email', 'address', 'city', 'state', 'country', 'zip_code', 'student_id', 'registration_number',
        ]

    def validate(self, attrs):
        if User.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError({'username': 'A user with this username already exists.'})
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({'email': 'A user with this email already exists.'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.pop('username'),
            email=validated_data.pop('email'),
            password=validated_data.pop('password'),
            first_name=validated_data.pop('first_name'),
            last_name=validated_data.pop('last_name'),
        )
        student = Student.objects.create(user=user, **validated_data)
        return student


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = ['id', 'student', 'subject', 'enrolled_at', 'status']


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    recorded_by = TeacherSerializer(read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'subject', 'date', 'status', 'recorded_by']


class FeeStructureSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = FeeStructure
        fields = ['id', 'department', 'semester', 'amount', 'description']


class PaymentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'student', 'amount', 'reference', 'status', 'receipt_id', 'paid_at', 'created_at']


class ExamSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'department', 'subject', 'schedule_date', 'total_marks', 'passing_marks']


class ResultSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    exam = ExamSerializer(read_only=True)

    class Meta:
        model = Result
        fields = ['id', 'student', 'exam', 'marks_obtained', 'grade', 'gpa', 'published', 'updated_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'message', 'created_by', 'created_at', 'is_public']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    receiver_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='receiver', write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'receiver_id', 'subject', 'body', 'sent_at', 'is_read']


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'timestamp', 'ip_address', 'metadata']
