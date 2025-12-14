from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser to add custom fields 
    and resolve reverse accessor clashes (E304).
    """
    
    # --- Custom Fields (Example, adjust as needed) ---
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profiles/', 
        null=True, 
        blank=True
    )
    # ----------------------------------------------------

    # --- FIX for E304: Define groups and user_permissions with unique related_name ---

    # Fix 1: Groups clash
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to.'
        ),
        # CRITICAL: Use a unique name for the reverse relationship
        related_name="custom_user_groups", 
        related_query_name="custom_user_group",
    )
    
    # Fix 2: User Permissions clash
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        # CRITICAL: Use a unique name for the reverse relationship
        related_name="custom_user_permissions",
        related_query_name="custom_user_permission_query",
    )
    # ---------------------------------------------------------------------------------

    def __str__(self):
        return self.username
