from django.test import TestCase
from . models import Profile, Project
from django.contrib.auth.models import User

# Create your tests here.
class ProfileTest(TestCase):
    def setUp(self):
        self.belinda = User(username = 'Belinda',email = 'codesrunner@gmail.com')
        self.belinda = Profile(user = self.belinda,user = 1,bio = 'tests',photo = 'test.jpg',date_craeted='june,12.2022')

    def test_instance(self):
        self.assertTrue(isinstance(self.belinda,Profile))

    def test_save_profile(self):
        Profile.save_profile(self)
        all_profiles = Profile.objects.all()
        self.assertTrue(len(all_profiles),0)

    def test_delete_profile(self):
        self.dorcas.delete_profile()
        all_profiles = Profile.objects.all()
        self.assertEqual(len(all_profiles),0)



class ProjectsTestCase(TestCase):
    def setUp(self):
        self.new_post = Project(title = 'testT',projectscreenshot = 'test.jpg',description = 'testD',user = 'belinda',projecturl = 'https://test.com',datecreated='june,12.2022')


    def test_save_project(self):
        self.new_post.save_project()
        pictures = Profile.objects.all()
        self.assertEqual(len(pictures),1)

    def test_delete_project(self):
        self.new_post.delete_project()
        pictures = Project.objects.all()
        self.assertEqual(len(pictures),1)  