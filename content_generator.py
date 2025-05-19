import os
import json
import base64
from dotenv import load_dotenv
from datetime import datetime
import time
import re
import json_repair
from openai import OpenAI
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml.ns import qn
# 导入提示词
from prompts import (
    SYSTEM_PROMPT, IMAGE_STYLE_PROMPT, IMAGE_SIZE, IMAGE_QUALITY, IMAGE_MODERATION, IMAGE_BACKGROUND
)

# 加载.env文件中的环境变量
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
OPENROUTER_CLAUDE_MODEL = os.getenv("OPENROUTER_Claude_3.7_Sonnet")
OPENROUTER_GEMINI_MODEL = os.getenv("OPENROUTER_Gemini_2.5_Pro")
OPENROUTER_DS_R1_MODEL = os.getenv("OPENROUTER_DeepSeek_R1")
AIHUBMIX_API_KEY = os.getenv("AIHUBMIX_API_KEY")
AIHUBMIX_BASE_URL = os.getenv("AIHUBMIX_BASE_URL")
AIHUBMIX_IMAGE_GEN_MODEL = os.getenv("AIHUBMIX_IMAGE_GENERATION_MODEL")

# 检查必要的环境变量是否设置
required_env_vars = [
    "OPENROUTER_API_KEY", "OPENROUTER_BASE_URL", "OPENROUTER_Claude_3.7_Sonnet",
    "AIHUBMIX_API_KEY", "AIHUBMIX_BASE_URL", "AIHUBMIX_IMAGE_GENERATION_MODEL"
]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"缺少环境变量: {', '.join(missing_vars)}")

# 初始化 OpenAI 客户端
openrouter = OpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL)
aihubmix = OpenAI(api_key=AIHUBMIX_API_KEY, base_url=AIHUBMIX_BASE_URL)

