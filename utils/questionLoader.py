import os
import re
from typing import Dict, List, Any
import streamlit as st

class QuestionLoader:
    def __init__(self, questions_dir: str = "questions"):
        self.questions_dir = questions_dir
        self.questions_cache = {}
        self.module_file_mapping = {}  # Cache for module name to file mapping
    
    def _build_module_file_mapping(self):
        """Build a mapping of module names to their corresponding files"""
        if self.module_file_mapping:
            return  # Already built
        
        if not os.path.exists(self.questions_dir):
            return
        
        for filename in os.listdir(self.questions_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(self.questions_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    # Extract module name from content
                    module_match = re.search(r'# Module: (.+)', content)
                    if module_match:
                        module_name = module_match.group(1).strip()
                        self.module_file_mapping[module_name] = filename
                except Exception as e:
                    st.error(f"Error reading {filename}: {e}")
    
    def parse_markdown_file(self, filepath: str) -> Dict[str, Any]:
        """Parse a markdown file and extract question data"""
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract module title
        module_match = re.search(r'# Module: (.+)', content)
        module_name = module_match.group(1).strip() if module_match else "Unknown Module"
        
        # Extract metadata
        metadata = self._extract_metadata(content)
        
        # Extract questions
        questions = self._extract_questions(content)
        
        return {
            "module_name": module_name,
            "metadata": metadata,
            "questions": questions
        }
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from markdown content"""
        metadata = {}
        metadata_section = re.search(r'## Metadata\n(.*?)\n## Questions', content, re.DOTALL)
        
        if metadata_section:
            metadata_text = metadata_section.group(1)
            for line in metadata_text.split('\n'):
                line = line.strip()
                if line.startswith('- **') and '**: ' in line:
                    # Extract key-value pair
                    key_value = line[4:]  # Remove '- **'
                    key, value = key_value.split('**: ', 1)
                    metadata[key] = value
        
        return metadata
    
    def _extract_questions(self, content: str) -> List[Dict[str, Any]]:
        """Extract questions from markdown content"""
        questions = []
        
        # Split content by question headers
        question_sections = re.split(r'### Question (\d+)', content)[1:]  # Skip first empty element
        
        # Process pairs (question_num, question_content)
        for i in range(0, len(question_sections), 2):
            if i + 1 < len(question_sections):
                question_num = question_sections[i]
                question_content = question_sections[i + 1]
                
                question_data = self._parse_single_question(question_content)
                question_data['id'] = int(question_num)
                questions.append(question_data)
        
        return questions
    
    def _parse_single_question(self, content: str) -> Dict[str, Any]:
        """Parse a single question from markdown content"""
        question_data = {}
        
        # Extract question text
        question_match = re.search(r'\*\*Question\*\*: (.+)', content)
        question_data['question'] = question_match.group(1).strip() if question_match else ""
        
        # Extract type
        type_match = re.search(r'\*\*Type\*\*: (.+)', content)
        question_data['type'] = type_match.group(1).strip() if type_match else "multiple_choice"
        
        # Extract difficulty
        difficulty_match = re.search(r'\*\*Difficulty\*\*: (\d+)', content)
        question_data['difficulty'] = int(difficulty_match.group(1)) if difficulty_match else 1
        
        # Extract options
        options_section = re.search(r'\*\*Options\*\*:\n(.*?)\n\*\*Correct\*\*:', content, re.DOTALL)
        if options_section:
            options_text = options_section.group(1)
            options = []
            for line in options_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    options.append(line[2:])  # Remove '- '
            question_data['options'] = options
        else:
            question_data['options'] = []
        
        # Extract correct answer
        correct_match = re.search(r'\*\*Correct\*\*: (.+)', content)
        question_data['correct'] = correct_match.group(1).strip() if correct_match else ""
        
        # Extract explanation
        explanation_match = re.search(r'\*\*Explanation\*\*: (.+)', content)
        question_data['explanation'] = explanation_match.group(1).strip() if explanation_match else ""
        
        # Extract tips
        tips_section = re.search(r'\*\*Tips\*\*:\s*\n(.*?)(?=\n---|$)', content, re.DOTALL)
        tips = []
        if tips_section:
            tips_text = tips_section.group(1)
            for line in tips_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    tips.append(line[2:])
        question_data['tips'] = tips
        
        return question_data
    
    def load_module_questions(self, module_name: str) -> Dict[str, Any]:
        """Load questions for a specific module"""
        if module_name in self.questions_cache:
            return self.questions_cache[module_name]
        
        # Build mapping if not done yet
        self._build_module_file_mapping()
        
        # Find the correct file for this module
        filename = self.module_file_mapping.get(module_name)
        
        if not filename:
            # Fallback: try to create filename from module name
            safe_filename = re.sub(r'[^\w\s-]', '', module_name).strip()
            safe_filename = re.sub(r'[-\s]+', '_', safe_filename)
            filename = f"{safe_filename}.md"
        
        filepath = os.path.join(self.questions_dir, filename)
        
        if os.path.exists(filepath):
            try:
                questions_data = self.parse_markdown_file(filepath)
                self.questions_cache[module_name] = questions_data
                return questions_data
            except Exception as e:
                st.error(f"Error parsing {filename}: {e}")
                return {"module_name": module_name, "metadata": {}, "questions": []}
        else:
            return {"module_name": module_name, "metadata": {}, "questions": []}
    
    def get_available_modules(self) -> List[str]:
        """Get list of available question modules"""
        if not os.path.exists(self.questions_dir):
            return []
        
        modules = []
        for filename in os.listdir(self.questions_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(self.questions_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                    module_match = re.search(r'# Module: (.+)', content)
                    if module_match:
                        module_name = module_match.group(1).strip()
                        modules.append(module_name)
                        # Also update the mapping
                        self.module_file_mapping[module_name] = filename
                except Exception as e:
                    st.error(f"Error reading {filename}: {e}")
        
        return sorted(modules)  # Return sorted list for consistency
    
    def filter_questions_by_difficulty(self, questions: List[Dict], min_difficulty: int, max_difficulty: int) -> List[Dict]:
        """Filter questions by difficulty range"""
        return [q for q in questions if min_difficulty <= q.get('difficulty', 1) <= max_difficulty]
    
    def clear_cache(self):
        """Clear the question cache (useful for development)"""
        self.questions_cache.clear()
        self.module_file_mapping.clear()