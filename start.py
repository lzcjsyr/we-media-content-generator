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
    from functions.summarizer import main as summarizer_main
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
    input_file = "input.txt"
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
    dirs = ["../完整作品", "../独立图片", "摘要汇总"]
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
    
    print("\n🎨 图像生成模式选择:")
    print("  1. 每段配图 (推荐) - 为每个段落生成配图")
    print("  2. 封面图片 - 仅为整篇文章生成一张封面图")
    print("  3. 无图模式 - 仅生成文字内容")
    
    try:
        image_mode = int(input("\n请选择图像模式 (1-3): "))
        if image_mode not in [1, 2, 3]:
            print("❌ 无效选择，使用默认模式1")
            image_mode = 1
    except ValueError:
        print("❌ 输入无效，使用默认模式1")
        image_mode = 1
    
    print("\n🤖 AI模型选择:")
    print("  1. Claude 3.7 Sonnet (推荐) - 写作质量最高")
    print("  2. Gemini 2.5 Pro - 创意度较高")
    print("  3. DeepSeek R1 - 性价比高")
    
    # 模型映射 - 使用环境变量中的模型名称
    import os
    models = {
        1: os.getenv("OPENROUTER_Claude_3.7_Sonnet", "anthropic/claude-3.5-sonnet"),
        2: os.getenv("OPENROUTER_Gemini_2.5_Pro", "google/gemini-2.0-flash-exp"), 
        3: os.getenv("OPENROUTER_DeepSeek_R1", "deepseek/deepseek-r1")
    }
    
    try:
        model_choice = int(input("\n请选择模型 (1-3): "))
        model = models.get(model_choice, models[1])
    except ValueError:
        print("❌ 输入无效，使用默认模型Claude")
        model = models[1]
    
    # 额外要求
    reqs = input("\n📋 额外创作要求 (可选，直接回车跳过): ").strip()
    if not reqs:
        reqs = "文章语言自然流畅，但要通过转折、惊喜、反转等手法，让读者有阅读的欲望。同时让文章有深度，有思考，有启发。"
    
    print(f"\n🚀 开始生成内容...")
    print(f"   图像模式: {['', '每段配图', '封面图片', '无图模式'][image_mode]}")
    print(f"   AI模型: {['', 'Claude 3.7 Sonnet', 'Gemini 2.5 Pro', 'DeepSeek R1'][model_choice if 'model_choice' in locals() else 1]}")
    print(f"   额外要求: {reqs}")
    
    try:
        content_main(
            image_mode=image_mode,
            model=model,
            reqs=reqs,
            temperature=0.7,
            image_model="GPT-Image",
            image_style="\n\n有视觉冲击的电影宣传海报质感，超高清展示，细节清晰，没有文字。",
            image_size="1536x1024",
            image_quality="high",
            image_moderation="low",
            image_background="auto"
        )
        print("\n✅ 内容生成完成!")
        print("📁 输出位置: ../完整作品/ 文件夹")
    except Exception as e:
        print(f"\n❌ 内容生成失败: {e}")

