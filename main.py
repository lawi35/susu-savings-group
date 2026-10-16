"""Command-line interface for the rotating susu savings group."""
from susu import SusuGroup, SusuError


def main() -> None:
    print("Rotating Susu Savings Group")
    while True:
        try:
            group = SusuGroup(input("Fixed weekly contribution (GHS, e.g. 50.00): ").strip())
            break
        except (SusuError, ValueError) as exc:
            print(f"Invalid amount: {exc}")

    print("Add members in payout order. Enter a blank name when finished.")
    while True:
        name = input("Member name/ID: ").strip()
        if not name:
            break
        try:
            group.add_member(name)
            print(f"Added {name}.")
        except SusuError as exc:
            print(f"Could not add member: {exc}")
    if not group.members:
        print("No members added. Exiting.")
        return

    while True:
        print("\n1) Record contribution\n2) Close current week\n3) Show report\n4) Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                group.record_contribution(input("Member name/ID: ").strip(), input("Contribution amount in GHS: ").strip())
                print("Contribution recorded.")
            elif choice == "2":
                result = group.close_week()
                if result["closed"]:
                    print(f"Week closed. {result['recipient']} receives GHS {result['payout']}.")
                    print(f"Week {group.current_week} is now open.")
                else:
                    print("Week cannot close. Outstanding amounts:")
                    for member, amount in result["owes"].items():
                        print(f"  {member}: GHS {amount}")
            elif choice == "3":
                print(group.report())
            elif choice == "4":
                print("Goodbye.")
                return
            else:
                print("Choose 1, 2, 3, or 4.")
        except (SusuError, ValueError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
