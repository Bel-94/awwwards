from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    photo = CloudinaryField('images', default='https://res.cloudinary.com/dz275mqsc/image/upload/v1654858776/default_nbsolf.png')
    bio = models.TextField(max_length=150,)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    datecreated = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user_username_icontains=name).all()

class Project(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=350)
    projectscreenshot = CloudinaryField('images')
    projecturl = models.URLField(max_length=250)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner', null=True)
    datecreated = models.DateField(auto_now_add=True)

    def save_projects(self):
        self.user

    def delete_project(self):
        self.delete()

    @classmethod
    def search_projects(cls, search_term):
        return cls.objects.filter(title_icontains=search_term).all()

RATE_CHOICES = [
(1,'1- Trash'),
(2,'2- Horrible'),
(3,'3- Terrible'),
(4,'4- Bad'),
(5,'5- Ok'),
(6,'6- Watchable'),
(7,'7- Good'),
(8,'8- Very Good'),
(9,'9- perfect'),
(10,'10- Master Piece'),
]

class Rateview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    text = models.TextField(max_length=500, blank=True)
    design = models.PositiveSmallIntegerField(choices=RATE_CHOICES, default=0)
    usability = models.PositiveSmallIntegerField(choices=RATE_CHOICES, default=0)
    content = models.PositiveSmallIntegerField(choices=RATE_CHOICES, default=0)
    
    def __str__(self):
        return self.user.username
    

