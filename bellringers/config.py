"""
Configuration settings for Bell Ringers app
"""
import os


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

    # Admin defaults (change these!)
    DEFAULT_ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    DEFAULT_ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'changeme123')
