"""
Standards management for Bell Ringers
Reads CS standards from markdown file or uses defaults
"""
import os
import re


STANDARDS_FILE = os.path.join(os.path.dirname(__file__), 'standards', 'Intro_CS.md')


def parse_standards_from_markdown(file_path):
    """Parse standards from a markdown file

    Expected format:
    ## Standard Code
    Description of the standard
    """
    standards = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse markdown sections
        # Looking for patterns like "## 1A-AP-10" or "## CS.1.2.3"
        pattern = r'##\s+([A-Z0-9\.\-]+)\s*\n+(.*?)(?=##|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)

        for code, description in matches:
            # Clean up the description
            description = description.strip()
            # Take first paragraph as the main description
            first_para = description.split('\n\n')[0]
            standards[code.strip()] = first_para.strip()

    except FileNotFoundError:
        pass  # Will use defaults

    return standards


def get_default_standards():
    """Default CS standards if no file is provided"""
    return {
        "None": "No specific standard - generate general content",
        "1A-AP-08": "Model daily processes by creating and following algorithms",
        "1A-AP-09": "Model the way programs store and manipulate data",
        "1A-AP-10": "Develop programs with sequences and simple loops",
        "1A-AP-11": "Decompose tasks into smaller, manageable subtasks",
        "1A-AP-12": "Develop plans that describe program sequences and events",
        "1A-AP-14": "Debug errors in an algorithm or program",
        "1A-AP-15": "Use correct terminology in identifying and describing programs",
        "1B-AP-08": "Compare and refine multiple algorithms for the same task",
        "1B-AP-09": "Create programs using compound conditionals and loops",
        "1B-AP-10": "Create programs using procedures with and without parameters",
        "1B-AP-11": "Create programs using lists and iteration",
        "1B-AP-12": "Modify programs to remove errors and add functionality",
        "1B-AP-15": "Test and refine programs using criteria and design specifications",
        "1B-AP-16": "Take on roles in teams when developing programs",
        "2-AP-10": "Use flowcharts or pseudocode to design algorithms",
        "2-AP-11": "Create procedures with parameters to organize code",
        "2-AP-12": "Design and develop programs using lists",
        "2-AP-13": "Decompose problems into smaller components",
        "2-AP-14": "Create procedures that use APIs or libraries",
        "2-AP-16": "Incorporate testing throughout program development",
        "2-AP-17": "Design programs to respond to user events",
        "2-AP-19": "Document code for readability and maintainability",
        "3A-AP-13": "Create prototypes that use algorithms to solve problems",
        "3A-AP-14": "Use lists to simplify solutions to complex problems",
        "3A-AP-15": "Justify the selection of data structures",
        "3A-AP-16": "Design and iteratively develop programs with event handlers",
        "3A-AP-17": "Decompose complex problems into smaller sub-problems",
        "3A-AP-18": "Create programming artifacts using design processes",
        "3A-AP-21": "Evaluate and refine computational artifacts",
        "3B-AP-08": "Describe how artificial intelligence drives applications",
        "3B-AP-09": "Implement an AI algorithm to address a problem",
        "3B-AP-10": "Use and adapt classic algorithms",
        "3B-AP-11": "Evaluate algorithms in terms of efficiency and correctness",
        "3B-AP-14": "Construct solutions using procedural abstraction",
        "3B-AP-16": "Demonstrate code reuse by creating libraries",
        "3B-AP-21": "Develop programs for multiple platforms",
        "3B-AP-22": "Evaluate computational solutions for impacts",
    }


def get_standards():
    """Get standards from file or return defaults"""
    # Try to parse from file first
    standards = parse_standards_from_markdown(STANDARDS_FILE)

    # If no standards loaded from file, use defaults
    if not standards:
        standards = get_default_standards()

    return standards


def get_standard_description(code):
    """Get description for a specific standard code"""
    standards = get_standards()
    return standards.get(code, "No description available")


def get_standards_list():
    """Get list of (code, description) tuples for dropdown"""
    standards = get_standards()
    return sorted(standards.items(), key=lambda x: (x[0] != "None", x[0]))
