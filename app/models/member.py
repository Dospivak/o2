from datetime import datetime, timedelta
from decimal import Decimal

class Member:
    PLANS = {
        'A': {'name': 'Plán A', 'price': Decimal('199'), 'includes_package': False},
        'B': {'name': 'Plán B', 'price': Decimal('399'), 'includes_package': False},
        'C': {'name': 'Plán C', 'price': Decimal('599'), 'includes_package': False},
        'D': {'name': 'Plán D', 'price': Decimal('799'), 'includes_package': True}
    }
    PACKAGE_PRICE = Decimal('99')

    def __init__(self, member_id, name, plan_type, start_date, has_package=False):
        self.member_id = member_id
        self.name = name
        self.plan = plan_type
        self.start_date = start_date if isinstance(start_date, datetime) else datetime.strptime(start_date, '%Y-%m-%d')
        self.has_package = has_package and not self.PLANS[plan_type]['includes_package']
        self.active = True

    def calculate_package_price(self, order_date):
        """Vypočítá cenu balíčku podle zbývajících dnů v období"""
        if not self.has_package or self.PLANS[self.plan]['includes_package']:
            return Decimal('0')
        
        days_remaining = 30 - (order_date - self.start_date).days
        if days_remaining <= 0:
            return Decimal('0')
            
        price = (self.PACKAGE_PRICE * Decimal(days_remaining) / Decimal('30'))
        return price

    def calculate_plan_change(self, new_plan, change_date):
        """Vypočítá cenu při změně plánu"""
        if new_plan not in self.PLANS:
            raise ValueError("Neplatný typ plánu")
            
        days_used = (change_date - self.start_date).days
        if days_used >= 30 or days_used < 0:
            daily_rate = self.PLANS[self.plan]['price'] / Decimal('30')
            return {
                'refund': Decimal('0'),
                'new_price': self.PLANS[new_plan]['price'],
                'days_used': days_used,
                'days_remaining': 0,
                'package_refund': Decimal('0'),
                'plan_refund': Decimal('0'),
                'daily_plan_rate': daily_rate,
                'daily_package_rate': Decimal('0'),
                'current_plan_price': self.PLANS[self.plan]['price'],
                'package_price': self.PACKAGE_PRICE
            }

        # Výpočet vratky za nevyužité dny plánu
        days_remaining = 30 - days_used
        daily_rate = self.PLANS[self.plan]['price'] / Decimal('30')
        plan_refund = (daily_rate * Decimal(days_remaining))

        # Calculate package refund only when changing to Plan D and user has a package
        package_refund = Decimal('0')
        daily_package_rate = Decimal('0')
        if self.has_package and self.PLANS[new_plan]['includes_package']:
            daily_package_rate = self.PACKAGE_PRICE / Decimal('30')
            package_refund = (daily_package_rate * Decimal(days_remaining))

        # Base price is just the plan price
        new_price = self.PLANS[new_plan]['price']

        return {
            'refund': plan_refund + package_refund,
            'new_price': new_price,
            'days_used': days_used,
            'days_remaining': days_remaining,
            'package_refund': package_refund,
            'plan_refund': plan_refund,
            'daily_plan_rate': daily_rate,
            'daily_package_rate': daily_package_rate,
            'current_plan_price': self.PLANS[self.plan]['price'],
            'package_price': self.PACKAGE_PRICE
        }

    def to_dict(self):
        return {
            'member_id': self.member_id,
            'name': self.name,
            'plan': self.plan,
            'plan_name': self.PLANS[self.plan]['name'],
            'plan_price': str(self.PLANS[self.plan]['price']),
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'has_package': self.has_package,
            'active': self.active
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            member_id=data['member_id'],
            name=data['name'],
            plan_type=data['plan'],
            start_date=data['start_date'],
            has_package=data.get('has_package', False)
        ) 