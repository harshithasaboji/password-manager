import sys
from colors import Colors
from security import PasswordManager


class Options:
    # username of the user
    __username = ''

    # Show welcome message for first time
    __welcome = True

    @staticmethod
    def __ask_username() -> None:
        """ This method prompt the user to enter username through command line """
        print(f"{Colors.CYAN}Please register here{Colors.END}")
        Options.__username = input("Please enter username: ")

    @staticmethod
    def __ask_password() -> None:
        """ This method prompt the user to enter password through command line """
        pm = PasswordManager()
        secure = False
        while True:
            msg = secure is True and 'Enter new strong password' or 'Enter your new password'
            password = input(f"{msg}: ")
            set_password = pm.set_password(password)
            if set_password == -1:
                print(f'{Colors.WARNING}Password must contain at-lease 6 characters{Colors.END}')
            elif set_password == 1:
                print(f'{Colors.WARNING}New password must be secured than your old password{Colors.END}')
            elif set_password == 2:
                print(f'{Colors.WARNING}Password already exists, it cannot be set.{Colors.END}')
            else:
                message = Options.__welcome and 'Your password is set' or 'Password has changed'
                print(f'{Colors.GREEN}{message}{Colors.END}')
                break

    @staticmethod
    def __show_options() -> int:
        """
        This method continuously prompt the user to select from given option
        until the user selects the correct option through command line
         """

        wrong = False
        selection = 0

        while True:
            if not wrong:
                print(f'{Colors.BLUE}NOTE: please select from following options{Colors.END}')
            else:
                print(f'{Colors.WARNING}please select correct option{Colors.END}')

            options = (
                '1. Show all my passwords\n'
                '2. Get current password\n'
                '3. Set new password\n'
                '4. Security level of my current password\n'
                '5. Logout\n')

            try:
                selection = int(input(options))
            except ValueError as e:
                wrong = True
                continue
            else:
                if selection in [1, 2, 3, 4, 5]:
                    break
                else:
                    wrong = True
                    continue

        return selection

    @classmethod
    def check_password(cls) -> bool:
        """
        This method continuously prompt the user to enter current password to perform the selected
        action for 3. If you enter wrong password for 3rd time program will terminate
        """
        pm = PasswordManager()
        pwd = input(f'{cls.__username.title()} Enter your current password to perform the action: ')
        chances = 0
        while True:
            if pm.is_correct(pwd):
                return True
            else:
                if chances > 2:
                    sys.exit('\nYour account is blocked')
                print(f'{Colors.WARNING}You have entered wrong password{Colors.END}')
                pwd = input(f'{Colors.FAIL}You have {3 - chances} attempts left. Please try again: {Colors.END}')
                chances += 1

    @classmethod
    def main_menu(cls) -> None:
        """ This method prompt the user to select correct options through command line """

        pm = PasswordManager()

        if not cls.__username:
            cls.__ask_username()

        if not pm.get_password():
            print(f'{Colors.WARNING}You have not set password for you account{Colors.END}')
            cls.__ask_password()

        if cls.__welcome:
            print(f'\n{Colors.GREEN}', 10 * '*', 'Welcome to Password Manager', 10 * '*', f'{Colors.END}\n')
            cls.__welcome = False

        while True:
            selection = cls.__show_options()
            if selection == 1 and cls.check_password():
                print(f'{Colors.CYAN}{pm.get_all_passwords()}{Colors.END}')
            elif selection == 2 and cls.check_password():
                print(f'{Colors.CYAN}Your current password: {pm.get_password()}{Colors.END}')
            elif selection == 3 and cls.check_password():
                cls.__ask_password()
            elif selection == 4 and cls.check_password():
                level = pm.get_level()
                strength = level == 0 and 'WEAK' or level == 1 and 'STRONG' or 'VERY STRONG'
                print(f'{Colors.CYAN}Your password is: {strength}{Colors.END}')
            elif selection == 5:
                sys.exit('\nYou are logged out')
