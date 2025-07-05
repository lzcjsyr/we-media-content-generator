#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
期刊分析器模块
负责分析期刊文件数量、摘要完成情况等统计信息
"""

import os
import glob
import re
from .summarizer import MAGAZINE_CONFIG, REPO_PATH

def parse_date_from_filename(filename, magazine_type):
    """从文件名中解析日期，处理不同期刊的文件名格式"""
    # 通用的日期匹配模式：YYYY.MM.DD
    match = re.search(r'(\d{4})\.(\d{2})\.(\d{2})', filename)
    return f"{match.group(1)}-{match.group(2)}-{match.group(3)}" if match else None

def get_magazine_paths(magazine_type, base_output_dir):
    """获取杂志相关的路径和文件信息（修复版本）"""
    if magazine_type not in MAGAZINE_CONFIG:
        raise ValueError(f"未知的杂志类型: {magazine_type}")
    
    config = MAGAZINE_CONFIG[magazine_type]
    base_path = os.path.join(REPO_PATH, config['base_dir'])
    
    # 修复输出目录路径计算
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # 向上一级到项目根目录
    
    if os.path.isabs(base_output_dir):
        magazine_output_dir = os.path.join(base_output_dir, config['title'])
    else:
        magazine_output_dir = os.path.join(project_root, base_output_dir, config['title'])
    
    # 确保输出目录存在
    os.makedirs(magazine_output_dir, exist_ok=True)
    
    # 查找所有符合模式的目录
    magazine_dirs = glob.glob(os.path.join(base_path, config['folder_pattern']))
    
    # 收集所有EPUB文件并解析日期，去重处理
    epub_info = []
    seen_dates = {}  # 用于跟踪已见过的日期
    
    for dir_path in magazine_dirs:
        if os.path.isdir(dir_path):
            epub_files = glob.glob(os.path.join(dir_path, config['file_pattern']))
            for epub_path in epub_files:
                filename = os.path.basename(epub_path)
                publication_date = parse_date_from_filename(filename, magazine_type)
                if publication_date:  # 只处理能解析出日期的文件
                    # 对重复日期进行去重，保留第一个找到的文件
                    if publication_date not in seen_dates:
                        json_filename = f"{config['name']}_{publication_date.replace('-', '')}.json"
                        json_path = os.path.join(magazine_output_dir, json_filename)
                        epub_info.append({
                            'epub_path': epub_path,
                            'json_path': json_path,
                            'publication_date': publication_date,
                            'filename': filename
                        })
                        seen_dates[publication_date] = True
    
    # 获取已存在的JSON文件
    existing_json_files = []
    if os.path.exists(magazine_output_dir):
        existing_json_files = glob.glob(os.path.join(magazine_output_dir, "*.json"))
    
    return {
        'config': config,
        'epub_info': epub_info,
        'existing_json_files': existing_json_files,
        'magazine_output_dir': magazine_output_dir
    }

def analyze_magazine_status(magazine_type, base_output_dir="摘要汇总"):
    """分析期刊的处理状态"""
    try:
        paths = get_magazine_paths(magazine_type, base_output_dir)
        
        # 计算期待的JSON文件路径集合
        expected_json_paths = {info['json_path'] for info in paths['epub_info']}
        # 已存在的JSON文件路径集合
        existing_json_set = set(paths['existing_json_files'])
        
        # 找到匹配的JSON文件（既期待又存在的）
        matched_json = expected_json_paths & existing_json_set
        # 需要处理的（期待但不存在的）
        needs_processing = expected_json_paths - existing_json_set
        
        return {
            "name": paths['config']['title'],
            "key": magazine_type,
            "epub_count": len(paths['epub_info']),  # 有效期数（唯一日期数量）
            "summary_count": len(matched_json),     # 已生成的摘要数量
            "pending_count": len(needs_processing), # 待处理数量
            "status": "✅ 已完成" if len(needs_processing) == 0 else f"📝 待处理{len(needs_processing)}篇"
        }
    except Exception as e:
        print(f"分析{magazine_type}时出错: {e}")
        return {
            "name": MAGAZINE_CONFIG.get(magazine_type, {}).get('title', '未知'),
            "key": magazine_type,
            "epub_count": 0,
            "summary_count": 0,
            "pending_count": 0,
            "status": "❌ 分析失败"
        }

def analyze_all_magazines(base_output_dir="摘要汇总"):
    """分析所有期刊的状态"""
    magazines_info = []
    
    for magazine_type in MAGAZINE_CONFIG.keys():
        info = analyze_magazine_status(magazine_type, base_output_dir)
        magazines_info.append(info)
    
    return magazines_info

def get_display_width(text):
    """计算文本在终端中的显示宽度（中文字符占2个宽度，英文占1个）"""
    width = 0
    for char in text:
        if ord(char) > 127:  # 中文字符
            width += 2
        else:  # 英文字符、数字、符号
            width += 1
    return width

def pad_text_to_width(text, target_width):
    """将文本填充到指定显示宽度（考虑中文字符）"""
    current_width = get_display_width(text)
    if current_width >= target_width:
        return text
    padding = target_width - current_width
    return text + " " * padding

def display_magazine_table(magazines_info):
    """以表格形式显示期刊信息"""
    # 定义列宽（按显示字符计算）
    col_widths = [4, 12, 8, 10, 8, 14]  # 编号、期刊名称、有效期数、已生成摘要、待处理、状态
    
    # 计算表格总宽度：列宽 + 分隔符 + 边距
    # 2(左边距) + 列宽总和 + 5个分隔符(每个3字符:" | ")
    total_width = 2 + sum(col_widths) + (len(col_widths) - 1) * 3
    
    print("\n" + "="*total_width)
    print("📊 期刊文件和摘要统计表")
    print("="*total_width)
    
    # 打印表头
    header_parts = ["编号", "期刊名称", "有效期数", "已生成摘要", "待处理", "状态"]
    header_line = "  "
    for i, part in enumerate(header_parts):
        padded_part = pad_text_to_width(part, col_widths[i])
        header_line += padded_part
        if i < len(header_parts) - 1:
            header_line += " | "
    print(header_line)
    
    # 分隔线
    separator = "--"
    for i in range(len(header_parts)):
        separator += "-" * col_widths[i]
        if i < len(header_parts) - 1:
            separator += "-+-"
    print(separator)
    
    total_epub = 0
    total_summary = 0
    total_pending = 0
    
    for idx, info in enumerate(magazines_info, 1):
        name = info['name']
        epub_count = info['epub_count']
        summary_count = info['summary_count']
        pending_count = info['pending_count']
        
        status = "✅ 已完成" if pending_count == 0 else f"📝 待处理{pending_count}篇"
        
        # 构造每一行，确保对齐
        line = "  "
        line += pad_text_to_width(str(idx), col_widths[0]) + " | "
        line += pad_text_to_width(name, col_widths[1]) + " | "
        line += pad_text_to_width(str(epub_count), col_widths[2]) + " | "
        line += pad_text_to_width(str(summary_count), col_widths[3]) + " | "
        line += pad_text_to_width(str(pending_count), col_widths[4]) + " | "
        line += pad_text_to_width(status, col_widths[5])
        
        print(line)
        
        total_epub += epub_count
        total_summary += summary_count
        total_pending += pending_count
    
    # 分隔线
    print(separator)
    
    # 合计行
    total_line = "  "
    total_line += pad_text_to_width("合计", col_widths[0]) + " | "
    total_line += pad_text_to_width("", col_widths[1]) + " | "  # 期刊名称列留空
    total_line += pad_text_to_width(str(total_epub), col_widths[2]) + " | "
    total_line += pad_text_to_width(str(total_summary), col_widths[3]) + " | "
    total_line += pad_text_to_width(str(total_pending), col_widths[4]) + " | "
    total_line += pad_text_to_width("", col_widths[5])  # 状态列留空
    print(total_line)
    
    print("="*total_width)
    
    return magazines_info