"""
Standards management for Bell Ringers
Reads CS standards from markdown file with hierarchical structure:
- Domains (## Domain X – Name)
- Standards (### Standard X.Y – Description)
- Performance Indicators (* **X.Y.Z** Description)
"""
import os
import re


STANDARDS_FILE = os.path.join(os.path.dirname(__file__), 'standards', 'Intro_CS.md')


def parse_standards_from_markdown(file_path):
    """Parse standards from a markdown file with hierarchical structure

    Expected format:
    ## Domain X – Domain Name
    ### Standard X.Y – Standard Description
    * **X.Y.Z** Performance indicator description

    Returns:
        Dictionary mapping performance indicator codes to descriptions
        Format: {"X.Y.Z": "Indicator description"}
    """
    standards = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by domains (## Domain X)
        domain_pattern = r'##\s+Domain\s+(\d+)\s*[–—-]\s*([^\n]+)'
        domain_sections = re.split(domain_pattern, content)

        # Process each domain (skipping the preamble)
        for i in range(1, len(domain_sections), 3):
            if i + 2 > len(domain_sections):
                break

            domain_num = domain_sections[i].strip()
            domain_name = domain_sections[i + 1].strip()
            domain_content = domain_sections[i + 2]

            # Split by standards (### Standard X.Y)
            standard_pattern = r'###\s+Standard\s+([\d\.]+)\s*[–—-]\s*([^\n]+)'
            standard_sections = re.split(standard_pattern, domain_content)

            # Process each standard
            for j in range(1, len(standard_sections), 3):
                if j + 2 > len(standard_sections):
                    break

                standard_num = standard_sections[j].strip()
                standard_desc = standard_sections[j + 1].strip()
                standard_content = standard_sections[j + 2]

                # Extract performance indicators (* **X.Y.Z** Description)
                indicator_pattern = r'\*\s+\*\*([\d\.]+)\*\*\s+([^\n]+)'
                indicators = re.findall(indicator_pattern, standard_content)

                for indicator_code, indicator_desc in indicators:
                    # Store with just the indicator description
                    # (Keep it concise for the dropdown)
                    standards[indicator_code.strip()] = indicator_desc.strip()

    except FileNotFoundError:
        pass  # Will use defaults
    except Exception as e:
        print(f"Error parsing standards file: {e}")
        pass  # Will use defaults

    return standards


def get_default_standards():
    """Default standards if no file is provided - sample from Intro CS"""
    return {
        "None": "No specific standard - generate general content",
        "1.1.1": "Demonstrate understanding of various career paths in computer science",
        "2.1.1": "Recognize situations where computational approaches would be beneficial",
        "2.1.2": "Apply computational thinking principles to problem-solving",
        "2.2.1": "Use various data types appropriately within a program",
        "2.2.2": "Create and use variables to store and manage data",
        "2.2.6": "Implement data structures to organize and manipulate collections",
        "2.3.1": "Analyze a program in terms of execution steps and expected outcomes",
        "2.3.4": "Create programs with selection control structures",
        "2.3.5": "Create programs with iteration control structures",
        "2.3.6": "Create subroutines for code modularity and reusability",
        "2.3.7": "Debug errors to ensure functionality",
        "2.4.1": "Use the console for basic data input/output operations",
        "2.5.1": "Implement consistent formatting and naming conventions",
        "3.1.1": "Categorize data into quantitative and qualitative types",
        "3.2.2": "Analyze data using descriptive statistics and visualizations",
        "4.1.1": "Define artificial intelligence and identify key subfields",
        "5.1.1": "Analyze core information security principles",
        "5.1.2": "Describe common cyber threats",
        "5.2.1": "Identify key hardware components and their roles",
        "5.3.1": "Define network concepts",
    }


def get_standards():
    """Get standards from file or return defaults"""
    # Try to parse from file first
    standards = parse_standards_from_markdown(STANDARDS_FILE)

    # If no standards loaded from file, use defaults
    if not standards:
        standards = get_default_standards()
    else:
        # Add "None" option to parsed standards
        standards = {"None": "No specific standard - generate general content", **standards}

    return standards


def get_standard_description(code):
    """Get description for a specific standard code"""
    standards = get_standards()
    return standards.get(code, "No description available")


def get_standards_list():
    """Get list of (code, description) tuples for dropdown

    Returns sorted list with "None" first, then numerically sorted indicators
    """
    standards = get_standards()

    def sort_key(item):
        code = item[0]
        # "None" comes first
        if code == "None":
            return (0, [])
        # Parse numeric codes like "2.3.7" and sort numerically
        try:
            parts = [int(x) for x in code.split('.')]
            return (1, parts)
        except (ValueError, AttributeError):
            # Fallback for non-numeric codes
            return (2, [0])

    return sorted(standards.items(), key=sort_key)
