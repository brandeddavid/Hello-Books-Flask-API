from api.models import User

user = User("dmwangi@gmail.com", "dmwangi", "David", "Mwangi", "password1234")
user.save()
user.promote()
