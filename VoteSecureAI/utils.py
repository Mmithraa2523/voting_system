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
    Example: 'uploads/party_symbols/image.jpg' -> '/static/uploads/party_symbols/image.jpg'
    """
    if not filepath:
        return ''
    
    normalized = normalize_path_for_url(filepath)
    
    # If it starts with 'uploads/', prepend '/static/'
    if normalized.startswith('uploads/'):
        return f'/static/{normalized}'
    
    # If it's already an absolute path starting with /static/, return as-is
    if normalized.startswith('/static/'):
        return normalized
    
    # Otherwise, assume it's in static folder
    return f'/static/{normalized}'
