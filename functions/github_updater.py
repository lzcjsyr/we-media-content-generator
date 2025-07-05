#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GitHub更新检查模块
负责检查和更新期刊仓库
"""

import os
import subprocess
from .summarizer import REPO_PATH

def check_github_updates():
    """检查GitHub上的期刊仓库是否有更新"""
    try:
        print("🔍 检查GitHub期刊仓库同步状态...")
        
        # 检查仓库是否存在
        if not os.path.exists(REPO_PATH):
            print("📁 本地未发现期刊仓库")
            return True, "需要克隆仓库"
        
        # 检查是否为Git仓库
        git_dir = os.path.join(REPO_PATH, '.git')
        if not os.path.exists(git_dir):
            print("❌ 本地目录不是Git仓库")
            return True, "需要重新克隆"
        
        try:
            # 切换到仓库目录并获取远程更新
            original_cwd = os.getcwd()
            os.chdir(REPO_PATH)
            
            # 检查是否有远程分支
            result = subprocess.run(['git', 'remote', '-v'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0 or not result.stdout.strip():
                print("❌ 未配置远程仓库")
                return True, "需要配置远程仓库"
            
            # 获取远程更新信息
            print("  正在获取远程更新信息...")
            result = subprocess.run(['git', 'fetch'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                print(f"⚠️ 获取远程更新失败: {result.stderr.strip()}")
                return False, "网络连接问题"
            
            # 比较本地和远程提交
            local_result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                                        capture_output=True, text=True, timeout=10)
            remote_result = subprocess.run(['git', 'rev-parse', 'origin/main'], 
                                         capture_output=True, text=True, timeout=10)
            
            if local_result.returncode != 0 or remote_result.returncode != 0:
                # 尝试master分支
                remote_result = subprocess.run(['git', 'rev-parse', 'origin/master'], 
                                             capture_output=True, text=True, timeout=10)
                if remote_result.returncode != 0:
                    print("⚠️ 无法获取远程分支信息")
                    return False, "分支检查失败"
            
            local_commit = local_result.stdout.strip()
            remote_commit = remote_result.stdout.strip()
            
            if local_commit == remote_commit:
                print("✅ 本地仓库已是最新版本")
                return False, "已是最新"
            else:
                print("🆕 发现远程仓库有更新")
                # 获取更新数量
                count_result = subprocess.run(['git', 'rev-list', '--count', f'{local_commit}..{remote_commit}'], 
                                            capture_output=True, text=True, timeout=10)
                if count_result.returncode == 0:
                    update_count = count_result.stdout.strip()
                    print(f"   有 {update_count} 个新提交")
                return True, f"有 {update_count if 'update_count' in locals() else '?'} 个更新"
                
        except subprocess.TimeoutExpired:
            print("⚠️ Git操作超时")
            return False, "操作超时"
        except Exception as e:
            print(f"⚠️ Git检查出错: {str(e)[:50]}")
            return False, "检查出错"
        finally:
            # 恢复原始工作目录
            if 'original_cwd' in locals():
                os.chdir(original_cwd)
            
    except ImportError:
        print("❌ 无法导入summarizer模块，请检查依赖")
        return False, "模块导入失败"

def update_repo_if_needed():
    """根据用户选择更新仓库"""
    try:
        from .summarizer import check_and_update_repo
        
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