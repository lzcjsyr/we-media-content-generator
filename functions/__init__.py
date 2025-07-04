#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
内容生成器模块包
提供内容生成、图片生成和期刊摘要等功能
"""

from .content_generator import main as generate_content
from .image_generator import generate_image, generate_batch_images
from .summarizer import main as generate_summary

__all__ = ['generate_content', 'generate_image', 'generate_batch_images', 'generate_summary']