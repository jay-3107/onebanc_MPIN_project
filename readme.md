# MPIN Security Validator

## Enhancing Mobile Banking Authentication Security

Jayesh Vilas Wankhede  
OneBanc  
Gurugram

## Introduction

Mobile banking security relies heavily on strong PINs, yet users often choose guessable combinations based on personal data or common sequences. The MPIN Validator analyzes 4-digit and 6-digit PINs against common patterns and demographic information (birthdays, anniversaries) to provide immediate feedback on PIN strength with specific weakness identification, helping users create more secure authentication credentials.

## Background

Mobile banking PIN vulnerabilities pose significant security risks as studies show many PINs can be guessed in few attempts. Users frequently select easily exploitable PINs based on birthdates, simple sequences, and repeated digits. Financial security standards recommend avoiding personal information, implementing multi-factor authentication, and periodic PIN rotation.

## Problem Statement

1. Weak MPINs create immediate financial vulnerability as unauthorized access can lead to fraudulent transactions, account takeovers, and data breaches.
2. Traditional PIN validation fails to detect demographic-based patterns where users transform personal dates (birthdays, anniversaries) into seemingly random numbers.
3. OneBank's security initiative requires an automated solution to analyze PIN strength against both common sequences and customer-specific demographic information.

## Requirement Analysis

Progressive functional requirements included:
- Detection of common 4-digit PINs
- Validation against demographic data
- Structured weakness categorization with specific reason codes
- Extension to support 6-digit PINs

The solution implements comprehensive validation that identifies not only obvious patterns but also complex transformations of personal data (like reversed birth years or combined day-month patterns), validated through extensive test cases.

## Technical Approach

1. Modular architecture separating core validation logic, pattern generation, and user interface
2. Python implementation leveraging string manipulation capabilities, datetime libraries, and testing frameworks
3. Hierarchical rule-based validation system 
4. Sophisticated date pattern analysis that extracts components and generates permutations
5. Extensible weakness categorization system with specific reason codes

## Implementation Details

### Component Breakdown

1. **Validator Core**
   - `pin_data.py`: Database of common weak PINs
   - `validator_core.py`: Main validation engine
   - `component_extractor.py`: Analyzes PINs to extract meaningful components

2. **CLI Interface**
   - `main.py`: User-friendly command-line interface with argument parsing, input validation, and formatted output

3. **Pattern Generators**
   - `pattern_generator.py`: Core engine identifying weakening patterns
   - `special_patterns.py`: Handles complex pattern recognition

4. **Demographic Pattern Detection**
   - Sophisticated personal information detection through component extraction and pattern matching

### PIN Strength Evaluation Algorithm

- Multi-factor scoring system:
  1. Base Entropy Calculation
  2. Pattern Penalty System
  3. Weighted Scoring Model
  4. Final Classification (Very Weak, Weak, Moderate, or Strong)

### User Interface Design

- Color-coded outputs
- Progressive disclosure with detailed analysis via `--verbose` flag
- Batch processing support
- Interactive mode with real-time feedback
- Comprehensive testing framework

## Testing Methodology

### Test-Driven Development Approach

Implemented comprehensive test-driven development methodology defining expected behaviors before coding, with an automated testing framework that compares actual results against expected outcomes.

### Test Case Categories

- **Common PIN Detection (Tests 1-4)**
  - Validates identification of frequently used PINs

- **Demographic Pattern Detection (Tests 5-12)**
  - Tests date-based patterns in various formats

- **Edge Cases (Tests 13-20)**
  - Handles strong PINs with demographics present
  - Tests reversed date patterns

- **Enhanced Pattern Detection (Tests 21-33)**
  - Tests sophisticated pattern recognition

- **Real-World Scenarios (Tests 34-45)**
  - Covers current date/time references
  - Tests username-derived patterns

- **Directional Keyboard Patterns (Tests 46-55)**
  - Tests vertical, horizontal, and diagonal sequences

- **Complex Keyboard Patterns (Tests 56-65)**
  - Tests knight's move patterns and other complex sequences

- **Combined Pattern Vulnerabilities (Tests 66-70)**
  - Tests keyboard patterns with demographic data matches

### Coverage Analysis

Test suite implements 70 distinct test scenarios covering all critical validation paths across multiple dimensions, including PIN length variants, various date formats, reversal patterns, cross-date mixing, and multiple weakness detection in single PINs.

## Usage

### Running the Application

```shell script
python main.py 
```

Options:
- `--demographics`: Provide demographic data for enhanced validation
- `--verbose`: Show detailed analysis
- `--batch`: Process multiple PINs from a file

### Running the Tests

```shell script
python test_validator.py
```

## Conclusion

This project delivers a comprehensive MPIN validation system that detects vulnerabilities in both 4-digit and 6-digit PINs through multi-layered analysis. The implementation successfully identifies common patterns, demographic-based combinations, and sophisticated transformations with high accuracy across all test cases.

The advanced pattern detection algorithm identifies not just obvious sequences but also transformed personal data that traditional validators would miss, addressing a critical security gap in mobile authentication. The modular architecture provides specific weakness codes rather than simple pass/fail results, enabling actionable security improvements.