from rest_framework import permissions

class IsLibrarianOrReadOnly(permissions.BasePermission):
    """
    Custom permission: 
    - Librarians (Staff) can do anything.
    - Members can only perform GET (viewing).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff