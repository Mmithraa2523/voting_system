"""
Utility functions for the voting system
"""
import os


def normalize_path_for_url(filepath):
    """
    Normalize a file path for use in URLs
    Converts backslashes to forward slashes for cross-platform compatibility
    """
    if not filepath:
        return ''
    # Convert all backslashes to forward slashes
    return filepath.replace('\\', '/')


def get_url_path(filepath):
    """
    Convert a filesystem path to a URL path
    Example: 'static/uploads/party_symbols/image.jpg' -> '/uploads/party_symbols/image.jpg'
    Example: 'uploads/party_symbols/image.jpg' -> '/uploads/party_symbols/image.jpg'
    """
    if not filepath:
        return ''
    
    normalized = normalize_path_for_url(filepath)
    
    # Remove 'static/' prefix if present
    if normalized.startswith('static/'):
        normalized = normalized[7:]  # Remove 'static/' (7 characters)
    
    # If it starts with 'uploads/', prepend '/'
    if normalized.startswith('uploads/'):
        return f'/{normalized}'
    
    # If it's already an absolute path starting with /, return as-is
    if normalized.startswith('/'):
        return normalized
    
    # Otherwise, assume it's in uploads folder
    return f'/uploads/{normalized}'
