"""
Google Gemini API integration for generating bell ringers
"""
import os
import google.generativeai as genai
from . import standards as standards_module


def configure_gemini():
    """Configure Gemini API with API key from environment"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    genai.configure(api_key=api_key)


def generate_bell_ringer(topic, format_type, constraint, standard_codes=[], user_prompt=""):
    """
    Generate a bell ringer using Gemini 2.0 Flash model

    Args:
        topic: CS topic (e.g., Variables, Loops, Data Structures)
        format_type: Question format (e.g., Debug the Code, Predict Output)
        constraint: Teaching constraint (e.g., 5-Minute Timer, AP-Level Review)
        standard_codes: List of CS standard codes to align with
        user_prompt: Optional user-provided keyword or phrase to customize content

    Returns:
        Generated bell ringer content as formatted HTML
    """
    configure_gemini()

    # Use the gemini-2.0-flash model
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    # Get standard descriptions if provided
    standard_text = ""
    if standard_codes and len(standard_codes) > 0:
        standards_list = []
        for code in standard_codes:
            standard_desc = standards_module.get_standard_description(code)
            standards_list.append(f"{code} - {standard_desc}")
        standard_text = "\n- **Standards**: " + "; ".join(standards_list)

    # Add prompt context if provided
    prompt_text = ""
    if user_prompt:
        prompt_text = f"\n- **User Focus**: Incorporate or relate to: {user_prompt}"

    # Craft a detailed prompt for the specific combination
    ai_prompt = f"""You are an expert Computer Science teacher creating a high-quality bell ringer (warm-up exercise) for a CS class.

Generate a bell ringer with these specifications:
- **Topic**: {topic}
- **Format**: {format_type}
- **Constraint**: {constraint}{standard_text}{prompt_text}

Requirements:
1. The activity should be completable within 5-10 minutes
2. Include clear instructions for students
3. For code-based questions, use Python unless otherwise appropriate
4. Make it engaging and appropriate for the constraint level
5. Include an answer key or expected output at the end
6. {"Align the content with the specified standards" if standard_codes else ""}

Format your response as HTML with these exact sections:
<div class="bell-ringer-content">
    <h2>Bell Ringer: {topic}</h2>

    <div class="section instructions">
        <h3>Instructions</h3>
        <p>[Clear, concise student-facing instructions]</p>
    </div>

    <div class="section problem">
        <h3>Problem</h3>
        <p>[The problem description]</p>
        <pre><code>[Any code snippets here - properly formatted]</code></pre>
    </div>

    <div class="section answer-key">
        <h3>Answer Key</h3>
        <p>[Explanation of solution]</p>
        <pre><code>[Solution code if applicable]</code></pre>
    </div>
</div>

IMPORTANT:
- Wrap ALL code in <pre><code> tags
- Keep content concise for printing on letter-sized paper
- Use proper HTML paragraphs and formatting
- Do NOT include any markdown formatting
- Only include the <div class="bell-ringer-content"> and its contents, no other HTML wrapper"""

    try:
        response = model.generate_content(ai_prompt)
        content = response.text

        # Clean up any markdown that might have slipped through
        content = content.replace('```python', '<pre><code class="language-python">')
        content = content.replace('```', '</code></pre>')

        # Remove any 'html' or '```html' tags that Gemini might add
        content = content.replace('```html', '').replace('```', '')
        content = content.strip()

        # Ensure content starts and ends cleanly
        if '<div class="bell-ringer-content">' not in content:
            # Model didn't follow format, wrap it
            content = f'<div class="bell-ringer-content">{content}</div>'

        return content
    except Exception as e:
        return f'<div class="bell-ringer-content"><div class="error">Error generating bell ringer: {str(e)}</div></div>'


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
