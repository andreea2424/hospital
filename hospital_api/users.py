from django.contrib.auth.models import User
from django.contrib.auth.models import Group
# create a new user
user = User.objects.create_user(username='johndoe', password='password123')

# set additional fields for the user
user.first_name = 'John'
user.last_name = 'Doe'
user.email = 'johndoe@example.com'

# assign the user to the appropriate group
doctor_group = Group.objects.get(name='Doctor')
doctor_group.user_set.add(user)

# save the user instance to the database
user.save()