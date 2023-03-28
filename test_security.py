from unittest import TestCase
from security import BasePasswordManager, PasswordManager


class TestBasePasswordManager(TestCase):

    def setUp(self) -> None:
        self.bpw = BasePasswordManager()

    def test_get_password(self):
        # First test, without method arguments
        self.assertEqual(self.bpw.get_password(), '')

        # Second test
        # Given
        self.bpw.old_passwords = li = ['password', 'security']
        # Then
        self.assertEqual(self.bpw.get_password(), li[-1])

    def test_is_correct(self):
        # first test
        self.assertFalse(self.bpw.is_correct('password'))

        # second test
        # given
        self.bpw.old_passwords = ['password']
        # then
        self.assertTrue(self.bpw.is_correct('password'))

    def test_get_all_passwords(self):
        # first test
        self.assertFalse(self.bpw.get_all_passwords())

        # second test
        # given
        self.bpw.old_passwords = li = ['password', 'security']
        # then
        self.assertEqual(self.bpw.get_all_passwords(), li)

    def tearDown(self) -> None:
        del self.bpw


class TestPasswordManager(TestCase):

    def setUp(self) -> None:
        self.pw = PasswordManager()

    def tearDown(self) -> None:
        del self.pw

    def test_set_password(self):
        # first test, with less-than 6 characters
        self.assertEqual(self.pw.set_password('12345'), -1)

        # second test, with alphanumeric and special characters
        # given
        password_123 = 'password@123'
        self.pw.old_passwords = [password_123]
        # then
        self.assertEqual(self.pw.set_password('%s' % password_123), 2)

        # third test, with only numeric characters which is less secured than old password
        self.assertEqual(self.pw.set_password('123456'), 1)

        # fourth test, with alphanumeric and special characters which is equal secured to old password
        self.assertEqual(self.pw.set_password('password$123'), 0)

    def test_get_level(self):
        # first test, without any method arguments
        self.assertEqual(self.pw.get_level(), -1)

        # given
        pwd = ['123456', 'password123', 'password@123']
        zero, one, two = 0, 1, 2

        # then
        # second test, with only numeric value
        self.assertEqual(self.pw.get_level(pwd[zero]), zero)

        # third test, with alphanumeric value
        self.assertEqual(self.pw.get_level(pwd[one]), one)

        # fourth test, with alphanumeric and special characters
        self.assertEqual(self.pw.get_level(pwd[two]), two)

        # fifth test, with only numeric value
        # given
        self.pw.old_passwords.append(pwd[zero])
        # then
        self.assertEqual(self.pw.get_level(), zero)

        # sixth test, with alphanumeric value
        # given
        self.pw.old_passwords.append(pwd[one])
        # then
        self.assertEqual(self.pw.get_level(), one)

        # seventh test, with alphanumeric and special characters
        # given
        self.pw.old_passwords.append(pwd[two])
        # then
        self.assertEqual(self.pw.get_level(), two)
