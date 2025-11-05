"""
Document parser module for extracting text and data from financial statements
"""

import os
from typing import Dict, Any, List
from pathlib import Path
import PyPDF2
from PIL import Image
import base64
import io


class DocumentParser:
    """
    Handles parsing of financial documents (PDF and images)
    """
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.png', '.jpg', '.jpeg']
    
    def parse_document(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a financial document and extract content
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        if file_ext == '.pdf':
            return self._parse_pdf(file_path)
        else:
            return self._parse_image(file_path)
    
    def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract text from PDF file"""
        text_content = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                text_content.append({
                    'page': page_num + 1,
                    'text': text
                })
        
        return {
            'type': 'pdf',
            'num_pages': num_pages,
            'content': text_content,
            'file_path': file_path
        }
    
    def _parse_image(self, file_path: str) -> Dict[str, Any]:
        """Process image file for multimodal analysis"""
        image = Image.open(file_path)
        
        # Convert image to base64 for API transmission
        buffered = io.BytesIO()
        image.save(buffered, format=image.format or 'PNG')
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            'type': 'image',
            'format': image.format,
            'size': image.size,
            'base64': img_base64,
            'file_path': file_path
        }
