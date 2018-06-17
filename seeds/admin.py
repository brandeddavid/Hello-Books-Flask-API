
"""
[
    This file creates the system's admin seed.
    The system needs an initial admin on first run.
]
"""
from api.models import User

user = User("dmwangi@gmail.com", "dmwangi", "David", "Mwangi", "password1234")
user.save()
user.promote()
