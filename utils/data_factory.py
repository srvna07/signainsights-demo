import random
import string
from datetime import datetime


class DataFactory:

    @staticmethod
    def random_string(length=4):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def random_username(prefix="user_"):
        return prefix + DataFactory.random_string()

    @staticmethod
    def random_email(prefix="user_", domain="@gmail.com"):
        return prefix + DataFactory.random_string() + domain

    @staticmethod
    def random_org_name(prefix="Test_Org"):
        return prefix + DataFactory.random_string()

    @staticmethod
    def generate_report_name(prefix="Test_Report"):
        return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    @staticmethod
    def generate_menu_name(prefix="Test_Menu"):
        return "test_" + ''.join(random.choices(string.ascii_lowercase, k=4))
