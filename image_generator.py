#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import base64
import time
import sys
import requests
import argparse
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from prompts import IMAGE_STYLE_PROMPT, IMAGE_SIZE, IMAGE_QUALITY, IMAGE_MODERATION, IMAGE_BACKGROUND

# 加载环境变量
load_dotenv()

# 环境变量配置
required_vars = [
    "AIHUBMIX_API_KEY",
    "AIHUBMIX_BASE_URL",
    "AIHUBMIX_IMAGE_GENERATION_MODEL"
]

# 检查必要环境变量
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    print(f"错误: 缺少环境变量: {', '.join(missing_vars)}")
    print("请创建 .env 文件并设置这些变量")
    sys.exit(1)

# 初始化AIHUBMIX客户端
aihubmix = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL")
)

# 初始化ARK客户端（可选）
ark_api_key = os.getenv("ARK_API_KEY")
ark_base_url = os.getenv("ARK_BASE_URL")
if ark_api_key and ark_base_url:
    ark_client = OpenAI(
        api_key=ark_api_key,
        base_url=ark_base_url
    )
    print("ARK图像生成服务已初始化")
else:
    ark_client = None
    print("ARK环境变量未配置，仅使用AIHUBMIX服务")

# 图像生成模型定义
IMAGE_MODELS = {
    "GPT-Image": "aihubmix",
    "Seedream": "ark"
}

def validate_image_model(image_model):
    """
    验证图像模型的可用性。
    
    Args:
        image_model (str): 图像模型名称
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if image_model not in IMAGE_MODELS:
        return False, f"不支持的图像模型 '{image_model}'，支持的模型: {', '.join(IMAGE_MODELS.keys())}"
    elif image_model == "Seedream" and not ark_client:
        return False, "Seedream模型需要配置ARK环境变量"
    return True, ""

def generate_image(prompt, output_dir="images", filename=None, image_model="GPT-Image", count=1):
    """
    生成图片并保存到指定目录
    
    Args:
        prompt (str): 图片描述文本
        output_dir (str): 输出目录
        filename (str): 文件名（不包含扩展名），如果为None则自动生成
        image_model (str): 图像生成模型
        count (int): 生成图片的数量，默认为1
        
    Returns:
        list: 保存的文件路径列表，如果失败返回空列表
    """
    
    if not prompt:
        print("错误: 图片描述文本不能为空")
        return []
        
    # 验证图像模型
    is_valid, error_message = validate_image_model(image_model)
    if not is_valid:
        print(error_message)
        return []
        
    # 验证数量参数
    if count < 1 or count > 10:
        print("错误: 图片数量必须在1-10之间")
        return []
        
    print(f"正在使用 {image_model} 生成 {count} 张图片...")
    
    # 确定使用的服务
    service = IMAGE_MODELS.get(image_model, "aihubmix")
    
    try:
        # API调用
        if service == "aihubmix":
            response = aihubmix.images.generate(
                model=os.getenv("AIHUBMIX_IMAGE_GENERATION_MODEL"),
                prompt=f"{prompt}{IMAGE_STYLE_PROMPT}",
                n=count,
                size=IMAGE_SIZE,
                quality=IMAGE_QUALITY,
                moderation=IMAGE_MODERATION,
                background=IMAGE_BACKGROUND
            )
        elif service == "ark":
            if not ark_client:
                print("错误: ARK客户端未初始化，请检查环境变量配置")
                return []
            # ARK服务目前只支持单张图片生成，需要循环调用
            if count > 1:
                print("注意: ARK服务当前只支持单张图片生成，将进行多次调用")
            response_data = []
            for i in range(count):
                single_response = ark_client.images.generate(
                    model=os.getenv("ARK_SeeDream_MODEL"),
                    prompt=f"{prompt}{IMAGE_STYLE_PROMPT}",
                    size=IMAGE_SIZE,
                    response_format="url"
                )
                if single_response.data:
                    response_data.extend(single_response.data)
            # 创建一个模拟的response对象
            class MockResponse:
                def __init__(self, data):
                    self.data = data
            response = MockResponse(response_data)
        else:
            print(f"错误: 未知的图像生成服务: {service}")
            return []
        
        if not response.data:
            print("错误: 未收到有效的图片数据")
            return []
        
        # 准备保存路径
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存所有生成的图片
        saved_files = []
        timestamp = datetime.now().strftime("%m%d_%H%M")
        
        for i, image_data in enumerate(response.data):
            # 生成文件名
            if filename is None:
                if count == 1:
                    current_filename = f"generated_image_{timestamp}"
                else:
                    current_filename = f"generated_image_{timestamp}_{i+1}"
            else:
                if count == 1:
                    current_filename = f"{filename}_{timestamp}"
                else:
                    current_filename = f"{filename}_{timestamp}_{i+1}"
            
            file_name = f"{current_filename}.png"
            file_path = os.path.join(output_dir, file_name)
            
            # 如果文件已存在，添加秒数
            if os.path.exists(file_path):
                seconds = datetime.now().strftime("%S")
                file_name = f"{current_filename}_{seconds}.png"
                file_path = os.path.join(output_dir, file_name)
            
            # 保存图片
            try:
                if service == "aihubmix":
                    image_bytes = base64.b64decode(image_data.b64_json)
                    with open(file_path, "wb") as f:
                        f.write(image_bytes)
                else:  # service == "ark"
                    image_url = image_data.url
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        with open(file_path, "wb") as f:
                            f.write(img_response.content)
                    else:
                        print(f"图片下载失败: HTTP {img_response.status_code}")
                        continue
                
                saved_files.append(file_path)
                print(f"图片已保存: {file_path} (使用 {image_model})")
                
            except Exception as e:
                print(f"保存图片 {i+1} 时出错: {e}")
                continue
        
        return saved_files
        
    except Exception as e:
        print(f"图片生成失败: {e}")
        return []

def generate_batch_images(prompts, output_dir="images", image_model="GPT-Image"):
    """
    批量生成图片
    
    Args:
        prompts (list): 图片描述文本列表
        output_dir (str): 输出目录
        image_model (str): 图像生成模型
        
    Returns:
        list: 成功生成的文件路径列表
    """
    successful_files = []
    
    for i, prompt in enumerate(prompts):
        print(f"\n[{i+1}/{len(prompts)}] 正在处理: {prompt[:50]}...")
        filename = f"batch_image_{i+1}"
        file_paths = generate_image(prompt, output_dir, filename, image_model)
        if file_paths:
            successful_files.extend(file_paths)
        else:
            print(f"  生成失败，跳过")
    
    return successful_files

def read_prompts_from_file(file_path):
    """
    从文件中读取图片描述文本（每行一个）
    
    Args:
        file_path (str): 文件路径
        
    Returns:
        list: 图片描述文本列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            prompts = [line.strip() for line in f if line.strip()]
        return prompts
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return []

