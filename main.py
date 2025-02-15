from membership_manager import MembershipManager

def main():
    manager = MembershipManager()
    
    while True:
        print("\n=== Membership Management System ===")
        print("1. Add new member")
        print("2. View member info")
        print("3. List packages")
        print("4. Calculate package price")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            member_id = input("Enter member ID: ")
            name = input("Enter member name: ")
            print("\nAvailable packages:")
            for pkg, details in manager.list_packages().items():
                print(f"- {pkg}: ${details['price']}/month")
            package_type = input("Enter package type: ")
            
            try:
                manager.add_member(member_id, name, package_type)
                print("Member added successfully!")
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == '2':
            member_id = input("Enter member ID: ")
            member = manager.get_member_info(member_id)
            if member:
                print("\nMember Information:")
                print(f"Name: {member['name']}")
                print(f"Package: {member['package']}")
                print(f"Start Date: {member['start_date']}")
                print(f"End Date: {member['end_date']}")
                print(f"Active: {member['active']}")
            else:
                print("Member not found!")
                
        elif choice == '3':
            packages = manager.list_packages()
            print("\nAvailable Packages:")
            for pkg, details in packages.items():
                print(f"\n{details['name']} Package:")
                print(f"Price: ${details['price']}")
                print(f"Duration: {details['duration_months']} month(s)")
                print("Features:", ", ".join(details['features']))
                
        elif choice == '4':
            package_type = input("Enter package type: ")
            try:
                price = manager.calculate_price(package_type)
                print(f"Price for {package_type} package: ${price}")
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == '5':
            print("Thank you for using the Membership Management System!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 