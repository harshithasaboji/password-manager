import re


class BasePasswordManager:
    # list that holds all of the user's past passwords.
    old_passwords = []

    def get_password(self) -> str:
        """ This method returns the current password of the user as a string """
        return self.old_passwords and self.old_passwords[-1] or ''

    def is_correct(self, password: str) -> bool:
        """ This method receives a string and returns a boolean True or False
        depending on whether the string is equal to the current password or not."""
        return self.old_passwords and password == self.old_passwords[-1] or False

    def get_all_passwords(self) -> list:
        """ This method returns the all password of the user as a list """
        return self.old_passwords


class PasswordManager(BasePasswordManager):

    def set_password(self, password: str) -> int:
        """
        This method receives the password and sets the user's password.
        Password change is successful only if:
            - Security level of the new password is greater.
            - Length of new password is minimum 6
        However, if the old password already has the highest security level,
        new password must be of the highest or equal security level for a successful password change.

        - -1 will be returned if password length is less-than 6 characters.
        - 0 will be returned if password is set successfully.
        - 1 will be returned if password doesn't met security levels.
        - 2 will be returned if new password matches with any of the old passwords,
            and password won't be saved.
        """

        if not len(password) >= 6:
            return -1
        elif password in self.old_passwords:
            return 2
        else:
            if self.get_level(password) >= self.get_level():
                self.old_passwords.append(password)
                return 0
            else:
                return 1

    def get_level(self, password: str = None) -> int:
        """
        This method returns the security level of the current password.
        It can also check and return the security level of a new password passed as a string.
        Security levels:
            -   -1 will be returned if user do not have any passwords set
            -   0 will be returned of password consists of alphabets or numbers only.
            -   1 will be returned if password is alphanumeric.
            -   2 will be returned if password is alphanumeric passwords along with special characters.
        """
        pwd = password is not None and password or self.old_passwords and self.old_passwords[-1] or False

        if not pwd:
            return -1
        elif (any(re.compile('[a-zA-Z]+[0-9]+[!@#$%^&*()+?_=,<>/-]+').findall(pwd))
              or any(re.compile('[a-zA-Z]+[!@#$%^&*()+?_=,<>/-]+[0-9]+').findall(pwd))
              or any(re.compile('[0-9]+[a-zA-Z]+[!@#$%^&*()+?_=,<>/-]+').findall(pwd))
              or any(re.compile('[0-9]+[!@#$%^&*()+?_=,<>/-]+[a-zA-Z]+').findall(pwd))
              or any(re.compile('[!@#$%^&*()+?_=,<>/-]+[a-zA-Z]+[0-9]+').findall(pwd))
              or any(re.compile('[!@#$%^&*()+?_=,<>/-]+[0-9]+[a-zA-Z]+').findall(pwd))
        ):
            return 2
        elif any(re.compile('[a-zA-Z]+[0-9]+').findall(pwd)) or any(re.compile('[0-9]+[a-zA-Z]+').findall(pwd)):
            return 1
        elif any(re.compile('[0-9]').findall(pwd)) or any(re.compile('[a-zA-Z]').findall(pwd)):
            return 0
