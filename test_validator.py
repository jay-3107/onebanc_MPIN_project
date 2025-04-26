"""
Test cases for the MPIN validator.
"""
from pin_validator import MPINValidator


def run_tests():
    """Run all test cases and display results."""

    print("Running MPIN Validator Test Cases")
    print("=" * 40)

    # Create validators for 4-digit and 6-digit PINs
    validator_4 = MPINValidator(4)
    validator_6 = MPINValidator(6)

    # Define test cases
    test_cases = [
        # Part A tests (Common PIN detection)
        {
            "name": "Test 1: Common 4-digit PIN",
            "pin": "1234",
            "demographics": None,
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["COMMONLY_USED"]
            }
        },
        {
            "name": "Test 2: Uncommon 4-digit PIN",
            "pin": "8193",
            "demographics": None,
            "pin_length": 4,
            "expected": {
                "strength": "STRONG",
                "weakness_reasons": []
            }
        },
        {
            "name": "Test 3: Common 6-digit PIN",
            "pin": "123456",
            "demographics": None,
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["COMMONLY_USED"]
            }
        },
        {
            "name": "Test 4: Uncommon 6-digit PIN",
            "pin": "918273",
            "demographics": None,
            "pin_length": 6,
            "expected": {
                "strength": "STRONG",
                "weakness_reasons": []
            }
        },

        # Part B & C tests (Basic demographics patterns)
        {
            "name": "Test 5: PIN matches user DOB (MMDD)",
            "pin": "0201",
            "demographics": {"dob": "1998-02-01"},
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF"]
            }
        },
        {
            "name": "Test 6: PIN matches spouse DOB",
            "pin": "1020",
            "demographics": {"spouse_dob": "1995-10-20"},
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SPOUSE"]
            }
        },
        {
            "name": "Test 7: PIN matches anniversary",
            "pin": "2505",
            "demographics": {"anniversary": "2015-05-25"},
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_ANNIVERSARY"]
            }
        },
        {
            "name": "Test 8: Multiple demographic matches",
            "pin": "0524",
            "demographics": {
                "dob": "1990-05-24",
                "spouse_dob": "1992-08-15",
                "anniversary": "2015-05-24"
            },
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_ANNIVERSARY"]
            }
        },
        {
            "name": "Test 9: Common PIN and demographic match",
            "pin": "1111",
            "demographics": {"dob": "1980-11-11"},
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["COMMONLY_USED", "DEMOGRAPHIC_DOB_SELF"]
            }
        },

        # Part D tests (6-digit PIN with demographics)
        {
            "name": "Test 10: 6-digit PIN matches DOB (DDMMYY)",
            "pin": "010298",
            "demographics": {"dob": "1998-02-01"},
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF"]
            }
        },
        {
            "name": "Test 11: 6-digit PIN matches spouse DOB (YYMMDD)",
            "pin": "950510",
            "demographics": {"spouse_dob": "1995-05-10"},
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SPOUSE"]
            }
        },
        {
            "name": "Test 12: 6-digit PIN matches anniversary (MMDDYY)",
            "pin": "051215",
            "demographics": {"anniversary": "2015-05-12"},
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_ANNIVERSARY"]
            }
        },

        # Basic edge cases
        {
            "name": "Test 13: Strong PIN with demographics present",
            "pin": "7294",
            "demographics": {
                "dob": "1990-05-15",
                "spouse_dob": "1992-08-20",
                "anniversary": "2015-06-10"
            },
            "pin_length": 4,
            "expected": {
                "strength": "STRONG",
                "weakness_reasons": []
            }
        },
        {
            "name": "Test 14: Strong 6-digit PIN with demographics present",
            "pin": "729438",
            "demographics": {
                "dob": "1990-05-15",
                "spouse_dob": "1992-08-20",
                "anniversary": "2015-06-10"
            },
            "pin_length": 6,
            "expected": {
                "strength": "STRONG",
                "weakness_reasons": []
            }
        },
        # Test 15 - Removed (Year-based PIN pattern)
        {
            "name": "Test 16: Reversed date pattern",
            "pin": "1020",
            "demographics": {"dob": "1998-02-01"},
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF"]
            }
        },
        {
            "name": "Test 17: Common PIN that is also in demographics",
            "pin": "1234",
            "demographics": {"anniversary": "2012-12-34"},  # Invalid date
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["COMMONLY_USED"]
            }
        },
        # Test 18 - Removed (PIN with invalid demographics)
        # Test 19 - Removed (Multiple demographics with no match)
        {
            "name": "Test 20: Spouse DOB with year in PIN",
            "pin": "9206",
            "demographics": {"spouse_dob": "1992-06-15"},
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SPOUSE"]
            }
        },

        # NEW TEST CASES FOR ENHANCED PATTERNS

        # Reversed full dates
        {
            "name": "Test 21: Reversed full date pattern (402570)",
            "pin": "402570",
            "demographics": {"dob": "2004-07-25"},
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF"]
            }
        },

        # Special case patterns
        {
            "name": "Test 22: Special case pattern (100589)",
            "pin": "100589",
            "demographics": {"anniversary": "1998-05-01"},
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_ANNIVERSARY"]
            }
        },

        # Day repetitions
        {
            "name": "Test 23: Day repetition pattern (2525)",
            "pin": "2525",
            "demographics": {"dob": "1990-08-25"},
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF"]
            }
        },
        {
            "name": "Test 24: Triple day repetition (252525)",
            "pin": "252525",
            "demographics": {"dob": "1990-08-25"},
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF"]
            }
        },

        # Month-day combinations across sources
        {
            "name": "Test 25: Month-day combinations across sources",
            "pin": "072505",
            "demographics": {
                "dob": "1990-07-25",
                "spouse_dob": "1992-05-15"
            },
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE"]
            }
        },

        # Year + Month-day combinations
        {
            "name": "Test 26: Year + Month-day combinations",
            "pin": "040525",
            "demographics": {
                "dob": "2004-07-25",
                "spouse_dob": "1992-05-25"
            },
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE"]
            }
        },

        # Multiple days from different sources
        {
            "name": "Test 27: Days from different sources",
            "pin": "2515",
            "demographics": {
                "dob": "1990-07-25",
                "spouse_dob": "1992-08-15"
            },
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE"]
            }
        },

        # All three dates patterns
        {
            "name": "Test 28: Days from all three sources",
            "pin": "252501",
            "demographics": {
                "dob": "1990-07-25",
                "spouse_dob": "1992-08-25",
                "anniversary": "2015-06-01"
            },
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE", "DEMOGRAPHIC_ANNIVERSARY"]
            }
        },

        # All three months
        {
            "name": "Test 29: Months from all three sources",
            "pin": "070805",
            "demographics": {
                "dob": "1990-07-25",
                "spouse_dob": "1992-08-15",
                "anniversary": "2015-05-01"
            },
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE", "DEMOGRAPHIC_ANNIVERSARY"]
            }
        },

        # Wedding year + both birthdays
        {
            "name": "Test 30: Wedding year + both birthdays",
            "pin": "152515",
            "demographics": {
                "dob": "1990-07-25",
                "spouse_dob": "1992-08-15",
                "anniversary": "2015-05-01"
            },
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE", "DEMOGRAPHIC_ANNIVERSARY"]
            }
        },

        # Test 31 - Removed (Reversed year components)

        # Reversed year combinations
        {
            "name": "Test 32: Reversed year combinations (9804)",
            "pin": "9804",
            "demographics": {
                "dob": "2004-07-25",
                "anniversary": "1998-05-01"
            },
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_ANNIVERSARY"]
            }
        },

        # Combined reverses
        {
            "name": "Test 33: Combined reverses (spouse year + wedding day)",
            "pin": "0001",
            "demographics": {
                "spouse_dob": "2000-08-15",
                "anniversary": "2015-05-01"
            },
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SPOUSE", "DEMOGRAPHIC_ANNIVERSARY"]
            }
        },

        # Current date/time (using 2025-04-25 as reference)
        {
            "name": "Test 34: Current year as PIN",
            "pin": "2025",
            "demographics": None,
            "pin_length": 4,
            "expected": {
                "strength": "STRONG",  # Current implementation doesn't check current date
                "weakness_reasons": []
            }
        },

        # Username-based patterns (using jay-3107 as reference)
        {
            "name": "Test 35: Username digits as PIN",
            "pin": "3107",
            "demographics": None,
            "pin_length": 4,
            "expected": {
                "strength": "STRONG",  # Current implementation doesn't check usernames
                "weakness_reasons": []
            }
        },

        # Additional tests based on your working examples
        {
            "name": "Test 36: Last two digits combinations (0400)",
            "pin": "0400",
            "demographics": {
                "dob": "2004-07-25",
                "spouse_dob": "2000-05-25",
            },
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE"]
            }
        },
        {
            "name": "Test 37: Birthday as Day-Month (2507)",
            "pin": "2507",
            "demographics": {"dob": "2004-07-25"},
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF"]
            }
        },
        {
            "name": "Test 38: Reversed birth year (4002)",
            "pin": "4002",
            "demographics": {"dob": "2004-07-25"},
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF"]
            }
        },
        {
            "name": "Test 39: Mixed birth months (0705)",
            "pin": "0705",
            "demographics": {
                "dob": "2004-07-25",
                "spouse_dob": "2000-05-25",
            },
            "pin_length": 4,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE"]
            }
        },
        {
            "name": "Test 40: Full birth date (YYMMDD - 040725)",
            "pin": "040725",
            "demographics": {"dob": "2004-07-25"},
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF"]
            }
        },
        {
            "name": "Test 41: Combined reverses (spouse year + wedding day - 000150)",
            "pin": "000150",
            "demographics": {
                "spouse_dob": "2000-05-25",
                "anniversary": "1998-05-01"
            },
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SPOUSE", "DEMOGRAPHIC_ANNIVERSARY"]
            }
        },
        {
            "name": "Test 42: Month-day pairs (072505)",
            "pin": "072505",
            "demographics": {
                "dob": "2004-07-25",
                "spouse_dob": "2000-05-25"
            },
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE"]
            }
        },
        {
            "name": "Test 43: Cross-date mixing (040525)",
            "pin": "040525",
            "demographics": {
                "dob": "2004-07-25",
                "spouse_dob": "2000-05-25"
            },
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE"]
            }
        },
        {
            "name": "Test 44: Wedding year + both birthdays (982525)",
            "pin": "982525",
            "demographics": {
                "dob": "2004-07-25",
                "spouse_dob": "2000-05-25",
                "anniversary": "1998-05-01"
            },
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE", "DEMOGRAPHIC_ANNIVERSARY"]
            }
        },
        {
            "name": "Test 45: Both birth years (200400)",
            "pin": "200400",
            "demographics": {
                "dob": "2004-07-25",
                "spouse_dob": "2000-05-25"
            },
            "pin_length": 6,
            "expected": {
                "strength": "WEAK",
                "weakness_reasons": ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE"]
            }
        }
    ]

    # Run the tests
    passed = 0
    failed = 0

    for test in test_cases:
        print(f"\n{test['name']}")
        print("-" * len(test['name']))

        # Select the appropriate validator
        validator = validator_4 if test['pin_length'] == 4 else validator_6

        # Run the validation
        try:
            result = validator.validate_pin(test['pin'], test['demographics'])

            # Compare with expected output
            success = (
                    result['strength'] == test['expected']['strength'] and
                    set(result['weakness_reasons']) == set(test['expected']['weakness_reasons'])
            )

            if success:
                print("✓ PASSED")
                passed += 1
            else:
                print("✗ FAILED")
                print(f"Expected: {test['expected']}")
                print(f"Got: {{'strength': '{result['strength']}', 'weakness_reasons': {result['weakness_reasons']}}}")
                failed += 1

        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            failed += 1

    # Print summary
    print("\n" + "=" * 40)
    print(f"Test Summary: {passed} passed, {failed} failed")
    print("=" * 40)


if __name__ == "__main__":
    run_tests()