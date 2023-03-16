from rest_framework.permissions import BasePermission

class IsGeneralManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='General Manager').exists()

class IsDoctor(BasePermission):
   def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='Doctor').exists())

class IsAssistant(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Assistant').exists()

