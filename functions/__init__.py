#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自媒体内容生成工具 - Functions模块
包含所有核心功能的实现
"""

__version__ = "2.0.0"
__author__ = "AI Assistant"

# 延迟导入，避免导入时的依赖问题
__all__ = [
    'content_main',
    'generate_image', 
    'generate_batch_images',
    'process_magazine',
    'analyze_all_magazines',
    'display_magazine_table',
    'check_github_updates',
    'update_repo_if_needed'
]

def __getattr__(name):
    """延迟导入函数"""
    if name == 'content_main':
        from .content_generator import main
        return main
    elif name == 'generate_image':
        from .image_generator import generate_image
        return generate_image
    elif name == 'generate_batch_images':
        from .image_generator import generate_batch_images
        return generate_batch_images
    elif name == 'process_magazine':
        from .summarizer import process_magazine
        return process_magazine
    elif name == 'analyze_all_magazines':
        from .magazine_analyzer import analyze_all_magazines
        return analyze_all_magazines
    elif name == 'display_magazine_table':
        from .magazine_analyzer import display_magazine_table
        return display_magazine_table
    elif name == 'check_github_updates':
        from .github_updater import check_github_updates
        return check_github_updates
    elif name == 'update_repo_if_needed':
        from .github_updater import update_repo_if_needed
        return update_repo_if_needed
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")