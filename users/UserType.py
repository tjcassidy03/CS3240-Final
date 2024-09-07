class UserType:
    ANONYMOUS = "Anonymous"
    COMMON = "Common"
    IFC_ADMIN = "IFC JC Admin"
    IFC_COUNSELOR = "IFC JC Counselor"
    DJANGO_ADMIN = "Django Admin"

    def __init__(self, user_type):
        self.user_type = user_type