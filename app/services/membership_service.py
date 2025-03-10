from datetime import datetime, timedelta
from decimal import Decimal
import json
from app.models.member import Member

class MembershipService:
    def __init__(self):
        self.members = {}

    def list_plans(self):
        """Vrátí seznam dostupných plánů"""
        return Member.PLANS

    def calculate_initial_price(self, plan_type, has_package, start_date):
        """Vypočítá počáteční cenu členství"""
        if plan_type not in Member.PLANS:
            raise ValueError("Neplatný typ plánu")

        total = Member.PLANS[plan_type]['price']
        if has_package:
            total += Member.PACKAGE_PRICE

        return {
            'plan_price': Member.PLANS[plan_type]['price'],
            'package_price': Member.PACKAGE_PRICE if has_package else Decimal('0'),
            'total': total
        }

    def calculate_plan_change(self, member_id, new_plan, change_date, wants_package=False):
        """Vypočítá změnu plánu pro člena"""
        if member_id not in self.members:
            raise ValueError("Člen nenalezen")
            
        member = self.members[member_id]
        
        # Check if this is just adding a package without changing plans
        if new_plan == member.plan and not member.has_package and wants_package:
            days_used = (change_date - member.start_date).days
            days_remaining = 30 - days_used if days_used < 30 else 0
            
            # Calculate prorated package price for remaining days
            prorated_package_price = (Member.PACKAGE_PRICE * Decimal(days_remaining) / Decimal('30')).quantize(Decimal('0.01'))
            
            return {
                'current_plan': member.plan,
                'current_plan_name': Member.PLANS[member.plan]['name'],
                'new_plan': member.plan,
                'new_plan_name': Member.PLANS[member.plan]['name'],
                'days_used': days_used,
                'days_remaining': days_remaining,
                'refund_amount': Decimal('0'),
                'plan_refund': Decimal('0'),
                'package_refund': Decimal('0'),
                'new_plan_price': Member.PLANS[member.plan]['price'],
                'final_price': prorated_package_price,
                'has_package': True,
                'daily_plan_rate': Member.PLANS[member.plan]['price'] / Decimal('30'),
                'current_plan_price': Member.PLANS[member.plan]['price'],
                'package_price': Member.PACKAGE_PRICE,
                'prorated_package_price': prorated_package_price,
                'is_adding_package': True
            }
        
        # Regular plan change logic
        result = member.calculate_plan_change(new_plan, change_date)
        
        # Get current package status and plan info
        has_package = member.has_package
        current_plan_includes_package = Member.PLANS[member.plan]['includes_package']
        new_plan_includes_package = Member.PLANS[new_plan]['includes_package']
        
        # Calculate final price
        final_price = result['new_price']
        days_remaining = result['days_remaining']
        
        # Handle package logic for different scenarios
        if new_plan_includes_package:
            # If moving to Plan D, package is included in price
            has_package = True
        elif wants_package:
            # When changing plans, charge full package price (not prorated)
            # since it's considered a new contract period
            final_price += Member.PACKAGE_PRICE
            has_package = True
        elif has_package and not new_plan_includes_package:
            # Only charge for the remaining days - this is a refund scenario
            package_price = (Member.PACKAGE_PRICE * Decimal(days_remaining) / Decimal('30')).quantize(Decimal('0.01'))
            final_price += package_price
        else:
            has_package = False
        
        return {
            'current_plan': member.plan,
            'current_plan_name': Member.PLANS[member.plan]['name'],
            'new_plan': new_plan,
            'new_plan_name': Member.PLANS[new_plan]['name'],
            'days_used': result['days_used'],
            'days_remaining': result['days_remaining'],
            'refund_amount': result['refund'],
            'plan_refund': result['plan_refund'],
            'package_refund': result['package_refund'],
            'new_plan_price': result['new_price'],
            'final_price': final_price - result['refund'],
            'has_package': has_package,
            'daily_plan_rate': result['daily_plan_rate'],
            'current_plan_price': result['current_plan_price'],
            'package_price': result['package_price'],
            'is_adding_package': False
        }

    def add_member(self, member_id, name, plan_type, start_date, has_package=False):
        """Přidá nového člena"""
        if member_id in self.members:
            raise ValueError("Členské ID již existuje")

        if plan_type not in Member.PLANS:
            raise ValueError("Neplatný typ plánu")

        member = Member(
            member_id=member_id,
            name=name,
            plan_type=plan_type,
            start_date=start_date,
            has_package=has_package
        )
        self.members[member_id] = member
        return member

    def get_member_info(self, member_id):
        """Získá informace o členovi"""
        member = self.members.get(member_id)
        return member.to_dict() if member else None

    def list_packages(self):
        return self.packages

    def calculate_price(self, package_type):
        if package_type not in self.packages:
            raise ValueError("Invalid package type")
        return self.packages[package_type]['price'] 