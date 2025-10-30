"""
Google Gemini API integration for generating bell ringers
"""
import os
import google.generativeai as genai


def configure_gemini():
    """Configure Gemini API with API key from environment"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    genai.configure(api_key=api_key)


def generate_bell_ringer(topic, format_type, constraint):
    """
    Generate a bell ringer using Gemini 2.0 Flash model

    Args:
        topic: CS topic (e.g., Variables, Loops, Data Structures)
        format_type: Question format (e.g., Debug the Code, Predict Output)
        constraint: Teaching constraint (e.g., 5-Minute Timer, AP-Level Review)

    Returns:
        Generated bell ringer content as formatted text
    """
    configure_gemini()

    # Use the gemini-2.0-flash model
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    # Craft a detailed prompt for the specific combination
    prompt = f"""You are an expert Computer Science teacher creating a high-quality bell ringer (warm-up exercise) for a CS class.

Generate a bell ringer with these specifications:
- **Topic**: {topic}
- **Format**: {format_type}
- **Constraint**: {constraint}

Requirements:
1. The activity should be completable within 5-10 minutes
2. Include clear instructions for students
3. For code-based questions, use Python unless otherwise appropriate
4. Make it engaging and appropriate for the constraint level
5. Include an answer key or expected output at the end

Format your response as:
# Bell Ringer: {topic}

## Instructions
[Clear student-facing instructions]

## Problem
[The actual problem/exercise]

## Answer Key
[Solution or expected output]

Make this pedagogically sound and immediately printable."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating bell ringer: {str(e)}"


def get_topic_options():
    """Return list of available topics"""
    return [
        "Variables",
        "Loops",
        "Conditionals",
        "Functions",
        "Data Structures",
        "Object-Oriented Programming",
        "Recursion",
        "Algorithms",
        "AI & Machine Learning",
        "Cybersecurity",
        "Binary & Number Systems",
        "Web Development",
        "Databases"
    ]


def get_format_options():
    """Return list of available formats"""
    return [
        "Debug the Code",
        "Predict the Output",
        "Vocabulary Match",
        "Code Tracing",
        "Short Answer",
        "Pseudocode Challenge",
        "Fill in the Blanks",
        "Multiple Choice",
        "Code Completion",
        "Real-World Application"
    ]


def get_constraint_options():
    """Return list of available constraints"""
    return [
        "5-Minute Timer",
        "Partner Discussion",
        "No Computers",
        "Analogy Time",
        "Introductory Level",
        "Intermediate Level",
        "AP-Level Review",
        "Think-Pair-Share",
        "Visual Diagram",
        "Quiz Prep"
    ]
