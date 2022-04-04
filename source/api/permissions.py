from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly as DjangoModelPerms

class QuotePermissions(DjangoModelPerms):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }