from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

student_types = [
    ('leader', 'cohort leader'),
    ('deputy', 'vice leader'),
    ('secretary', 'secretary'),
    ('president', 'president'),
    ('member', 'member'),
    
]

UNIQUE_ROLES = ['president', 'secretary']


class Student(models.Model):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    student_type = models.CharField(max_length=100, choices=student_types, default='member')
    date_join = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        ordering = ['-date_join']    
        constraints = [
            models.UniqueConstraint(
                fields=['student_type'],
                condition=models.Q(student_type__in=UNIQUE_ROLES),
                name='unique_roles'
            )
        ]

    def save(self, *args, **kwargs):
    
        if self.student_type in UNIQUE_ROLES:
            existing_role = Student.objects.filter(
                student_type=self.student_type
            ).exclude(pk=self.pk).exists()
            if existing_role:
                raise ValidationError(f"Only one student can hold the role of {self.get_student_type_display()}.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student_Profile(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE)
    bio = models.TextField()
    date_of_birth = models.DateField()
    address = models.CharField(max_length=300)
    rating = models.FloatField(default=0.0)
    profile_picture = models.ImageField(upload_to='student_profile')
    date_join = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}"

class Program(models.Model):
    courses = models.CharField(max_length=500)
    grade = models.IntegerField(default=0.0)
    student = models.ForeignKey(Student, related_name='courses', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.courses}"

class CohortGroup(models.Model):
    name = models.CharField(max_length=200)
    date_join = models.DateTimeField(auto_now_add=True)
    student = models.ManyToManyField(Student, related_name='cohortgroup')

    def __str__(self):
        return f"{self.name}"