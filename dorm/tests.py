from django.test import TestCase
from dorm.views import confirm
from .models import Owner

# Create your tests here.
class NullRequest(object):
    POST = dict()
class StudentViewTests(TestCase):
    def test_login(self):
        owner_set = Owner.objects.all()
        for owner in owner_set:
            if owner.user_type is not None:
                request = NullRequest()
                request.POST['userAccount'] = owner.user.username
                request.POST['userPwd'] = 'yottaliu'
                response = confirm(request)
                self.assertContains(response, owner.user_type)
