import re
from passlib.hash import pbkdf2_sha512


class Utils:
    @staticmethod
    def email_is_valid(email: str) -> bool:
        """
        Check user input against the regular expression
        expected input in format of an email
        :param email: example@example.com
        :return:
        """
        email_address_matcher = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password: str):
        """
        Hash a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hash_password(password: str, hashed_password: str):
        """
        Checks that the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at this stage.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)
