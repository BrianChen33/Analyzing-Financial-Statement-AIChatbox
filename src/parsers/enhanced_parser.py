"""
Enhanced document parser supporting Excel, CSV, and XBRL formats
"""

import os
from typing import Dict, Any, List
from pathlib import Path
import PyPDF2
from PIL import Image
import base64
import io

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False


class EnhancedDocumentParser:
    """
    Handles parsing of financial documents (PDF, images, Excel, CSV, XBRL)
    """
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.png', '.jpg', '.jpeg', '.xls', '.xlsx', '.csv', '.xbrl', '.xml']
    
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
        elif file_ext in ['.png', '.jpg', '.jpeg']:
            return self._parse_image(file_path)
        elif file_ext in ['.xls', '.xlsx']:
            return self._parse_excel(file_path)
        elif file_ext == '.csv':
            return self._parse_csv(file_path)
        elif file_ext in ['.xbrl', '.xml']:
            return self._parse_xbrl(file_path)
        else:
            raise ValueError(f"Unsupported format: {file_ext}")
    
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
    
    def _parse_excel(self, file_path: str) -> Dict[str, Any]:
        """Parse Excel file using pandas"""
        if not PANDAS_AVAILABLE:
            raise ValueError("pandas is required for Excel parsing. Install with: pip install pandas openpyxl")
        
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        sheets_data = {}
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            sheets_data[sheet_name] = {
                'data': df.to_dict('records'),
                'columns': df.columns.tolist(),
                'shape': df.shape
            }
        
        return {
            'type': 'excel',
            'sheets': list(sheets_data.keys()),
            'content': sheets_data,
            'file_path': file_path
        }
    
    def _parse_csv(self, file_path: str) -> Dict[str, Any]:
        """Parse CSV file using pandas"""
        if not PANDAS_AVAILABLE:
            raise ValueError("pandas is required for CSV parsing. Install with: pip install pandas")
        
        df = pd.read_csv(file_path)
        
        return {
            'type': 'csv',
            'data': df.to_dict('records'),
            'columns': df.columns.tolist(),
            'shape': df.shape,
            'file_path': file_path
        }
    
    def _parse_xbrl(self, file_path: str) -> Dict[str, Any]:
        """Parse XBRL file"""
        import xml.etree.ElementTree as ET
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Extract financial data from XBRL
            financial_data = {}
            namespaces = {'xbrli': 'http://www.xbrl.org/2003/instance'}
            
            # This is a simplified parser - production would need more sophisticated parsing
            for elem in root.iter():
                if elem.text and elem.text.strip():
                    tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                    financial_data[tag_name] = elem.text.strip()
            
            return {
                'type': 'xbrl',
                'data': financial_data,
                'file_path': file_path
            }
        except Exception as e:
            return {
                'type': 'xbrl',
                'error': f'Failed to parse XBRL: {str(e)}',
                'file_path': file_path
            }
