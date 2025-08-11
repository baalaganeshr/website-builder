"""
Simplified prompt manager for website building with local Ollama models.
Optimized for 'gpt-oss-20b' and 'llama3.2:3b' with short, effective prompts.
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class WebsitePromptTemplate:
    """Simple, effective prompts optimized for local models"""
    
    # System prompts - kept short for local model efficiency
    HTML_SYSTEM = "You are a web developer. Create clean, modern HTML with embedded CSS. Use semantic HTML5 and responsive design."
    
    CSS_SYSTEM = "You are a CSS expert. Create modern, responsive styles using Flexbox/Grid. Focus on clean design and good UX."
    
    REACT_SYSTEM = "You are a React developer. Create functional components with hooks. Use TypeScript and modern practices."

    @staticmethod
    def html_prompt(description: str, requirements: str = "") -> str:
        """Short HTML generation prompt"""
        req_text = f"\nAdditional: {requirements}" if requirements else ""
        return f"Create a complete HTML page: {description}{req_text}\n\nRequirements:\n- Complete HTML with embedded CSS\n- Responsive design\n- Modern styling\n- Semantic HTML5\n\nReturn only the HTML code:"
    
    @staticmethod
    def css_prompt(description: str, html: str = "") -> str:
        """Short CSS generation prompt"""
        html_text = f"\nHTML context: {html[:200]}..." if html else ""
        return f"Create CSS for: {description}{html_text}\n\nRequirements:\n- Modern responsive CSS\n- Flexbox/Grid layouts\n- Good color scheme\n- Mobile-first\n\nReturn only CSS code:"
    
    @staticmethod
    def react_prompt(description: str, props: List[str] = None) -> str:
        """Short React component prompt"""
        props_text = f"\nProps: {', '.join(props)}" if props else ""
        return f"Create React component: {description}{props_text}\n\nRequirements:\n- Functional component with hooks\n- TypeScript\n- Modern JSX\n- Good styling\n\nReturn only the component code:"
    
    @staticmethod
    def enhance_prompt(code: str, request: str) -> str:
        """Short enhancement prompt"""
        return f"Enhance this code: {request}\n\nCode:\n{code}\n\nReturn only the improved code:"
    
    @staticmethod
    def fix_prompt(code: str, issues: str) -> str:
        """Short fix prompt"""
        return f"Fix these issues: {issues}\n\nCode:\n{code}\n\nReturn only the fixed code:"


class WebsitePromptManager:
    """Simple prompt manager for local Ollama models"""
    
    def __init__(self, ollama_client):
        self.client = ollama_client
        self.templates = WebsitePromptTemplate()
    
    async def generate_html_page(
        self, 
        description: str, 
        additional_requirements: str = "",
        model_name: Optional[str] = None
    ) -> str:
        """Generate HTML page using local model"""
        try:
            prompt = self.templates.html_prompt(description, additional_requirements)
            logger.info(f"Generating HTML with {model_name or self.client.model_name}")
            
            response = ""
            async for chunk in self.client.generate_stream(
                prompt=prompt,
                model=model_name,
                system_prompt=self.templates.HTML_SYSTEM
            ):
                response += chunk
            
            return self._extract_code(response)
        except Exception as e:
            logger.error(f"HTML generation error: {e}")
            raise
    
    async def generate_css_styles(
        self, 
        mockup_description: str, 
        existing_html: str = "",
        model_name: Optional[str] = None
    ) -> str:
        """Generate CSS styles using local model"""
        try:
            prompt = self.templates.css_prompt(mockup_description, existing_html)
            logger.info(f"Generating CSS with {model_name or self.client.model_name}")
            
            response = ""
            async for chunk in self.client.generate_stream(
                prompt=prompt,
                model=model_name,
                system_prompt=self.templates.CSS_SYSTEM
            ):
                response += chunk
            
            return self._extract_code(response)
        except Exception as e:
            logger.error(f"CSS generation error: {e}")
            raise
    
    async def generate_react_component(
        self, 
        component_description: str, 
        props: List[str] = None,
        model_name: Optional[str] = None
    ) -> str:
        """Generate React component using local model"""
        try:
            prompt = self.templates.react_prompt(component_description, props)
            logger.info(f"Generating React with {model_name or self.client.model_name}")
            
            response = ""
            async for chunk in self.client.generate_stream(
                prompt=prompt,
                model=model_name,
                system_prompt=self.templates.REACT_SYSTEM
            ):
                response += chunk
            
            return self._extract_code(response)
        except Exception as e:
            logger.error(f"React generation error: {e}")
            raise
    
    async def enhance_existing_code(
        self, 
        existing_code: str, 
        enhancement_request: str,
        model_name: Optional[str] = None
    ) -> str:
        """Enhance existing code using local model"""
        try:
            prompt = self.templates.enhance_prompt(existing_code, enhancement_request)
            logger.info(f"Enhancing code with {model_name or self.client.model_name}")
            
            response = ""
            async for chunk in self.client.generate_stream(
                prompt=prompt,
                model=model_name
            ):
                response += chunk
            
            return self._extract_code(response)
        except Exception as e:
            logger.error(f"Code enhancement error: {e}")
            raise
    
    async def fix_code_issues(
        self, 
        problematic_code: str, 
        issues_description: str,
        model_name: Optional[str] = None
    ) -> str:
        """Fix code issues using local model"""
        try:
            prompt = self.templates.fix_prompt(problematic_code, issues_description)
            logger.info(f"Fixing code with {model_name or self.client.model_name}")
            
            response = ""
            async for chunk in self.client.generate_stream(
                prompt=prompt,
                model=model_name
            ):
                response += chunk
            
            return self._extract_code(response)
        except Exception as e:
            logger.error(f"Code fixing error: {e}")
            raise
    
    async def create_full_website(
        self, 
        site_description: str, 
        pages: List[str] = None,
        model_name: Optional[str] = None
    ) -> Dict[str, str]:
        """Create complete website using local model"""
        try:
            pages_text = f" with pages: {', '.join(pages)}" if pages else ""
            prompt = f"Create a complete website: {site_description}{pages_text}\n\nGenerate multiple files if needed. Return organized code:"
            
            logger.info(f"Creating website with {model_name or self.client.model_name}")
            
            response = ""
            async for chunk in self.client.generate_stream(
                prompt=prompt,
                model=model_name,
                system_prompt=self.templates.HTML_SYSTEM
            ):
                response += chunk
            
            return self._parse_files(response)
        except Exception as e:
            logger.error(f"Website creation error: {e}")
            raise
    
    def _extract_code(self, response: str) -> str:
        """Extract code from model response"""
        response = response.strip()
        
        # Remove code fences
        if "```" in response:
            parts = response.split("```")
            for i, part in enumerate(parts):
                if i % 2 == 1:  # Odd indices are code blocks
                    # Skip language specifier line
                    lines = part.split('\n')
                    if len(lines) > 1:
                        return '\n'.join(lines[1:]).strip()
        
        # Remove common prefixes
        prefixes = ["Here's", "Here is", "I'll create", "This is"]
        for prefix in prefixes:
            if response.startswith(prefix):
                lines = response.split('\n')
                return '\n'.join(lines[1:]).strip()
        
        return response
    
    def _parse_files(self, response: str) -> Dict[str, str]:
        """Parse multi-file response"""
        files = {}
        
        if "index.html" in response.lower():
            # Try to split by file indicators
            parts = response.split("```")
            current_file = "index.html"
            
            for i, part in enumerate(parts):
                if i % 2 == 1:  # Code block
                    files[current_file] = part.strip()
                elif "style.css" in part.lower():
                    current_file = "style.css"
                elif ".js" in part.lower():
                    current_file = "script.js"
        
        if not files:
            files["index.html"] = self._extract_code(response)
        
        return files
