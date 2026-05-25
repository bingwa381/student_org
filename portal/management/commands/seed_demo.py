from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portal.models import Department, ClassGroup, Subject, Teacher, Student, Announcement


class Command(BaseCommand):
    help = 'Seed the database with demo data for the student management system.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding demo data...')

        admin_user, _ = User.objects.get_or_create(username='admin', defaults={
            'email': 'admin@example.com',
            'first_name': 'Site',
            'last_name': 'Administrator',
        })
        admin_user.set_password('Admin1234')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

        dept, _ = Department.objects.get_or_create(code='SCI', defaults={'name': 'Science', 'description': 'Science department'})
        class_group, _ = ClassGroup.objects.get_or_create(name='2026 Intake', year='1st Year', department=dept)

        teacher_user, _ = User.objects.get_or_create(username='teacher1', defaults={
            'email': 'teacher1@example.com',
            'first_name': 'Emma',
            'last_name': 'Wong',
        })
        teacher_user.set_password('Teacher1234')
        teacher_user.save()
        teacher, _ = Teacher.objects.get_or_create(user=teacher_user, defaults={
            'department': dept,
            'phone': '+255123456789',
            'bio': 'Senior science lecturer',
        })

        subject, _ = Subject.objects.get_or_create(code='SCI101', defaults={
            'title': 'Foundations of Science',
            'department': dept,
            'teacher': teacher,
        })

        student_user, _ = User.objects.get_or_create(username='student1', defaults={
            'email': 'student1@example.com',
            'first_name': 'James',
            'last_name': 'Munya',
        })
        student_user.set_password('Student1234')
        student_user.save()
        Student.objects.get_or_create(user=student_user, defaults={
            'department': dept,
            'class_group': class_group,
            'gender': 'Male',
            'date_of_birth': '2004-06-17',
            'phone': '+255987654321',
            'course': 'Diploma in Applied Science',
            'year_of_study': '1st Year',
            'payment_amount': 10000,
            'payment_confirmed': True,
            'is_approved': True,
            'status': Student.Status.APPROVED,
        })

        Announcement.objects.get_or_create(title='Welcome to the student portal', defaults={
            'message': 'The new Student Management System is live. Please login to view your dashboard.',
            'created_by': admin_user,
            'is_public': True,
        })

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
