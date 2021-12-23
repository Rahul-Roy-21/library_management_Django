from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

from .models import StudentProfile

def student_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='Student')
		instance.groups.add(group)
        
		StudentProfile.objects.create(user=instance)
		print('Student-Profile created Along with User-Registration !!')

post_save.connect(student_profile, sender=User)
# We can also Use @post-save(sender=User)