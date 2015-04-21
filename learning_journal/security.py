from pyramid.security import Allow, Everyone, Authenticated

##
# __acl__ access control list, security container built into python
##

class ACLFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'create'),
        (Allow, Authenticated, 'edit'),
    ]
    def __init__(self, request):
        pass
