from .models import UserProfile
from django.contrib.auth.models import User

def add_variable_to_context(request):
    try:
        username = User.objects.get(username=request.user.username)
        ProfileObj = UserProfile.objects.get(User=username)
        avatar = ProfileObj.ProfilePic.url
    except:
        avatar = '/media/default.png'
    return {
        'avatar': avatar
    }