def read_input_file(file_path):
    """读取输入文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def generate_content_with_title(content, output_dir=None, model=OPENROUTER_GEMINI_MODEL, reqs="", temperature=0.7):

    try:
        # 如果有额外要求，添加到提示词中
        user_content = content
        if reqs:
            user_content = f"{content}\n\n额外要求：{reqs}"
            
        print("\n开始API调用...")
        # API调用获取内容，直接指定返回JSON格式
        response = openrouter.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            max_tokens=6000,
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        
        # 获取响应内容
        response_content = response.choices[0].message.content.strip()
        print(f"\nAPI返回内容长度: {len(response_content)} 字符")
        
        try:
            # 尝试直接解析JSON
            try:
                result = json.loads(response_content)
            except json.JSONDecodeError:
                print("检测到JSON格式问题，尝试修复...")
                # 使用json_repair修复JSON
                result = json.loads(json_repair.repair_json(response_content))
            
            print("成功解析JSON响应")
            
            # 确保输出目录存在
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                json_path = os.path.join(output_dir, "content.json")
            else:
                json_path = "content.json"
                
            # 保存解析后的JSON，确保使用UTF-8编码
            with open(json_path, 'w', encoding='utf-8', errors='replace') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            # 验证保存的文件
            with open(json_path, 'r', encoding='utf-8') as f:
                saved_content = f.read()
                print(f"已保存JSON文件大小: {len(saved_content)} 字节")
                
            print(f"JSON内容已保存到: {json_path}")
            
            return result
            
        except Exception as e:
            print(f"JSON解析失败: {e}")
            return {
                "error": "JSON解析失败",
                "message": str(e),
                "raw_response": response_content
            }
            
    except Exception as e:
        print(f"\n生成内容错误: {e}")
        return {"error": str(e)}

def generate_and_save_image(paragraph, output_dir, index):
    """基于段落生成图片并保存到指定目录"""
    try:
        if not paragraph:
            print("警告: 段落内容为空，无法生成图片")
            return None
            
        print(f"\n正在生成图片，索引: {index}")
        print(f"提示词长度: {len(paragraph)} 字符")
        
        # 生成图片
        try:
            response = aihubmix.images.generate(
                model=AIHUBMIX_IMAGE_GEN_MODEL,
                prompt=f"{paragraph}{IMAGE_STYLE_PROMPT}",
                n=1,
                size=IMAGE_SIZE,
                quality=IMAGE_QUALITY,
                moderation=IMAGE_MODERATION,
                background=IMAGE_BACKGROUND
            )
            print("API 调用成功")
        except Exception as e:
            print(f"API 调用失败: {e}")
            return None
        
        if not response or not hasattr(response, 'data') or not response.data:
            print("错误: 未收到有效的图片数据")
            if hasattr(response, 'error'):
                print(f"API错误: {response.error}")
            return None
            
        # 保存图片
        os.makedirs(output_dir, exist_ok=True)
        try:
            image_data = response.data[0]
            if not hasattr(image_data, 'b64_json') or not image_data.b64_json:
                print("错误: 图片数据中缺少 base64 编码")
                return None
                
            image_bytes = base64.b64decode(image_data.b64_json)
            file_name = f"image_{index}.png"
            
            # 避免文件名冲突
            if os.path.exists(os.path.join(output_dir, file_name)):
                file_name = f"image_{index}_{int(time.time())}.png"
                
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, "wb") as f:
                f.write(image_bytes)
            
            print(f"图片已保存: {file_path}")
            return file_name
            
        except Exception as save_error:
            print(f"保存图片时出错: {save_error}")
            return None
        
    except Exception as e:
        print(f"图片生成过程中发生错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_docx_report_native(content_json, images, output_dir, image_mode=1):
    """创建 Word 文档报告，包含所有标题方案
    
    Args:
        content_json: 包含文章内容的JSON对象
        images: 图片文件名列表
        output_dir: 输出目录
        image_mode: 图片模式，1=每段一张图，2=整篇文章一张图，3=无图
    """
    try:
        doc = Document()
        
        # 设置默认字体和样式 - 使用更通用的字体设置
        style = doc.styles['Normal']
        style.font.name = 'Times New Roman'  # 英文字体
        if not style.element.rPr:
            style.element.get_or_add_rPr()
        style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')  # 中文字体改为宋体
        style.font.size = Pt(12)
        style.paragraph_format.space_after = Pt(8)
        style.font.color.rgb = RGBColor(0, 0, 0)  # 确保文字颜色为黑色
        
        # 辅助函数：设置文本运行的格式
        def set_run_style(run, size=12, bold=False):
            run.font.name = 'Times New Roman'
            if not run._element.rPr:
                run._element.get_or_add_rPr()
            run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
            run.font.size = Pt(size)
            run.bold = bold
            run.font.color.rgb = RGBColor(0, 0, 0)
        
        # 添加文档标题
        heading = doc.add_heading(level=0)
        heading_run = heading.add_run("文章标题方案生成报告")
        set_run_style(heading_run, size=20, bold=True)
        doc.add_paragraph()  # 添加空行
        
        # 创建标题比较表格
        table = doc.add_table(rows=4, cols=2)
        table.style = 'Table Grid'
        
        # 设置表格内容
        headers = ["标题编号", "标题内容"]
        for i, header in enumerate(headers):
            cell = table.rows[0].cells[i]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(header)
            set_run_style(run, bold=True)
            
        # 添加标题行
        for i in range(1, 4):
            title_key = f"title_{i}"
            row = table.rows[i]
            
            # 标题编号
            cell = row.cells[0]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(f"标题{['一', '二', '三'][i-1]}")
            set_run_style(run)
            
            # 标题内容
            cell = row.cells[1]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(content_json.get(title_key, "自媒体文章"))
            set_run_style(run)
        
        # 添加空行
        doc.add_paragraph()
        doc.add_paragraph()
        
        # 添加文章内容标题
        content_heading = doc.add_heading(level=0)
        content_heading_run = content_heading.add_run("文章内容")
        set_run_style(content_heading_run, size=18, bold=True)
        doc.add_paragraph()  # 添加空行
        
        # 添加文章内容
        paragraphs = content_json.get("paragraphs", [])
        
        # 检查是否有整篇文章的配图（索引为0的图片）
        if images and len(images) > 0 and images[0] and os.path.exists(os.path.join(output_dir, images[0])):
            try:
                image_path = os.path.join(output_dir, images[0])
                # 在文章内容标题后添加整篇文章的配图
                pic_paragraph = doc.add_paragraph()
                pic_paragraph.alignment = 1  # 居中对齐
                pic_run = pic_paragraph.add_run()
                pic_run.add_picture(image_path, width=Inches(5.0))
                # 图片后添加空行作为分隔
                doc.add_paragraph()
                # 从段落图片列表中移除整篇文章的配图，避免重复添加
                images[0] = None
            except Exception as e:
                print(f"添加整篇文章配图时出错: {e}")
        
        for i, (p, image_filename) in enumerate(zip(paragraphs, images)):
            subtitle = p.get("subtitle", "")
            content = p.get("content", "")
            
            # 添加子标题
            if subtitle:
                subheading = doc.add_heading(level=1)
                subheading_run = subheading.add_run(subtitle)
                set_run_style(subheading_run, size=14, bold=True)
            
            # 添加段落内容
            if content:
                para = doc.add_paragraph()
                text_run = para.add_run(content)
                set_run_style(text_run)
            else:
                para = doc.add_paragraph()
                text_run = para.add_run("[内容缺失]")
                set_run_style(text_run)
                print(f"警告: 第{i+1}段内容为空")
            
            # 使用分隔符区隔文本和图片，避免格式问题
            separator = doc.add_paragraph()
            separator_run = separator.add_run("\u3000")
            set_run_style(separator_run)  # 增加一个空格分隔符
            
            # 添加图片
            if image_filename:
                image_path = os.path.join(output_dir, image_filename)
                try:
                    if os.path.exists(image_path):
                        # 创建专门的段落来容纳图片
                        pic_paragraph = doc.add_paragraph()
                        pic_paragraph.alignment = 1  # 居中对齐
                        
                        # 添加图片
                        pic_run = pic_paragraph.add_run()
                        pic_run.add_picture(image_path, width=Inches(5.0))
                        
                        # 图片后添加空行作为分隔
                        after_pic = doc.add_paragraph()
                        after_run = after_pic.add_run("\u3000")
                        set_run_style(after_run)
                    else:
                        print(f"警告: 图片文件不存在: {image_path}")
                except Exception as e:
                    print(f"图片插入错误: {e}")
        
        # 保存文档
        doc_path = os.path.join(output_dir, "report.docx")
        try:
            doc.save(doc_path)
            print(f"DOCX报告已成功生成: {doc_path}")
        except Exception as e:
            print(f"文档保存失败: {e}")
            raise
            
    except Exception as e:
        print(f"创建 DOCX 报告时发生严重错误: {e}")
        raise

def main(image_mode=1, model=OPENROUTER_GEMINI_MODEL, reqs="", temperature=0.7):
    # 验证temperature参数
    if not (0 <= temperature <= 1):
        raise ValueError("temperature参数必须在0到1之间")

    # 读取输入并验证
    content = read_input_file("input.txt")
    if not content:
        print("无法读取输入文件 input.txt，程序终止")
        return
    
    if reqs:
        print("检测到额外要求，将整合到提示词中")
    
    # 创建输出目录
    timestamp = datetime.now().strftime("%m%d_%H%M")
    output_dir = f"content_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成内容
    print(f"正在生成文章内容，使用模型：{model}...")
    result = generate_content_with_title(content, output_dir, model=model, reqs=reqs, temperature=temperature)
    if not isinstance(result, dict) or "paragraphs" not in result or not isinstance(result["paragraphs"], list):
        print("错误: 内容生成返回无效结果")
        return
    
    # 使用标题创建更友好的目录名
    title = result.get("title_1", "未命名文章")
    title_dir = f"{re.sub(r'[\s\-_.,:\;"\'\[\]{{}}()\\/*&^%$#@!~`|<>?]+', '', title)}_{timestamp}"
    if title_dir != output_dir and not os.path.exists(title_dir):
        os.rename(output_dir, title_dir)
        output_dir = title_dir
    
    # 生成配图
    paragraphs = result["paragraphs"]
    images_for_docx = [None] * len(paragraphs)
    successfully_generated_images_count = 0
    
    if image_mode == 1:  # 每章节/段落一张图
        print(f"正在生成段落配图...")
        for i, p in enumerate(paragraphs):
            if not p.get("content"): 
                continue

            print(f"  图片 {i+1}/{len(paragraphs)} 正在生成...")
            print(f"  段落内容: {p.get('content', '')[:100]}...")
            image_filename = generate_and_save_image(p.get("content", ""), output_dir, i + 1)
            if image_filename:
                images_for_docx[i] = image_filename
                successfully_generated_images_count += 1
                print("  √ 生成成功")
            else:
                print("  × 生成失败")
    
    elif image_mode == 2:  # 整篇文章一张图
        print(f"正在生成文章整体配图...")
        # 合并所有文本内容，限制长度以避免提示词过长
        all_content = "\n".join([p.get("subtitle", "") + ": " + p.get("content", "")[:100] for p in paragraphs if p.get("content")])
        all_content = all_content[:500]  # 限制长度
        
        print(f"  生成文章配图...")
        print(f"  合并内容预览: {all_content[:200]}...")
        image_filename = generate_and_save_image(all_content, output_dir, 0)  # 使用索引0表示整篇文章
        if image_filename:
            # 将图片放在第一段
            if len(images_for_docx) > 0:
                images_for_docx[0] = image_filename
            successfully_generated_images_count = 1
            print("  √ 生成成功")
        else:
            print("  × 生成失败")
    
    else:  # 模式3：不生成图片
        print("已跳过图片生成")
    
    # 传递 image_mode 参数给 create_docx_report_native 函数
    create_docx_report_native(result, images_for_docx, output_dir, image_mode=image_mode)
    print(f"\n生成完成! 保存至: {output_dir}")
    for i in range(1, 4):
        print(f"  标题{i}: {result.get(f'title_{i}', '无标题')}")
    print(f"  文件: report.docx, content.json 和 {successfully_generated_images_count} 张配图")

if __name__ == "__main__":
    """
    主程序入口
    使用示例：
        1. 为每个章节生成配图: main(image_mode=1)
        2. 为整篇文章生成一张配图: main(image_mode=2)
        3. 不生成任何配图: main(image_mode=3)
        
        使用不同模型:
        - 使用Claude 3.7 Sonnet: model=OPENROUTER_CLAUDE_MODEL
        - 使用DeepSeek R1: model=OPENROUTER_DS_R1_MODEL
        - 使用Gemini 2.5 Pro: model=OPENROUTER_GEMINI_MODEL
        
        使用额外要求:
        - 在reqs参数中传入字符串，例如：
          main(reqs="文章风格要正式，使用专业术语")
        
        控制生成随机性:
        - temperature: 控制生成文本的随机性，范围0-1，值越大随机性越强，默认0.7
          例如: main(temperature=0.5)  # 更确定性的输出
               main(temperature=0.9)  # 更有创意的输出
    """
    
    main(image_mode=3, model=OPENROUTER_DS_R1_MODEL, reqs="文章风格生动活泼，像好友聊天", temperature=0.7)