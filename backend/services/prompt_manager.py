"""
Simplified prompt manager for generating a complete website (HTML and CSS)
from a single description using local Ollama models.
"""

from typing import Dict, Optional
import logging
import re
from models.ollama_client import ChatMessage

logger = logging.getLogger(__name__)

class WebsitePromptTemplate:
    """A single, effective prompt for generating a full website."""

    SYSTEM_PROMPT = (
        "You are an expert web developer specializing in creating single-page websites. "
        "Your task is to generate clean, modern, and responsive HTML and CSS based on a user's description. "
        "Provide the complete HTML file first, then the complete CSS file. "
        "Do not use any placeholder comments."
    )

    @staticmethod
    def website_prompt(description: str) -> str:
        """Creates the prompt for generating a complete website."""
        return (
            f"Generate a complete, single-page website about: '{description}'.\n\n"
            "**Requirements:**\n"
            "1.  **HTML:** A complete HTML5 structure in a single `index.html` file. Use semantic tags (e.g., `<header>`, `<main>`, `<section>`, `<footer>`). Link to an external stylesheet named `style.css`.\n"
            "2.  **CSS:** A complete stylesheet in a single `style.css` file. Use modern CSS practices like Flexbox or Grid for layout. Ensure the design is responsive and looks good on both desktop and mobile devices.\n\n"
            "**Output Format:**\n"
            "Provide the code for each file separately, enclosed in markdown-style code blocks with language identifiers.\n"
            "Example:\n"
            "```html\n"
            "<!DOCTYPE html>\n"
            "<html>\n"
            "...\n"
            "</html>\n"
            "```\n\n"
            "```css\n"
            "body {\n"
            "...\n"
            "}\n"
            "```\n\n"
            "Begin generating the website now."
        )

class WebsitePromptManager:
    """Manages the generation and parsing of a complete website."""

    def __init__(self, ollama_client):
        self.client = ollama_client
        self.templates = WebsitePromptTemplate()

    async def generate_website_from_description(
        self,
        description: str,
        model_name: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generates both HTML and CSS from a single description and returns them as a dictionary.
        """
        prompt = self.templates.website_prompt(description)
        model_to_use = model_name or self.client.model_name
        logger.info(f"Generating website for '{description}' using model {model_to_use}")

        try:
            # Use the non-streaming completion method for simplicity
            completion = await self.client.generate_completion(
                messages=[
                    ChatMessage(role="system", content=self.templates.SYSTEM_PROMPT),
                    ChatMessage(role="user", content=prompt),
                ],
                model_name=model_to_use
            )
            full_response = completion.content or ""
            return self._parse_website_code(full_response)
        except Exception as e:
            logger.error(f"Error during website generation: {e}")
            raise

    def _parse_website_code(self, response: str) -> Dict[str, str]:
        """
        Parses the LLM response to extract HTML and CSS code blocks.
        """
        html_match = re.search(r"```html\n(.*?)\n```", response, re.DOTALL)
        css_match = re.search(r"```css\n(.*?)\n```", response, re.DOTALL)

        html_code = html_match.group(1).strip() if html_match else ""
        css_code = css_match.group(1).strip() if css_match else ""

        # Fallback if the model didn't follow the format perfectly
        if not html_code and not css_match:
            # Assume the whole response is HTML with embedded CSS
            return {"html": response, "css": ""}
            
        if not html_code and "html" in response.lower():
             html_code = response # Assume it's all html

        return {"html": html_code, "css": css_code}