def image_generation():
    """独立图片生成工作流"""
    print("\n" + "="*50)
    print("🖼️ 独立图片生成模式")
    print("="*50)
    
    print("\n📋 图片生成方式:")
    print("  1. 单张图片 - 输入一个描述生成一张图片")
    print("  2. 批量生成 - 从文件读取多个描述批量生成")
    print("  3. 交互模式 - 连续输入多个描述")
    
    try:
        mode = int(input("\n请选择生成方式 (1-3): "))
    except ValueError:
        print("❌ 输入无效，使用默认模式1")
        mode = 1
    
    if mode == 1:
        # 单张图片生成
        prompt = input("\n📝 请输入图片描述: ").strip()
        if not prompt:
            print("❌ 图片描述不能为空")
            return
        
        filename = input("🏷️ 文件名前缀 (可选): ").strip()
        
        print(f"\n🚀 正在生成图片...")
        try:
            file_paths = generate_image(
                prompt=prompt,
                output_dir=None,  # 使用默认目录
                filename=filename if filename else None,
                image_model="GPT-Image",
                count=1
            )
            
            if file_paths:
                print(f"\n✅ 图片生成成功:")
                for path in file_paths:
                    print(f"  📷 {path}")
            else:
                print("\n❌ 图片生成失败")
        except Exception as e:
            print(f"\n❌ 图片生成失败: {e}")
    
    elif mode == 2:
        # 批量生成
        batch_file = input("\n📄 批量描述文件路径 (每行一个描述): ").strip()
        if not batch_file:
            print("❌ 文件路径不能为空")
            return
        
        if not os.path.exists(batch_file):
            print(f"❌ 文件不存在: {batch_file}")
            return
        
        print(f"\n🚀 正在批量生成图片...")
        try:
            prompts = read_prompts_from_file(batch_file)
            if not prompts:
                print("❌ 未能从文件中读取到有效的描述文本")
                return
            
            print(f"📝 找到 {len(prompts)} 个描述")
            successful_files = generate_batch_images(prompts, None, "GPT-Image")
            
            print(f"\n✅ 批量生成完成! 成功生成 {len(successful_files)} 张图片")
            print("📁 输出位置: ../独立图片/ 文件夹")
        except Exception as e:
            print(f"\n❌ 批量生成失败: {e}")
    
    elif mode == 3:
        # 交互模式
        print("\n🔄 进入交互模式，输入 'quit' 或 'exit' 退出")
        while True:
            try:
                prompt = input("\n📝 请输入图片描述: ").strip()
                if prompt.lower() in ['quit', 'exit', 'q']:
                    print("👋 退出交互模式")
                    break
                
                if not prompt:
                    print("❌ 描述文本不能为空")
                    continue
                
                print(f"🚀 正在生成图片...")
                file_paths = generate_image(
                    prompt=prompt,
                    output_dir=None,  # 使用默认目录
                    filename=None,
                    image_model="GPT-Image",
                    count=1
                )
                
                if file_paths:
                    print(f"✅ 生成成功:")
                    for path in file_paths:
                        print(f"  📷 {path}")
                else:
                    print("❌ 生成失败")
                    
            except KeyboardInterrupt:
                print("\n\n👋 退出交互模式")
                break
            except Exception as e:
                print(f"❌ 生成失败: {e}")

def check_github_updates():
    """检查GitHub上的期刊仓库是否有更新"""
    try:
        from functions.summarizer import check_and_update_repo, REPO_PATH
        import subprocess
        
        print("\n🔍 检查GitHub期刊仓库更新状态...")
        
        # 如果仓库不存在，直接返回需要克隆
        if not os.path.exists(REPO_PATH):
            print("📁 本地未发现期刊仓库")
            return True, "需要克隆仓库"
        
        # 检查是否有远程更新
        try:
            # 获取远程更新信息
            subprocess.run(['git', 'fetch'], cwd=REPO_PATH, capture_output=True, timeout=30)
            
            # 比较本地和远程提交
            local_result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                                        cwd=REPO_PATH, capture_output=True, text=True)
            remote_result = subprocess.run(['git', 'rev-parse', 'origin/main'], 
                                         cwd=REPO_PATH, capture_output=True, text=True)
            
            if local_result.returncode == 0 and remote_result.returncode == 0:
                local_commit = local_result.stdout.strip()
                remote_commit = remote_result.stdout.strip()
                
                if local_commit == remote_commit:
                    print("✅ 期刊仓库已是最新版本")
                    return False, "已是最新"
                else:
                    print("🆕 发现期刊仓库有更新")
                    return True, "有新内容"
            else:
                print("⚠️ 无法检查更新状态")
                return False, "检查失败"
                
        except Exception as e:
            print(f"⚠️ 检查更新时出错: {e}")
            return False, "检查出错"
            
    except ImportError:
        print("❌ 无法导入summarizer模块，请检查依赖")
        return False, "模块导入失败"

