from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, Student, Teacher


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Student)
def assign_student_role(sender, instance, **kwargs):
    profile = getattr(instance.user, 'profile', None)
    if profile and profile.role != Profile.Roles.STUDENT:
        profile.role = Profile.Roles.STUDENT
        profile.save()


@receiver(post_save, sender=Teacher)
def assign_teacher_role(sender, instance, **kwargs):
    profile = getattr(instance.user, 'profile', None)
    if profile and profile.role != Profile.Roles.TEACHER:
        profile.role = Profile.Roles.TEACHER
        profile.save()
