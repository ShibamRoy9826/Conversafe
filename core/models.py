from django.db import models
from PIL import Image

from landing.models import AUser


class UserProfile(models.Model):
    user = models.OneToOneField(AUser, on_delete=models.CASCADE)
    user_url = models.SlugField(unique=True)
    display_name = models.TextField(
        default="GuestUser", null=True, blank=True, max_length=30
    )

    short_bio = models.TextField(default="A new Conversafe user", max_length=100)
    long_bio = models.TextField(
        default="Description not provided by user", max_length=1000
    )
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

    GENDERS = ((MALE, "Male"), (FEMALE, "Female"), (OTHER, "Other"))

    gender = models.CharField(max_length=6, choices=GENDERS, null=True, blank=True)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    acheivements = models.IntegerField(null=True, blank=True)

    avatar = models.ImageField(
        default="profilePics/dummyProfile.png", upload_to="profilePics"
    )

    ENGLISH = "ENGLISH"
    HINDI = "HINDI"
    BENGALI = "BENGALI"
    GERMAN = "GERMAN"
    SPANISH = "SPANISH"

    LANGUAGES = (
        (ENGLISH, "en"),
        (HINDI, "hi"),
        (BENGALI, "bn"),
        (GERMAN, "de"),
        (SPANISH, "es"),
    )

    language = models.CharField(max_length=10, choices=LANGUAGES, default=ENGLISH)
    learn_lang = models.CharField(max_length=10, choices=LANGUAGES, default=ENGLISH)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.avatar.path)


class LearningSource(models.Model):
    siteName = models.CharField(max_length=30)
    siteUrl = models.CharField(max_length=500)
    urlNoProtocol = models.CharField(max_length=450)
    siteType = models.CharField(max_length=30)
