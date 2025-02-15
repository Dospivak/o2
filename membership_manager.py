import json
from datetime import datetime, timedelta

class MembershipManager:
    def __init__(self):
        self.packages = {
            'basic': {
                'name': 'Basic',
                'price': 29.99,
                'duration_months': 1,
                'features': ['Gym access', 'Locker room']
            },
            'premium': {
                'name': 'Premium',
                'price': 49.99,
                'duration_months': 1,
                'features': ['Gym access', 'Locker room', 'Group classes', 'Pool access']
            },
            'annual': {
                'name': 'Annual',
                'price': 299.99,
                'duration_months': 12,
                'features': ['Gym access', 'Locker room', 'Group classes', 'Pool access', 'Personal trainer']
            }
        }
        self.members = self._load_members()

    def _load_members(self):
        try:
            with open('members.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _save_members(self):
        with open('members.json', 'w') as file:
            json.dump(self.members, file, indent=4)

    def add_member(self, member_id, name, package_type):
        if package_type not in self.packages:
            raise ValueError("Invalid package type")

        start_date = datetime.now()
        end_date = start_date + timedelta(days=30 * self.packages[package_type]['duration_months'])

        self.members[member_id] = {
            'name': name,
            'package': package_type,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'active': True
        }
        self._save_members()

    def get_member_info(self, member_id):
        return self.members.get(member_id)

    def list_packages(self):
        return self.packages

    def calculate_price(self, package_type):
        if package_type not in self.packages:
            raise ValueError("Invalid package type")
        return self.packages[package_type]['price'] 