from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: allow read-only for anyone, but only allow modifying
    or deleting objects if the request.user is considered the owner.

    NOTE: your Book model must have an ownership field (e.g. created_by FK to User)
    for this to be meaningful. If not, you can adapt to use the Author relation
    (e.g. allow only if request.user == book.author.user) depending on your domain.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions require an 'owner' attribute on the object
        return getattr(obj, "created_by", None) == request.user