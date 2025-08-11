"""
Optimized prompt templates for website building using Ollama models.
These prompts are specifically designed for local model capabilities and context limits.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class WebsitePromptTemplate:
    """Container for website building prompt templates"""
    
    # System prompts for different tasks
    HTML_GENERATION_SYSTEM = """You are an expert web developer specializing in creating clean, modern HTML with CSS. 
When generating code:
- Use semantic HTML5 elements
- Include responsive CSS with Flexbox/Grid
- Use modern color schemes and typography
- Ensure accessibility with proper ARIA labels
- Include placeholder content that makes sense
- Generate complete, runnable code
- Keep code clean and well-structured"""

    CSS_STYLING_SYSTEM = """You are a CSS expert focused on modern, responsive design.
When creating styles:
- Use CSS Grid and Flexbox for layouts
- Implement mobile-first responsive design
- Use CSS custom properties (variables) for consistency
- Include hover effects and smooth transitions
- Follow modern design principles (good contrast, spacing)
- Use semantic class names following BEM methodology"""

    REACT_COMPONENT_SYSTEM = """You are a React developer creating functional components with hooks.
When building components:
- Use functional components with useState/useEffect hooks
- Implement proper TypeScript types
- Include JSX with semantic HTML
- Use CSS modules or styled-components for styling
- Include proper event handlers and state management
- Add PropTypes or TypeScript interfaces for type safety"""

    @staticmethod
    def create_html_from_description(description: str, additional_requirements: str = "") -> str:
        """Generate prompt for creating HTML from description"""
        return f"""Create a complete HTML page based on this description:

{description}

{additional_requirements}

Requirements:
- Generate a complete HTML page with embedded CSS
- Use semantic HTML5 elements (header, nav, main, section, footer, etc.)
- Include responsive CSS with mobile-first approach
- Use modern design with good color scheme and typography
- Include proper meta tags and structure
- Make it visually appealing with CSS Grid/Flexbox
- Add some interactive elements (hover effects, etc.)
- Use placeholder content that fits the theme
- Ensure the page is ready to use without external dependencies

Return only the complete HTML code with embedded CSS."""

    @staticmethod  
    def create_css_from_mockup(mockup_description: str, existing_html: str = "") -> str:
        """Generate prompt for creating CSS from mockup description"""
        html_context = f"\n\nExisting HTML structure:\n```html\n{existing_html}\n```" if existing_html else ""
        
        return f"""Create CSS styles to match this design mockup:

{mockup_description}{html_context}

Requirements:
- Create modern, responsive CSS
- Use CSS Grid and Flexbox for layouts
- Implement mobile-first responsive design
- Use proper color scheme with good contrast
- Include typography that matches the design
- Add hover effects and smooth transitions
- Use CSS custom properties for consistency
- Follow modern CSS best practices
- Make it visually polished and professional

Return only the CSS code."""

    @staticmethod
    def create_react_component(component_description: str, props: List[str] = None) -> str:
        """Generate prompt for creating React component"""
        props_text = f"Props needed: {', '.join(props)}" if props else "Determine props based on the requirements"
        
        return f"""Create a React functional component based on this description:

{component_description}

{props_text}

Requirements:
- Use React functional component with hooks (useState, useEffect as needed)
- Include TypeScript types/interfaces
- Use semantic HTML structure
- Include CSS-in-JS or CSS modules for styling
- Implement proper event handlers
- Add error handling where appropriate
- Include JSDoc comments for the component
- Make it reusable and well-structured
- Follow React best practices

Return the complete React component code with TypeScript."""

    @staticmethod
    def enhance_existing_code(existing_code: str, enhancement_request: str) -> str:
        """Generate prompt for enhancing existing code"""
        return f"""Enhance this existing web code based on the following request:

Enhancement request: {enhancement_request}

Existing code:
```
{existing_code}
```

Requirements:
- Improve the existing code without breaking functionality
- Add the requested enhancements
- Maintain existing working features
- Keep the code clean and well-organized
- Use modern web development best practices
- Ensure responsive design is maintained
- Add comments for new functionality
- Test that all features work together

Return the complete enhanced code."""

    @staticmethod
    def fix_code_issues(problematic_code: str, issues_description: str) -> str:
        """Generate prompt for fixing code issues"""
        return f"""Fix the issues in this web code:

Issues to fix: {issues_description}

Problematic code:
```
{problematic_code}
```

Requirements:
- Fix all identified issues
- Maintain existing functionality where possible
- Improve code quality and structure
- Add error handling if needed
- Ensure cross-browser compatibility
- Follow web standards and best practices
- Add comments explaining fixes
- Test that the code works properly

Return the complete fixed code."""

    @staticmethod
    def create_full_website(site_description: str, pages: List[str] = None) -> str:
        """Generate prompt for creating a complete multi-page website"""
        pages_text = f"Pages needed: {', '.join(pages)}" if pages else "Determine pages based on the requirements"
        
        return f"""Create a complete website based on this description:

{site_description}

{pages_text}

Requirements:
- Create a multi-page website with navigation
- Use consistent design across all pages
- Implement responsive design for mobile/desktop
- Include proper HTML structure with semantic elements
- Add CSS for professional styling
- Include interactive elements and animations
- Add proper meta tags and SEO considerations
- Use modern web development practices
- Make it production-ready
- Include placeholder content that fits the theme

Return the complete website code organized by files (HTML, CSS, JS if needed)."""


class OllamaOptimizedPrompts:
    """Prompts specifically optimized for Ollama models with context limits"""
    
    @staticmethod
    def compress_for_local_model(long_prompt: str, max_tokens: int = 2000) -> str:
        """Compress prompts to work better with local models"""
        # For local models, we need to be more concise
        lines = long_prompt.split('\n')
        essential_lines = []
        
        for line in lines:
            # Keep essential instruction words, remove verbose explanations
            if any(keyword in line.lower() for keyword in [
                'create', 'generate', 'use', 'include', 'requirements:', 'return'
            ]):
                essential_lines.append(line)
        
        compressed = '\n'.join(essential_lines)
        
        # If still too long, truncate and add essential ending
        if len(compressed.split()) > max_tokens:
            words = compressed.split()
            compressed = ' '.join(words[:max_tokens-20]) + '\n\nReturn clean, complete, working code.'
        
        return compressed
    
    @staticmethod
    def get_model_specific_prompt(base_prompt: str, model_name: str) -> str:
        """Adjust prompts based on the specific Ollama model being used"""
        if "3b" in model_name.lower():
            # For smaller models, use more direct instructions
            return f"Task: {base_prompt}\n\nGenerate clean, working code. Be concise but complete."
        elif "20b" in model_name.lower():
            # For larger models, can use more detailed instructions
            return base_prompt
        else:
            # Default handling
            return base_prompt
