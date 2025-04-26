"""
MPIN Validator - Entry point
"""

import sys
import os
from datetime import datetime
from validator_core import MPINValidator

def display_header():
    """Display application header."""
    print("\n" + "=" * 50)
    print("  MPIN Security Validator  ".center(50, "="))
    print("=" * 50)
    print("\nThis tool evaluates the security of your Mobile PIN (MPIN)")
    print("based on common patterns and personal demographics.")
    print("\nType 'exit' at any prompt to quit the application.")

def get_date_input(prompt):
    """
    Get a date input from user with validation.

    Args:
        prompt (str): The prompt to display to the user

    Returns:
        str, None, or 'exit': Valid date string, None if skipped, or 'exit' to quit
    """
    while True:
        date_str = input(prompt)

        # Check for exit command
        if date_str.lower() == 'exit':
            return 'exit'

        # Skip if empty
        if not date_str:
            return None

        # Try to parse the date
        try:
            # Check if the date format is correct
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD format or press Enter to skip.")

def get_demographics():
    """
    Get demographic information from user.

    Returns:
        dict, None, or 'exit': Demographics dictionary, None if skipped, or 'exit' to quit
    """
    print("\nDemographic information (optional, press Enter to skip)")
    print("-" * 50)

    demographics = {}

    # Get dates with validation
    dob = get_date_input("Your date of birth (YYYY-MM-DD): ")
    if dob == 'exit':
        return 'exit'
    if dob:
        demographics["dob"] = dob

    spouse_dob = get_date_input("Spouse's date of birth (YYYY-MM-DD): ")
    if spouse_dob == 'exit':
        return 'exit'
    if spouse_dob:
        demographics["spouse_dob"] = spouse_dob

    anniversary = get_date_input("Wedding anniversary (YYYY-MM-DD): ")
    if anniversary == 'exit':
        return 'exit'
    if anniversary:
        demographics["anniversary"] = anniversary

    return demographics if demographics else None

def get_pin_length():
    """
    Get PIN length preference from user.

    Returns:
        int or 'exit': PIN length or 'exit' to quit
    """
    while True:
        pin_length = input("Select PIN length (4 or 6 digits): ")

        # Check for exit command
        if pin_length.lower() == 'exit':
            return 'exit'

        try:
            pin_length = int(pin_length)
            if pin_length not in (4, 6):
                print("Error: PIN length must be either 4 or 6.")
                continue
            return pin_length
        except ValueError:
            print("Error: Please enter a valid number (4 or 6).")

def get_pin(pin_length):
    """
    Get PIN from user.

    Returns:
        str or 'exit': PIN string or 'exit' to quit
    """
    while True:
        pin = input(f"\nEnter your {pin_length}-digit PIN: ")

        # Check for exit command
        if pin.lower() == 'exit':
            return 'exit'

        if len(pin) != pin_length:
            print(f"Error: PIN must be exactly {pin_length} digits.")
            continue
        if not pin.isdigit():
            print("Error: PIN must contain only digits.")
            continue
        return pin

def display_results(result):
    """Display validation results."""
    print("\n" + "=" * 50)
    print("  MPIN Security Assessment  ".center(50, "="))
    print("=" * 50)

    # Display strength with color if supported
    strength = result["strength"]
    if strength == "STRONG":
        strength_text = f"STRONG"
        try:
            # Use ANSI escape codes for color if supported
            if sys.platform != "win32" or "ANSICON" in os.environ:
                strength_text = f"\033[92m{strength}\033[0m"  # Green
        except:
            pass
    else:
        strength_text = f"WEAK"
        try:
            if sys.platform != "win32" or "ANSICON" in os.environ:
                strength_text = f"\033[91m{strength}\033[0m"  # Red
        except:
            pass

    print(f"\nPIN Strength: {strength_text}")

    # Display weakness reasons if any
    if result["weakness_reasons"]:
        print("\nWeakness Reasons:")
        for reason in result["weakness_reasons"]:
            if reason == "COMMONLY_USED":
                print("• This is a commonly used PIN pattern")
            elif reason == "DEMOGRAPHIC_DOB_SELF":
                print("• Contains your date of birth pattern")
            elif reason == "DEMOGRAPHIC_DOB_SPOUSE":
                print("• Contains your spouse's date of birth pattern")
            elif reason == "DEMOGRAPHIC_ANNIVERSARY":
                print("• Contains your wedding anniversary pattern")

        # Add raw array display
        print("\nWeakness Codes:")
        print(result["weakness_reasons"])
    else:
        print("\nNo weaknesses detected. Your PIN appears to be secure.")
        print("\nWeakness Codes: []")

    # Add recommendations
    print("\nRecommendations:")
    if result["strength"] == "WEAK":
        print("• Choose a PIN that is not based on personal dates")
        print("• Avoid sequential or repetitive patterns")
        print("• Consider using a randomized PIN")
    else:
        print("• Continue using strong PINs")
        print("• Change your PIN periodically")
        print("• Never share your PIN with others")

    print("\n" + "=" * 50)

def validate_another():
    """Ask if user wants to validate another PIN."""
    while True:
        choice = input("\nValidate another PIN? (y/n): ")
        if choice.lower() in ['y', 'yes']:
            return True
        elif choice.lower() in ['n', 'no', 'exit']:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def main():
    """Main function to run the menu-based CLI application."""
    display_header()

    # Store demographics for reuse across validations
    user_demographics = None

    # Main application loop
    while True:
        try:
            # If demographics aren't collected yet, get them
            if user_demographics is None:
                user_demographics = get_demographics()
                if user_demographics == 'exit':
                    print("\nExiting application. Thank you for using MPIN Validator!")
                    return 0

            # Get PIN length
            pin_length = get_pin_length()
            if pin_length == 'exit':
                print("\nExiting application. Thank you for using MPIN Validator!")
                return 0

            # Create validator
            validator = MPINValidator(pin_length)

            # Get PIN
            pin = get_pin(pin_length)
            if pin == 'exit':
                print("\nExiting application. Thank you for using MPIN Validator!")
                return 0

            # Validate PIN
            result = validator.validate_pin(pin, user_demographics)

            # Display results
            display_results(result)

            # Ask if user wants to validate another PIN
            if not validate_another():
                print("\nExiting application. Thank you for using MPIN Validator!")
                break

        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            return 1
        except Exception as e:
            print(f"\nError: {str(e)}")
            # Don't exit on errors, just continue the loop
            if not validate_another():
                return 1

    return 0

if __name__ == "__main__":
    import os
    sys.exit(main())