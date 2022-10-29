class UserMixin:
    def has_role(self, *args):
        roles = self.roles
        if not roles:
            return False
        user_role_names = list(map(lambda role: role.slug, roles))
        for role_name in list(args):
            if role_name in user_role_names:
                return True
        return False
