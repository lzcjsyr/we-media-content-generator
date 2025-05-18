#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
from datetime import datetime
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

# 从主模块导入函数
from content_generator import (
    read_input_file, 
    generate_content_with_title
)

# 从content_generator导入模型常量
from content_generator import (
    OPENROUTER_GEMINI_MODEL,
    OPENROUTER_CLAUDE_MODEL,
    OPENROUTER_DS_R1_MODEL
)

def set_heading_font(heading):
    """Set font for heading to Times New Roman/宋体"""
    if heading.runs:
        run = heading.runs[0]
        run.font.name = 'Times New Roman'
        if not run._element.rPr:
            run._element.get_or_add_rPr()
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

def create_comparison_report(results, output_dir):
    """创建包含所有模型生成内容的比较报告"""
    doc = Document()
    
    # 设置默认字体为宋体
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'  # 英文字体
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')  # 中文字体
    style.font.size = Pt(12)
    
    # 添加文档标题
    title = doc.add_heading('模型比较报告', level=0)
    if title.runs:
        title_run = title.runs[0]
        title_run.font.name = 'Times New Roman'
        if not title_run._element.rPr:
            title_run._element.get_or_add_rPr()
        title_run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        title_run.font.size = Pt(18)
    
    # 添加说明
    doc.add_paragraph('本报告对比了不同模型生成的内容效果，包括标题和段落内容。')
    doc.add_paragraph(f'生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    doc.add_paragraph()
    
    # 1. 标题比较部分
    heading = doc.add_heading('一、标题比较', level=1)
    set_heading_font(heading)
    
    # 创建标题比较表格
    title_table = doc.add_table(rows=4, cols=4)
    title_table.style = 'Table Grid'
    
    # 表头
    title_table.cell(0, 0).text = "标题方案"
    title_table.cell(0, 1).text = "Gemini"
    title_table.cell(0, 2).text = "Claude"
    title_table.cell(0, 3).text = "DeepSeek"
    
    # 填充标题比较内容
    for i in range(1, 4):
        key = f"title_{i}"
        title_table.cell(i, 0).text = f"标题 {i}"
        title_table.cell(i, 1).text = results["gemini"].get(key, "未生成")
        title_table.cell(i, 2).text = results["claude"].get(key, "未生成")
        title_table.cell(i, 3).text = results["deepseek"].get(key, "未生成")
    
    doc.add_paragraph()
    
    # 2. 段落内容比较
    heading = doc.add_heading('二、正文内容比较', level=1)
    set_heading_font(heading)
    
    # 获取每个模型生成的段落数量
    gemini_paragraphs = results["gemini"].get("paragraphs", [])
    claude_paragraphs = results["claude"].get("paragraphs", [])
    deepseek_paragraphs = results["deepseek"].get("paragraphs", [])
    
    # 计算最大段落数
    max_paragraphs = max(
        len(gemini_paragraphs),
        len(claude_paragraphs),
        len(deepseek_paragraphs)
    )
    
    # 遍历所有段落，进行比较
    for i in range(max_paragraphs):
        section_heading = doc.add_heading(f'段落 {i+1}', level=2)
        set_heading_font(section_heading)
        
        # 小标题比较
        heading = doc.add_heading('小标题比较:', level=3)
        set_heading_font(heading)
        subtitle_table = doc.add_table(rows=2, cols=3)
        subtitle_table.style = 'Table Grid'
        
        # 表头
        subtitle_table.cell(0, 0).text = "Gemini"
        subtitle_table.cell(0, 1).text = "Claude"
        subtitle_table.cell(0, 2).text = "DeepSeek"
        
        # 填充小标题
        subtitle_table.cell(1, 0).text = gemini_paragraphs[i].get("subtitle", "无小标题") if i < len(gemini_paragraphs) else "无内容"
        subtitle_table.cell(1, 1).text = claude_paragraphs[i].get("subtitle", "无小标题") if i < len(claude_paragraphs) else "无内容"
        subtitle_table.cell(1, 2).text = deepseek_paragraphs[i].get("subtitle", "无小标题") if i < len(deepseek_paragraphs) else "无内容"
        
        doc.add_paragraph()
        
        # 段落内容比较
        heading = doc.add_heading('段落内容比较:', level=3)
        set_heading_font(heading)
        
        # Gemini 内容
        heading = doc.add_heading('Gemini:', level=4)
        set_heading_font(heading)
        gemini_content = gemini_paragraphs[i].get("content", "无内容") if i < len(gemini_paragraphs) else "无内容"
        doc.add_paragraph(gemini_content)
        
        # Claude 内容
        heading = doc.add_heading('Claude:', level=4)
        set_heading_font(heading)
        claude_content = claude_paragraphs[i].get("content", "无内容") if i < len(claude_paragraphs) else "无内容"
        doc.add_paragraph(claude_content)
        
        # DeepSeek 内容
        heading = doc.add_heading('DeepSeek:', level=4)
        set_heading_font(heading)
        deepseek_content = deepseek_paragraphs[i].get("content", "无内容") if i < len(deepseek_paragraphs) else "无内容"
        doc.add_paragraph(deepseek_content)
        
        doc.add_paragraph()
    
    # 保存文档
    doc_path = os.path.join(output_dir, "model_comparison.docx")
    doc.save(doc_path)
    print(f"模型比较报告已保存: {doc_path}")
    return doc_path

def main():
    # 读取输入
    content = read_input_file("input.txt")
    if not content:
        print("无法读取输入文件 input.txt，程序终止")
        return
    
    # 创建输出目录
    timestamp = datetime.now().strftime("%m%d_%H%M")
    output_dir = f"comparison_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # 定义模型和友好名称的映射
    models = {
        "gemini": OPENROUTER_GEMINI_MODEL,
        "claude": OPENROUTER_CLAUDE_MODEL,
        "deepseek": OPENROUTER_DS_R1_MODEL
    }
    
    # 存储各模型的生成结果
    results = {}
    
    # 使用三个不同模型生成内容
    for model_name, model_id in models.items():
        print(f"\n正在使用 {model_name} 模型生成内容...")
        
        # 为每个模型创建单独的子目录
        model_dir = os.path.join(output_dir, model_name)
        os.makedirs(model_dir, exist_ok=True)
        
        # 生成内容
        try:
            result = generate_content_with_title(content, model_dir, model=model_id)
            results[model_name] = result
            
            # 保存JSON结果到子目录
            json_path = os.path.join(model_dir, "content.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
                
            print(f"{model_name} 模型内容已保存到 {json_path}")
            
        except Exception as e:
            print(f"{model_name} 模型生成失败: {e}")
            results[model_name] = {"title_1": f"{model_name} 生成失败", "paragraphs": []}
    
    # 创建比较报告
    if results:
        report_path = create_comparison_report(results, output_dir)
        
        # 打印结果概要
        print("\n模型比较完成!")
        print(f"比较结果已保存到目录: {output_dir}")
        print(f"比较报告: {report_path}")
        
        # 为每个模型打印标题示例
        for model_name in models.keys():
            if model_name in results:
                title = results[model_name].get("title_1", "未生成")
                print(f"{model_name} 标题示例: {title}")
    else:
        print("所有模型生成失败，无法创建比较报告")

if __name__ == "__main__":
    main()