def update_repo_if_needed():
    """根据用户选择更新仓库"""
    try:
        from functions.summarizer import check_and_update_repo
        
        print("\n🔄 正在更新期刊仓库...")
        success = check_and_update_repo()
        
        if success:
            print("✅ 期刊仓库更新完成")
            return True
        else:
            print("❌ 期刊仓库更新失败")
            return False
            
    except Exception as e:
        print(f"❌ 更新过程出错: {e}")
        return False

def analyze_local_files_and_summaries():
    """分析本地期刊文件和已生成摘要的数量"""
    try:
        from functions.summarizer import MAGAZINE_CONFIG, REPO_PATH
        import glob
        
        # 期刊配置
        magazines_info = []
        
        for key, config in MAGAZINE_CONFIG.items():
            magazine_name = config["title"]
            
            # 统计本地期刊文件数量
            epub_count = 0
            if os.path.exists(REPO_PATH):
                magazine_path = os.path.join(REPO_PATH, config["base_dir"])
                if os.path.exists(magazine_path):
                    # 查找所有epub文件
                    pattern = os.path.join(magazine_path, "**", "*.epub")
                    epub_files = glob.glob(pattern, recursive=True)
                    epub_count = len(epub_files)
            
            # 统计已生成摘要数量
            summary_count = 0
            summary_path = os.path.join("摘要汇总", config["title"])
            if os.path.exists(summary_path):
                json_files = glob.glob(os.path.join(summary_path, "*.json"))
                summary_count = len(json_files)
            
            # 计算未处理数量
            pending_count = max(0, epub_count - summary_count)
            
            magazines_info.append({
                "key": key,
                "name": magazine_name,
                "epub_count": epub_count,
                "summary_count": summary_count,
                "pending_count": pending_count
            })
        
        return magazines_info
        
    except Exception as e:
        print(f"❌ 分析本地文件时出错: {e}")
        return []

def display_magazine_table(magazines_info):
    """以表格形式显示期刊信息"""
    print("\n" + "="*80)
    print("📊 期刊文件和摘要统计表")
    print("="*80)
    
    # 表头
    print(f"{'序号':<4} {'期刊名称':<12} {'本地文件':<8} {'已生成摘要':<10} {'待处理':<8} {'状态':<10}")
    print("-" * 80)
    
    total_epub = 0
    total_summary = 0
    total_pending = 0
    
    for i, info in enumerate(magazines_info, 1):
        status = "✅ 完成" if info["pending_count"] == 0 else f"📝 待处理{info['pending_count']}篇"
        
        print(f"{i:<4} {info['name']:<12} {info['epub_count']:<8} {info['summary_count']:<10} {info['pending_count']:<8} {status:<10}")
        
        total_epub += info["epub_count"]
        total_summary += info["summary_count"]
        total_pending += info["pending_count"]
    
    print("-" * 80)
    print(f"{'总计':<4} {'':<12} {total_epub:<8} {total_summary:<10} {total_pending:<8}")
    print("="*80)
    
    return magazines_info

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
    magazines_info = analyze_local_files_and_summaries()
    
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
    print(f"  {len(magazines_info) + 2}. 强制重新处理所有期刊")
    
    try:
        choice = int(input(f"\n请选择 (1-{len(magazines_info) + 2}): "))
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
            # 调用具体的处理函数
            print("📋 请直接使用以下命令进行处理:")
            print(f"python functions/summarizer.py {selected_magazine['key']}")
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            
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
            for magazine in pending_magazines:
                print(f"\n📋 处理 {magazine['name']}，请使用:")
                print(f"python functions/summarizer.py {magazine['key']}")
        else:
            print("❌ 取消批量处理")
            
    elif choice == len(magazines_info) + 2:
        # 强制重新处理所有期刊
        print("\n⚠️ 强制重新处理将覆盖所有现有摘要")
        confirm = input("确认继续？(y/n): ").strip().lower()
        
        if confirm in ['y', 'yes', '是']:
            print("\n🚀 开始强制重新处理所有期刊...")
            print("📋 请依次使用以下命令:")
            for magazine in magazines_info:
                print(f"python functions/summarizer.py {magazine['key']} --force")
        else:
            print("❌ 取消强制处理")
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
                file_paths = generate_image(args.prompt, "../独立图片")
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