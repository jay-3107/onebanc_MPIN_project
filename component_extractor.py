"""
MPIN Validator - Date component extraction functionality
"""
from datetime import datetime


class DateComponentExtractor:
    """
    Extracts date components that could be used in PINs
    """

    def extract_date_components(self, date_str):
        """
        Extract all possible date components that could be used in PIN combinations.

        Args:
            date_str (str): Date string in YYYY-MM-DD format

        Returns:
            dict: Dictionary of date components
        """
        if not date_str:
            return {}

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            # Return empty dict for invalid dates
            return {}

        day = date_obj.day
        month = date_obj.month
        year = date_obj.year

        # All possible components with their label and value
        components = {
            "D": f"{day:02d}",  # Day with zero padding (01-31)
            "D_nz": f"{day}",  # Day without zero padding (1-31)
            "M": f"{month:02d}",  # Month with zero padding (01-12)
            "M_nz": f"{month}",  # Month without zero padding (1-12)
            "YY": f"{year % 100:02d}",  # Last 2 digits of year (00-99)
            "YYYY": f"{year}",  # Full 4-digit year
            "YY_1": f"{year // 100:02d}",  # First 2 digits of year (19, 20, etc.)
            "YY_2": f"{year % 100:02d}",  # Last 2 digits of year again (for clarity)

            # Add reversed components
            "D_rev": f"{day:02d}"[::-1],  # Reversed day (10 -> 01)
            "M_rev": f"{month:02d}"[::-1],  # Reversed month (10 -> 01)
            "YY_rev": f"{year % 100:02d}"[::-1],  # Reversed year (89 -> 98)
            "YYYY_rev": f"{year}"[::-1],  # Reversed full year (1990 -> 0991)

            # Add individual digits for more granular combinations
            "D_1": f"{day:02d}"[0],  # First digit of day
            "D_2": f"{day:02d}"[1],  # Second digit of day
            "M_1": f"{month:02d}"[0],  # First digit of month
            "M_2": f"{month:02d}"[1],  # Second digit of month
            "Y_1": f"{year}"[0],  # First digit of year
            "Y_2": f"{year}"[1],  # Second digit of year
            "Y_3": f"{year}"[2],  # Third digit of year
            "Y_4": f"{year}"[3],  # Fourth digit of year

            # Special: Full date reversed
            "FULL_REV": f"{year}{month:02d}{day:02d}"[::-1],  # Full date reversed

            # Special: Day repeated
            "DD": f"{day:02d}{day:02d}",  # Day repeated (e.g. 2525)

            # Full date components
            "MD": f"{month:02d}{day:02d}",  # Month+Day (e.g., 0725)
            "DM": f"{day:02d}{month:02d}",  # Day+Month (e.g., 2507)
            "YMD": f"{year % 100:02d}{month:02d}{day:02d}",  # YearMonthDay (e.g., 040725)
            "MDY": f"{month:02d}{day:02d}{year % 100:02d}",  # MonthDayYear (e.g., 072504)

            # Special: Common patterns
            "YYDD": f"{year % 100:02d}{day:02d}",  # YY+DD (e.g., 0425)
            "DDAY": f"{day:02d}{year % 100:02d}",  # DD+YY (e.g., 2504)

            # Store raw date for special case matching
            "RAW_DATE": date_str,  # Store the original date
        }

        return components

    def extract_date_patterns(self, date_str, pin_length):
        """
        Extract all possible date patterns that could be used in a PIN.

        Args:
            date_str (str): Date string in YYYY-MM-DD format
            pin_length (int): Length of the PIN

        Returns:
            list: List of possible PIN patterns derived from the date
        """
        components = self.extract_date_components(date_str)
        if not components:
            return []

        patterns = []

        # Define common pattern templates based on PIN length
        if pin_length == 4:
            # Define all possible 4-digit patterns
            pattern_templates = [
                ["D", "M"],  # DDMM
                ["M", "D"],  # MMDD
                ["YY", "M"],  # YYMM
                ["M", "YY"],  # MMYY
                ["YY", "D"],  # YYDD
                ["D", "YY"],  # DDYY
                ["YY_1", "YY_2"],  # Year first half + Year second half
                ["D", "D"],  # Day repeated (e.g., 2525)
                ["M", "M"],  # Month repeated (e.g., 0707)
                ["D_rev", "M_rev"],  # Reversed day-month
                ["YY_rev", "D_rev"],  # Reversed year-day
                ["YY"],  # Just year (e.g., 0404) - will repeat internally
            ]
        elif pin_length == 6:
            # Define all possible 6-digit patterns
            pattern_templates = [
                ["D", "M", "YY"],  # DDMMYY
                ["M", "D", "YY"],  # MMDDYY
                ["YY", "M", "D"],  # YYMMDD
                ["D", "YY", "M"],  # DDYYMM
                ["M", "YY", "D"],  # MMYYDD
                ["YY", "D", "M"],  # YYDDMM
                ["YYYY", "D"],  # YYYYDD
                ["YYYY", "M"],  # YYYYMM
                ["D", "D", "D"],  # Day repeated thrice (e.g., 252525)
                ["M", "M", "M"],  # Month repeated thrice (e.g., 070707)
                ["D", "M", "D"],  # Day-Month-Day (e.g., 250725)
                ["M", "D", "M"],  # Month-Day-Month (e.g., 072507)
                ["YMD"],  # Combined YearMonthDay
                ["MDY"],  # Combined MonthDayYear
                ["DD", "YY"],  # Day repeated + Year (e.g., 252504)
                ["YY", "DD"],  # Year + Day repeated (e.g., 042525)
                ["FULL_REV"],  # Full date reversed
            ]

        # Generate all pattern permutations
        for template in pattern_templates:
            try:
                # Create the pattern from components
                pattern = "".join(components[comp] for comp in template)

                # Only add if pattern has the correct length
                if len(pattern) == pin_length:
                    patterns.append(pattern)

                    # Also add reversed pattern for certain templates
                    if "FULL_REV" not in template:  # Don't reverse already reversed patterns
                        patterns.append(pattern[::-1])
            except:
                # Skip this template if any component is missing
                continue

        # Add special patterns for repetitions
        if pin_length == 4:
            # Add day repeated
            day = components.get("D", "")
            if len(day) == 2:
                patterns.append(day + day)  # e.g., 2525

        elif pin_length == 6:
            # Add day repeated thrice
            day = components.get("D", "")
            if len(day) == 2:
                patterns.append(day + day + day)  # e.g., 252525

            # Add month-day-month pattern
            month = components.get("M", "")
            day = components.get("D", "")
            if len(month) == 2 and len(day) == 2:
                patterns.append(month + day + month)  # e.g., 072507
                patterns.append(day + month + day)  # e.g., 250725

        # Remove duplicates
        return list(set(patterns))

    def extract_components_by_length(self, components, length):
        """
        Extract component values of a specific length.

        Args:
            components (dict): Component dictionary
            length (int): Required component length

        Returns:
            list: List of components with matching length
        """
        extracted = []

        # Go through each component
        for key, value in components.items():
            if isinstance(value, str) and len(value) == length:
                extracted.append(value)

        # Also include all possible substring variations for longer components
        for key, value in components.items():
            if isinstance(value, str) and len(value) > length:
                # Generate all possible substrings of the required length
                for i in range(len(value) - length + 1):
                    extracted.append(value[i:i + length])

        return extracted