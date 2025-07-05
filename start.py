#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🚀 自媒体内容生成工具 - 统一启动入口

功能说明:
1. 📝 内容生成 - 根据input.txt文件生成自媒体文章内容和配图
2. 🖼️ 独立图片生成 - 根据文本描述生成图片
3. 📚 期刊摘要 - 处理期刊EPUB文件并生成摘要报告

输出目录:
- 内容生成: ../完整作品/ 文件夹
- 独立图片: ../独立图片/ 文件夹  
- 期刊摘要: 摘要汇总/ 文件夹

使用方法:
    python start.py
"""

import os
import sys
import argparse
from pathlib import Path

# 确保可以导入functions模块
try:
    from functions.content_generator import main as content_main
    from functions.image_generator import generate_image, generate_batch_images, read_prompts_from_file
    from functions.summarizer import process_magazine
    from functions.magazine_analyzer import analyze_all_magazines, display_magazine_table
    from functions.github_updater import check_github_updates, update_repo_if_needed
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    print("请确保已安装所有依赖: pip install -r functions/requirements.txt")
    sys.exit(1)

def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("🚀 自媒体内容生成工具 v2.0")
    print("=" * 60)
    print("📝 功能菜单:")
    print("  1. 内容生成 - 根据input.txt生成文章和配图")
    print("  2. 独立图片生成 - 根据文本描述生成图片")
    print("  3. 期刊摘要 - 处理期刊EPUB文件生成摘要")
    print("  4. 退出程序")
    print("=" * 60)

def check_input_file():
    """检查input.txt文件是否存在"""
    # 确保使用脚本所在目录的input.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "input.txt")
    if not os.path.exists(input_file):
        print(f"❌ 未找到 {input_file} 文件")
        print("请在当前目录创建 input.txt 文件并添加要处理的内容")
        return False
    
    # 检查文件是否为空
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    if not content:
        print(f"❌ {input_file} 文件为空")
        print("请在文件中添加要处理的内容")
        return False
    
    print(f"✅ 找到 {input_file} 文件，内容长度: {len(content)} 字符")
    return True

def create_output_directories():
    """创建输出目录"""
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)  # 期刊系列内容生成目录
    
    # 定义输出目录
    dirs = [
        os.path.join(parent_dir, "完整作品"),
        os.path.join(parent_dir, "独立图片"), 
        os.path.join(script_dir, "摘要汇总")
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"📁 确保目录存在: {dir_path}")

def content_generation():
    """内容生成工作流"""
    print("\n" + "="*50)
    print("📝 内容生成模式")
    print("="*50)
    
    if not check_input_file():
        return

    print("\n🎨 内容生成模式选择:")
    print("  1. 默认模式 (推荐) - 一键生成文章和高质量封面图")
    print("  2. 自定义模式 - 自定义所有文本和图片参数")

    try:
        generation_mode = int(input("\n请选择生成模式 (1-2): "))
        if generation_mode not in [1, 2]:
            print("❌ 无效选择，使用默认模式1")
            generation_mode = 1
    except ValueError:
        print("❌ 输入无效，使用默认模式1")
        generation_mode = 1

    # --- 参数定义 ---
    import os
    models = {
        1: (os.getenv("OPENROUTER_Claude_3.7_Sonnet", "anthropic/claude-3.5-sonnet"), "Claude 3.7 Sonnet"),
        2: (os.getenv("OPENROUTER_Gemini_2.5_Pro", "google/gemini-2.0-flash-exp"), "Gemini 2.5 Pro"),
        3: (os.getenv("OPENROUTER_DeepSeek_R1", "deepseek/deepseek-r1"), "DeepSeek R1")
    }
    
    # 设置默认模式的参数
    image_mode = 2
    model, model_choice_text = models[1]
    temperature = 0.7
    reqs = "文章语言自然流畅，但要通过转折、惊喜、反转等手法，让读者有阅读的欲望。同时让文章有深度，有思考，有启发。"
    image_model = "GPT-Image"
    image_style = "\n\n有视觉冲击的电影宣传海报质感，超高清展示，细节清晰，没有文字。"
    image_size = "1536x1024"
    image_quality = "high"
    image_moderation = "low"
    image_background = "auto"

    if generation_mode == 1:  # 默认模式
        print("\n✨ 已选择默认模式，将使用预设参数自动生成。")
        print("   - 文本模型: Claude 3.7 Sonnet")
        print("   - 创作风格: 平衡创作 (0.7)")
        print("   - 图片模式: 一张高质量横向封面图")

    else:  # 自定义模式
        print("\n✨ 已选择自定义模式，请配置以下参数。")
        
        # 1. 选择文本模型
        print("\n🤖 AI文本模型选择:")
        print("  1. Claude 3.7 Sonnet (推荐) - 写作质量最高")
        print("  2. Gemini 2.5 Pro - 创意度较高")
        print("  3. DeepSeek R1 - 性价比高")
        try:
            model_choice_num = int(input("\n请选择模型 (1-3): "))
            model, model_choice_text = models.get(model_choice_num, models[1])
        except ValueError:
            print("❌ 输入无效，使用默认模型Claude")
            model, model_choice_text = models[1]

        # 2. 选择创作随机性
        print("\n🎯 创作随机性设置:")
        print("  1. 保守创作 (0.3) - 稳定可靠，逻辑性强")
        print("  2. 平衡创作 (0.7) - 推荐，创意与稳定兼顾")
        print("  3. 创意创作 (0.9) - 富有创意，表达多样")
        print("  4. 自定义数值 (0-1)")
        try:
            temp_choice = int(input("\n请选择创作风格 (1-4): "))
            if temp_choice == 1: temperature = 0.3
            elif temp_choice == 2: temperature = 0.7
            elif temp_choice == 3: temperature = 0.9
            elif temp_choice == 4:
                try:
                    temperature = float(input("请输入自定义数值 (0-1): "))
                    if not 0 <= temperature <= 1:
                        print("❌ 值超出范围，使用默认值0.7")
                        temperature = 0.7
                except ValueError:
                    print("❌ 输入无效，使用默认值0.7")
                    temperature = 0.7
            else:
                print("❌ 输入无效，使用默认值0.7")
                temperature = 0.7
        except ValueError:
            print("❌ 输入无效，使用默认值0.7")
            temperature = 0.7

        # 3. 额外要求
        reqs_input = input("\n📋 额外创作要求 (可选，直接回车使用默认): ").strip()
        if reqs_input:
            reqs = reqs_input

        # 4. 图像生成模式
        print("\n🎨 图像生成模式选择:")
        print("  1. 每段配图 - 为每个段落生成配图")
        print("  2. 封面图片 - 仅为整篇文章生成一张封面图")
        print("  3. 无图模式 - 仅生成文字内容")
        try:
            image_mode = int(input("\n请选择图像模式 (1-3): "))
            if image_mode not in [1, 2, 3]:
                print("❌ 无效选择，将不生成图片")
                image_mode = 3
        except ValueError:
            print("❌ 输入无效，将不生成图片")
            image_mode = 3

        # 5. 如果需要生成图片，则进行详细配置
        if image_mode != 3:
            print("\n🎨 图像生成配置:")
            print("  1. 使用默认配置 (推荐) - GPT-Image, 横向, 低质量")
            print("  2. 自定义配置")
            try:
                img_config_choice = int(input("\n请选择图像配置 (1-2): "))
            except ValueError:
                print("❌ 输入无效，使用默认配置")
                img_config_choice = 1

            if img_config_choice == 2:
                print("\n🎨 图像生成模型选择:")
                print("  1. GPT-Image (推荐) - GPT-4o 图像生成")
                print("  2. Seedream - 豆包即梦3.0")
                try:
                    img_model_choice = int(input("\n请选择图像模型 (1-2): "))
                    image_model = "GPT-Image" if img_model_choice == 1 else "Seedream"
                except ValueError:
                    print("❌ 输入无效，使用默认模型GPT-Image")
                    image_model = "GPT-Image"
                
                print("\n🖼️ 图像尺寸选择:")
                print("  1. 1536x1024 (推荐) - 横向长图")
                print("  2. 1024x1024 - 正方形")
                print("  3. 1792x1024 - 超宽横图")
                print("  4. 1024x1792 - 竖版长图")
                size_options = {1: "1536x1024", 2: "1024x1024", 3: "1792x1024", 4: "1024x1792"}
                try:
                    size_choice = int(input("\n请选择图像尺寸 (1-4): "))
                    image_size = size_options.get(size_choice, "1536x1024")
                except ValueError:
                    print("❌ 输入无效，使用默认尺寸1536x1024")
                    image_size = "1536x1024"
                
                print("\n✨ 图像质量选择:")
                print("  1. low (推荐) - 低质量，速度快")
                print("  2. standard - 标准质量")
                print("  3. high - 高质量，速度慢")
                quality_options = {1: "low", 2: "standard", 3: "high"}
                try:
                    quality_choice = int(input("\n请选择图像质量 (1-3): "))
                    image_quality = quality_options.get(quality_choice, "low")
                except ValueError:
                    print("❌ 输入无效，使用默认质量low")
                    image_quality = "low"
                
                print("\n🛡️ 自定义图像风格 (可选):")
                print(f"  当前默认: {image_style.strip()}")
                custom_style = input("请输入自定义风格描述 (直接回车使用默认): ").strip()
                if custom_style:
                    image_style = f"\n\n{custom_style}"
    
    # --- 执行生成 ---
    print(f"\n🚀 开始生成内容...")
    image_mode_text = {1: '每段配图', 2: '封面图片', 3: '无图模式'}.get(image_mode, '未知')
    print(f"   AI模型: {model_choice_text}")
    print(f"   创作随机性: {temperature}")
    print(f"   图像模式: {image_mode_text}")
    if image_mode != 3:
        print(f"   图像模型: {image_model}")
        print(f"   图像尺寸: {image_size}")
        print(f"   图像质量: {image_quality}")
    print(f"   额外要求: {reqs}")
    
    try:
        content_main(
            image_mode=image_mode,
            model=model,
            reqs=reqs,
            temperature=temperature,
            image_model=image_model,
            image_style=image_style,
            image_size=image_size,
            image_quality=image_quality,
            image_moderation=image_moderation,
            image_background=image_background
        )
        print("\n✅ 内容生成完成!")
        print("📁 输出位置: 完整作品/ 文件夹")
    except Exception as e:
        print(f"\n❌ 内容生成失败: {e}")
        import traceback
        traceback.print_exc()


def image_generation():
    """独立图片生成工作流"""
    print("\n" + "="*50)
    print("🖼️ 独立图片生成模式")
    print("="*50)
    
    print("\n⚙️ 生成配置选择:")
    print("  1. 默认配置 (推荐) - GPT-Image模型, 低质量, 横向尺寸")
    print("  2. 自定义配置 - 可调整所有参数")
    
    try:
        config_choice = int(input("\n请选择配置方式 (1-2): "))
    except ValueError:
        print("❌ 输入无效，使用默认配置")
        config_choice = 1
    
    # 设置默认参数
    image_model = "GPT-Image"
    image_quality = "low"
    image_size = "1536x1024"
    
    if config_choice == 2:
        # 自定义配置
        print("\n🎨 图像生成模型选择:")
        print("  1. GPT-Image (推荐) - GPT-4o 图像生成")
        print("  2. Seedream - 豆包即梦3.0")
        
        try:
            model_choice = int(input("\n请选择图像模型 (1-2): "))
            image_model = "GPT-Image" if model_choice == 1 else "Seedream"
        except ValueError:
            print("❌ 输入无效，使用默认模型GPT-Image")
            image_model = "GPT-Image"
        
        print("\n✨ 图像质量选择:")
        print("  1. low - 低质量，速度快")
        print("  2. standard - 标准质量")
        print("  3. high - 高质量，速度慢")
        
        quality_options = {1: "low", 2: "standard", 3: "high"}
        
        try:
            quality_choice = int(input("\n请选择图像质量 (1-3): "))
            image_quality = quality_options.get(quality_choice, "low")
        except ValueError:
            print("❌ 输入无效，使用默认质量low")
            image_quality = "low"
        
        print("\n🖼️ 图像尺寸选择:")
        print("  1. 1536x1024 - 横向长图")
        print("  2. 1024x1024 - 正方形")
        print("  3. 1792x1024 - 超宽横图")
        print("  4. 1024x1792 - 竖版长图")
        
        size_options = {
            1: "1536x1024",
            2: "1024x1024", 
            3: "1792x1024",
            4: "1024x1792"
        }
        
        try:
            size_choice = int(input("\n请选择图像尺寸 (1-4): "))
            image_size = size_options.get(size_choice, "1536x1024")
        except ValueError:
            print("❌ 输入无效，使用默认尺寸1536x1024")
            image_size = "1536x1024"
    
    # 获取生成参数
    prompt = input("\n📝 请输入图片描述: ").strip()
    if not prompt:
        print("❌ 图片描述不能为空")
        return
    
    try:
        count = int(input("\n🔢 请输入要生成的图片数量 (1-10): "))
        if count < 1 or count > 10:
            print("❌ 数量必须在1-10之间，使用默认值1")
            count = 1
    except ValueError:
        print("❌ 输入无效，使用默认值1")
        count = 1
    
    # 自动生成文件名：模型+质量+月日时分
    from datetime import datetime
    timestamp = datetime.now().strftime("%m%d_%H%M")
    filename = f"{image_model}_{image_quality}_{timestamp}"
    
    print(f"\n🚀 正在生成{count}张图片...")
    print(f"   使用模型: {image_model}")
    print(f"   图像质量: {image_quality}")
    print(f"   图像尺寸: {image_size}")
    print(f"   图片描述: {prompt[:50]}...")
    print(f"   文件前缀: {filename}")
    
    try:
        file_paths = generate_image(
            prompt=prompt,
            output_dir=None,  # 使用默认目录
            filename=filename,
            image_model=image_model,
            count=count,
            image_size=image_size,
            image_quality=image_quality
        )
        
        if file_paths:
            print(f"\n✅ 成功生成{len(file_paths)}张图片:")
            for path in file_paths:
                print(f"  📷 {path}")
            print("📁 输出位置: 独立图片/ 文件夹")
        else:
            print("\n❌ 图片生成失败")
    except Exception as e:
        print(f"\n❌ 图片生成失败: {e}")
    
    # 询问是否继续生成
    continue_choice = input("\n是否继续生成其他图片？(y/n): ").strip().lower()
    if continue_choice in ['y', 'yes', '是']:
        image_generation()  # 递归调用自己





def summarizer_generation():
    """期刊摘要生成工作流"""
    print("\n" + "="*50)
    print("📚 期刊摘要生成模式")
    print("="*50)
    
    # 1. 检查GitHub更新
    has_updates, update_status = check_github_updates()
    
    # 2. 询问用户是否更新
    if has_updates:
        print(f"\n📡 更新状态: {update_status}")
        update_choice = input("是否更新期刊仓库？(y/n): ").strip().lower()
        
        if update_choice in ['y', 'yes', '是']:
            if not update_repo_if_needed():
                print("⚠️ 更新失败，将使用现有本地文件")
        else:
            print("📁 将使用现有本地文件")
    
    # 3. 分析本地文件和摘要数量
    print("\n🔍 正在分析本地期刊文件和摘要...")
    magazines_info = analyze_all_magazines()
    
    if not magazines_info:
        print("❌ 无法分析期刊信息，请检查期刊仓库")
        return
    
    # 4. 显示统计表格
    magazines_info = display_magazine_table(magazines_info)
    
    # 5. 用户选择要处理的期刊
    print("\n📖 请选择要处理的期刊:")
    for i, info in enumerate(magazines_info, 1):
        pending_text = f"(待处理 {info['pending_count']} 篇)" if info['pending_count'] > 0 else "(已完成)"
        print(f"  {i}. {info['name']} {pending_text}")
    print(f"  {len(magazines_info) + 1}. 处理所有待处理的期刊")
    
    try:
        choice = int(input(f"\n请选择 (1-{len(magazines_info) + 1}): "))
    except ValueError:
        print("❌ 输入无效，退出摘要生成")
        return
    
    # 6. 处理用户选择
    if 1 <= choice <= len(magazines_info):
        # 处理单个期刊
        selected_magazine = magazines_info[choice - 1]
        
        if selected_magazine["pending_count"] == 0:
            force_choice = input(f"{selected_magazine['name']} 已全部处理完成，是否强制重新处理？(y/n): ").strip().lower()
            if force_choice not in ['y', 'yes', '是']:
                print("❌ 取消处理")
                return
        
        print(f"\n🚀 开始处理 {selected_magazine['name']}...")
        print("📁 输出位置: 摘要汇总/ 文件夹")
        
        try:
            # 直接调用处理函数
            result = process_magazine(selected_magazine['key'], "摘要汇总")
            
            if result and result.get('partially_successful', False):
                # 有部分成功的处理
                if result.get('all_successful', False):
                    print(f"\n✅ {selected_magazine['name']} 处理完成!")
                else:
                    print(f"\n⚠️ {selected_magazine['name']} 部分处理完成")
                
                # 重新统计显示结果
                print("\n📊 处理后统计:")
                updated_info = analyze_all_magazines()
                if updated_info:
                    for info in updated_info:
                        if info['key'] == selected_magazine['key']:
                            print(f"  {info['name']}: 总共{info['epub_count']}篇，已处理{info['summary_count']}篇，剩余{info['pending_count']}篇")
                            break
            else:
                print(f"\n❌ {selected_magazine['name']} 处理失败")
                
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            import traceback
            print(f"详细错误: {traceback.format_exc()}")
            
    elif choice == len(magazines_info) + 1:
        # 处理所有待处理的期刊
        pending_magazines = [info for info in magazines_info if info["pending_count"] > 0]
        
        if not pending_magazines:
            print("✅ 所有期刊都已处理完成")
            return
        
        print(f"\n🚀 开始处理 {len(pending_magazines)} 个待处理期刊...")
        for magazine in pending_magazines:
            print(f"  📝 {magazine['name']}: {magazine['pending_count']} 篇待处理")
        
        confirm = input("\n确认开始批量处理？(y/n): ").strip().lower()
        if confirm in ['y', 'yes', '是']:
            try:
                fully_successful_count = 0
                partially_successful_count = 0
                failed_count = 0
                
                for i, magazine in enumerate(pending_magazines, 1):
                    print(f"\n📋 [{i}/{len(pending_magazines)}] 正在处理 {magazine['name']}...")
                    result = process_magazine(magazine['key'], "摘要汇总")
                    
                    if result and result.get('partially_successful', False):
                        if result.get('all_successful', False):
                            fully_successful_count += 1
                            print(f"✅ {magazine['name']} 处理完成")
                        else:
                            partially_successful_count += 1
                            print(f"⚠️ {magazine['name']} 部分处理完成")
                    else:
                        failed_count += 1
                        print(f"❌ {magazine['name']} 处理失败")
                
                print(f"\n📊 批量处理完成:")
                print(f"  ✅ 完全成功: {fully_successful_count} 个期刊")
                print(f"  ⚠️ 部分成功: {partially_successful_count} 个期刊")
                print(f"  ❌ 处理失败: {failed_count} 个期刊")
                
                if partially_successful_count > 0 or failed_count > 0:
                    print(f"\n💡 提示: 部分失败通常是由于LLM响应不稳定导致，建议重新运行处理失败的期刊。")
                
                # 显示最终统计
                if fully_successful_count > 0 or partially_successful_count > 0:
                    print("\n📈 最新统计:")
                    updated_info = analyze_all_magazines()
                    if updated_info:
                        display_magazine_table(updated_info)
                        
            except Exception as e:
                print(f"❌ 批量处理失败: {e}")
                import traceback
                print(f"详细错误: {traceback.format_exc()}")
        else:
            print("❌ 取消批量处理")
    else:
        print("❌ 无效选择")

def main():
    """主程序入口"""
    # 检查是否使用命令行参数
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="自媒体内容生成工具")
        parser.add_argument("--mode", choices=["content", "image", "summary"], 
                          help="直接指定工作模式")
        parser.add_argument("--prompt", help="图片生成的描述文本")
        parser.add_argument("--magazine", help="期刊类型")
        
        args = parser.parse_args()
        
        create_output_directories()
        
        if args.mode == "content":
            content_generation()
        elif args.mode == "image":
            if args.prompt:
                file_paths = generate_image(args.prompt, None)  # 使用默认目录
                if file_paths:
                    print(f"✅ 图片生成成功: {file_paths[0]}")
                else:
                    print("❌ 图片生成失败")
            else:
                image_generation()
        elif args.mode == "summary":
            summarizer_generation()
        return
    
    # 交互式模式
    create_output_directories()
    
    while True:
        print_banner()
        
        try:
            choice = input("\n请选择功能 (1-4): ").strip()
            
            if choice == "1":
                content_generation()
            elif choice == "2":
                image_generation()
            elif choice == "3":
                summarizer_generation()
            elif choice == "4":
                print("\n👋 感谢使用！")
                break
            else:
                print("\n❌ 无效选择，请输入 1-4")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序已退出")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
        
        # 询问是否继续
        if choice in ["1", "2", "3"]:
            continue_choice = input("\n是否继续使用其他功能？(y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes', '是']:
                print("\n👋 感谢使用！")
                break

if __name__ == "__main__":
    main()