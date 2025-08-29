from rest_framework import permissions

# 一个权限类表示一种验证权限的方式呢
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # 对任何人都开放('GET', 'HEAD', 'OPTIONS')
        # 这些都是Read-only方法
        if request.method in permissions.SAFE_METHODS:
            return True

        # 其他方法则要验证权限
        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user