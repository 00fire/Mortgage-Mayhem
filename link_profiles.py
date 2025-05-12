# link_profiles.py
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from app2.models import UserProfile

User = get_user_model()

for p in UserProfile.objects.filter(user__isnull=True):
    u, created = User.objects.get_or_create(
        username=p.username,
        defaults={"password": make_password(p.password or "changeme123")},
    )
    p.user = u
    p.save(update_fields=["user"])
    print("linked", p.username, "(new)" if created else "(exists)")