def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(description="图片生成工具")
    
    # 添加基本参数
    parser.add_argument(
        "prompt", 
        nargs="?",
        help="图片描述文本"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="images",
        help="输出目录 (默认: images)"
    )
    
    parser.add_argument(
        "-f", "--filename",
        help="输出文件名（不包含扩展名）"
    )
    
    parser.add_argument(
        "-m", "--model",
        choices=list(IMAGE_MODELS.keys()),
        default="GPT-Image",
        help="图像生成模型 (默认: GPT-Image)"
    )
    
    # 批量处理参数
    parser.add_argument(
        "--batch",
        help="从文件中读取多个描述文本进行批量生成（每行一个）"
    )
    
    # 交互模式
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="交互模式，可以连续输入多个描述文本"
    )
    
    args = parser.parse_args()
    
    # 批量处理模式
    if args.batch:
        prompts = read_prompts_from_file(args.batch)
        if not prompts:
            print("未能从文件中读取到有效的描述文本")
            return
        
        print(f"从文件中读取到 {len(prompts)} 个描述文本")
        successful_files = generate_batch_images(prompts, args.output, args.model)
        print(f"\n批量生成完成! 成功生成 {len(successful_files)} 张图片")
        for file_path in successful_files:
            print(f"  - {file_path}")
        return
    
    # 交互模式
    if args.interactive:
        print("进入交互模式，输入 'quit' 或 'exit' 退出")
        while True:
            try:
                prompt = input("\n请输入图片描述: ").strip()
                if prompt.lower() in ['quit', 'exit', 'q']:
                    print("退出交互模式")
                    break
                
                if not prompt:
                    print("描述文本不能为空")
                    continue
                
                file_paths = generate_image(prompt, args.output, args.filename, args.model)
                if file_paths:
                    print(f"✅ 生成成功:")
                    for path in file_paths:
                        print(f"  - {path}")
                else:
                    print("❌ 生成失败")
                    
            except KeyboardInterrupt:
                print("\n\n退出交互模式")
                break
        return
    
    # 单次生成模式
    if args.prompt:
        file_paths = generate_image(args.prompt, args.output, args.filename, args.model)
        if file_paths:
            print(f"\n✅ 图片生成成功:")
            for path in file_paths:
                print(f"  - {path}")
        else:
            print("\n❌ 图片生成失败")
    else:
        # 如果没有提供参数，显示帮助信息
        parser.print_help()
        print("\n使用示例:")
        print("  python image_generator.py \"一只可爱的小猫在花园里玩耍\"")
        print("  python image_generator.py \"科技感的城市夜景\" -o my_images -f city_night")
        print("  python image_generator.py --batch prompts.txt")
        print("  python image_generator.py --interactive")

if __name__ == "__main__":
    
    # 示例prompt，可以根据需要修改
    prompt = "特朗普与他在华尔街和硅谷的密友在通过官商勾结，谋取私利。有视觉冲击的电影宣传海报质感，超高清展示，细节清晰，没有文字。"
    
    # 生成图片
    file_paths = generate_image(
        prompt=prompt, 
        output_dir="images", 
        filename="trump",
        image_model="GPT-Image",
        count=1
    )
    
    if file_paths:
        print(f"\n✅ 图片生成成功:")
        for path in file_paths:
            print(f"  - {path}")
    else:
        print("\n❌ 图片生成失败")