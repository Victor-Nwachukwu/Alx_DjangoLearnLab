from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser to include social media profile fields 
    like bio, profile picture, and a self-referencing followers relationship.
    
    CRITICAL FIXES are included for 'groups' and 'user_permissions' to prevent 
    SystemCheckError (E304) clashes when inheriting from AbstractUser.
    """
    
    # 1. Custom Profile Fields
    bio = models.TextField(
        max_length=500, 
        blank=True, 
        null=True,
        verbose_name=_('Biography'),
        help_text=_("A short description of the user.")
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True,
        verbose_name=_('Profile Picture'),
        help_text=_("Upload a profile image for your account.")
    )
    
    # 2. Self-Referencing Many-to-Many Relationship for Followers
    # - 'self': References the CustomUser model itself.
    # - symmetrical=False: Allows User A to follow User B without User B automatically following User A.
    # - related_name='following': Allows checking users this user follows (user.following.all()).
    # - related_name='followers': Allows checking users who follow this user (user.followers.all()).
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
        verbose_name=_('Followers'),
        help_text=_("Users who follow this account.")
    )

    # 3. FIXES for E304 Clashes (Required when extending AbstractUser)
    # These override the inherited fields to provide unique reverse accessors.
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_groups", 
        related_query_name="custom_user",
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_permissions",
        related_query_name="custom_user_permission",
    )
    
    # Other inherited fields (username, email, first_name, last_name, etc.) are available

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.username