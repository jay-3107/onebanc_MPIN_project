"""
MPIN Validator - Core functionality and validator framework
"""
from datetime import datetime
import time
from pin_data import get_common_pins
from component_extractor import DateComponentExtractor
from pattern_generator import PatternGenerator
from special_patterns import SpecialPatternDetector


class MPINValidator:
    """
    MPIN Validator class that implements comprehensive validation logic for all parts (A-D).
    """

    def __init__(self, pin_length=4):
        """
        Initialize the PIN validator with a specific PIN length.

        Args:
            pin_length (int): Length of the PIN (4 or 6 digits)
        """
        if pin_length not in (4, 6):
            raise ValueError("PIN length must be either 4 or 6")

        self.pin_length = pin_length
        self.common_pins = get_common_pins(pin_length)

        # Performance limits
        self.max_combinations = 500000  # Maximum number of combinations to generate
        self.max_execution_time = 3.0  # Maximum execution time in seconds

        # Initialize components
        self.component_extractor = DateComponentExtractor()
        self.pattern_generator = PatternGenerator(pin_length, self.max_combinations,
                                                  self.max_execution_time)
        self.special_detector = SpecialPatternDetector(pin_length)

    def validate_pin_format(self, pin):
        """
        Validate that the PIN has the correct format.

        Args:
            pin (str): The PIN to validate

        Returns:
            bool: True if the PIN format is valid, False otherwise
        """
        if not pin or not isinstance(pin, str):
            return False

        if len(pin) != self.pin_length:
            return False

        if not pin.isdigit():
            return False

        return True

    def is_common_pin(self, pin):
        """
        Part A: Check if the PIN is commonly used.

        Args:
            pin (str): The PIN to check

        Returns:
            bool: True if the PIN is common, False otherwise
        """
        return pin in self.common_pins

    def check_demographic_matches(self, pin, demographics):
        """
        Check if the PIN matches any demographic data patterns.

        Args:
            pin (str): The PIN to check
            demographics (dict): Dictionary containing demographic information

        Returns:
            list: List of weakness reasons found
        """
        if not demographics:
            return []

        weakness_reasons = []

        # Check standard patterns first (direct matches with single date patterns)
        for source, key in [
            ("dob", "DEMOGRAPHIC_DOB_SELF"),
            ("spouse_dob", "DEMOGRAPHIC_DOB_SPOUSE"),
            ("anniversary", "DEMOGRAPHIC_ANNIVERSARY")
        ]:
            if demographics.get(source):
                patterns = self.component_extractor.extract_date_patterns(demographics[source],
                                                                          self.pin_length)
                if pin in patterns:
                    weakness_reasons.append(key)

        # Check direct special cases
        special_matches = self.special_detector.check_direct_special_cases(pin, demographics)
        if special_matches:
            weakness_reasons.extend(special_matches)
            return list(set(weakness_reasons))

        # If no direct matches found, check for combined patterns
        if not weakness_reasons:
            # Generate all possible combinations
            pin_reasons = self.pattern_generator.generate_all_combinations(demographics)

            # Check if the PIN is in the generated combinations
            if pin in pin_reasons:
                weakness_reasons.extend(pin_reasons[pin])

        return list(set(weakness_reasons))  # Remove duplicates

    def get_weakness_reasons(self, pin, demographics=None):
        """
        Part C: Get all reasons why a PIN is considered weak.

        Args:
            pin (str): The PIN to evaluate
            demographics (dict): Optional demographic information

        Returns:
            list: List of weakness reasons (empty if the PIN is strong)
        """
        reasons = []

        # Check for common PIN
        if self.is_common_pin(pin):
            reasons.append("COMMONLY_USED")

        # Check demographics if provided
        if demographics:
            demographic_reasons = self.check_demographic_matches(pin, demographics)
            reasons.extend(demographic_reasons)

        return list(set(reasons))  # Remove duplicates

    def evaluate_strength(self, pin, demographics=None):
        """
        Part B: Evaluate PIN strength (WEAK or STRONG).

        Args:
            pin (str): The PIN to evaluate
            demographics (dict): Optional demographic information

        Returns:
            str: "WEAK" or "STRONG"
        """
        reasons = self.get_weakness_reasons(pin, demographics)
        return "WEAK" if reasons else "STRONG"

    def validate_pin(self, pin, demographics=None):
        """
        Full PIN validation (Parts A, B, C, D combined).

        Args:
            pin (str): The PIN to validate
            demographics (dict): Optional demographic information

        Returns:
            dict: Validation results including strength and weakness reasons
        """
        # Validate PIN format
        if not self.validate_pin_format(pin):
            raise ValueError(f"Invalid PIN format. Must be {self.pin_length} digits.")

        # Get weakness reasons
        weakness_reasons = self.get_weakness_reasons(pin, demographics)

        # Determine strength
        strength = "WEAK" if weakness_reasons else "STRONG"

        return {
            "pin": pin,
            "pin_length": self.pin_length,
            "strength": strength,
            "weakness_reasons": weakness_reasons
        }