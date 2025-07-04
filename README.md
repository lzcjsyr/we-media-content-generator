# 🚀 自媒体内容生成工具 v2.0

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-Compatible-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个强大的AI驱动的自媒体内容创作工具套件，专为内容创作者设计。能够将严肃的学术期刊文章转化为生动有趣的社交媒体内容，支持多种AI模型和自动图片生成。

## 🆕 v2.0 更新内容

- **统一入口**: 新增 `start.py` 作为统一启动入口，支持交互式菜单和命令行参数
- **模块化设计**: 将核心功能重新组织到 `functions/` 模块中，提高代码可维护性
- **优化用户体验**: 提供友好的交互界面，清晰的功能选择和参数配置
- **智能路径管理**: 自动创建输出目录，确保跨平台兼容性

## ✨ 核心特色

### 🎯 智能内容转化
- **期刊文章重塑**：将《经济学人》等高端杂志的深度内容转化为适合中国社交媒体传播的生动故事
- **多标题生成**：一次性生成3个不同角度的标题方案（现象描述、影响分析、趋势预测）
- **分段式内容**：自动生成引言和多个段落，每段配有生动的小标题
- **社交媒体优化**：语言接地气，支持emoji表情，适合微信公众号等平台

### 🤖 多模型支持
- **OpenRouter集成**：支持Claude 3.7 Sonnet、Gemini 2.5 Pro、DeepSeek R1等顶级模型
- **模型比较**：并行使用多个模型生成内容，生成详细比较报告
- **灵活切换**：可根据需求选择最适合的模型

### 🖼️ 智能配图生成
- **段落配图**：为每个段落生成对应的插图
- **封面图片**：为整篇文章生成封面配图
- **微信公众号风格**：专为中文社交媒体优化的视觉风格

### 📚 期刊摘要系统
- **多期刊支持**：经济学人、纽约客、大西洋月刊、连线杂志
- **EPUB处理**：自动提取和解析EPUB格式文件
- **智能摘要**：每篇文章生成300字精炼摘要

## 🛠️ 技术栈

```python
# 核心技术
- Python 3.8+
- OpenAI API (兼容OpenRouter)
- AI图片生成 (AiHubMix)

# 主要依赖
- openai: AI模型调用
- python-docx: Word文档生成
- ebooklib: EPUB文件处理
- beautifulsoup4: HTML内容解析
- json-repair: JSON格式修复
```

## 📦 安装配置

### 1. 环境准备
```bash
# 克隆项目
git clone <repository-url>
cd 自媒体内容生成

# 创建虚拟环境 (推荐)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r functions/requirements.txt
```

### 2. 环境变量配置
创建 `.env` 文件：
```env
# OpenRouter API配置
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# 模型配置
OPENROUTER_Claude_3.7_Sonnet=anthropic/claude-3.5-sonnet
OPENROUTER_Gemini_2.5_Pro=google/gemini-2.0-flash-exp
OPENROUTER_DeepSeek_R1=deepseek/deepseek-r1

# AiHubMix图片生成
AIHUBMIX_API_KEY=your_aihubmix_api_key
AIHUBMIX_BASE_URL=your_aihubmix_base_url
AIHUBMIX_IMAGE_GENERATION_MODEL=flux-1.1-pro
```

## 🚀 快速开始

### 🎮 交互式启动（推荐）
```bash
# 启动统一入口程序
python start.py
```

程序将显示友好的交互式菜单，您可以选择：
1. **📝 内容生成** - 根据input.txt生成文章和配图
2. **🖼️ 独立图片生成** - 根据文本描述生成图片
3. **📚 期刊摘要** - 处理期刊EPUB文件生成摘要

### 💻 命令行模式
```bash
# 直接启动内容生成
python start.py --mode content

# 直接生成图片
python start.py --mode image --prompt "一只可爱的小猫在花园里"

# 启动期刊摘要
python start.py --mode summary
```

### 📝 内容生成详细说明

#### 准备工作
1. 在当前目录创建或编辑 `input.txt` 文件
2. 将要转换的期刊文章内容放入文件中
3. 运行 `python start.py` 选择功能1

#### 配置选项
- **图像模式**: 
  - 模式1: 每段配图（推荐）
  - 模式2: 仅封面图
  - 模式3: 无图模式
- **AI模型**: Claude 3.7 Sonnet / Gemini 2.5 Pro / DeepSeek R1
- **创作要求**: 可自定义写作风格和要求

### 🖼️ 图片生成说明

支持三种生成方式：
1. **单张生成**: 输入一个描述，生成一张图片
2. **批量生成**: 从文件读取多个描述，批量生成
3. **交互模式**: 连续输入多个描述，实时生成

### 📚 期刊摘要说明

支持处理以下期刊的EPUB文件：
- 经济学人 (The Economist)
- 纽约客 (The New Yorker)
- 大西洋月刊 (The Atlantic)
- 连线 (Wired)

#### 🆕 智能摘要流程
1. **自动检查更新**: 检查GitHub上期刊仓库是否有新内容
2. **用户确认更新**: 询问是否同步最新的期刊文件
3. **智能分析统计**: 分析本地文件数量与已生成摘要数量
4. **可视化表格**: 清晰显示各期刊的处理状态
5. **灵活处理选项**: 
   - 单个期刊处理
   - 批量处理待处理期刊
   - 强制重新处理所有期刊

#### 📊 统计表格示例

| 序号 | 期刊名称    | 本地文件 | 已生成摘要 | 待处理 | 状态          |
|------|-------------|----------|------------|--------|---------------|
| 1    | 经济学人    | 65       | 52         | 13     | 📝 待处理13篇 |
| 2    | 纽约客      | 78       | 78         | 0      | ✅ 完成       |
| 3    | 大西洋月刊  | 19       | 15         | 4      | 📝 待处理4篇  |
| 4    | 连线        | 18       | 10         | 8      | 📝 待处理8篇  |
| **总计** | **4本期刊** | **180** | **155** | **25** | **📊 统计完成** |

> 📌 表格说明：自动统计各期刊的文件数量和处理状态，帮助用户快速了解工作进度

## 📁 项目结构

```
内容生成器/
├── 📄 README.md                 # 项目说明文档
├── 🔧 .env                      # 环境变量配置
├── 📝 input.txt                 # 输入文章示例
├── 🚀 start.py                  # 统一启动入口（新增）
│
├── 🎯 functions/                # 核心功能模块（新增）
│   ├── __init__.py              # 模块初始化
│   ├── content_generator.py     # 内容生成主程序
│   ├── image_generator.py       # 独立图片生成工具
│   ├── summarizer.py            # 期刊摘要工具
│   ├── prompts.py               # AI提示词模板
│   └── ⚙️ requirements.txt      # Python依赖包（已移入）
│
├── 📊 输出目录
│   ├── ../完整作品/              # 内容生成输出
│   │   ├── 西方科学家为何扎堆来中国_0531_1608/
│   │   │   ├── report.docx      # 生成的Word报告
│   │   │   ├── content.json     # 结构化内容数据
│   │   │   ├── image_1.png      # 段落配图
│   │   │   └── image_2.png
│   │
│   ├── ../独立图片/              # 独立图片生成输出（新增）
│   │   ├── generated_image_0704_1412.png
│   │   └── custom_image_0704_1415.png
│   │
│   └── 摘要汇总/                 # 期刊摘要目录
│       ├── 大西洋月刊/           # 大西洋月刊摘要
│       ├── 经济学人/             # 经济学人摘要
│       ├── 纽约客/               # 纽约客摘要
│       └── 连线/                 # 连线摘要
```

## 💡 使用示例

### 输入示例（input.txt）
```text
**China's universities are wooing Western scientists**
And they are reaching beyond academics with Chinese heritage
May 22nd 2025

Charles lieber had few options. On April 28th the renowned 
former Harvard chemist took up a new post at Tsinghua 
University's Shenzhen campus...
```

### 输出示例
```json
{
  "title_1": "西方科学家为啥都跑中国了",
  "title_2": "人才大战：中国的逆袭时刻", 
  "title_3": "科学家用脚投票的真相",
  "introduction": "一个有趣的现象正在发生：越来越多顶级西方科学家开始选择中国...",
  "paragraphs": [
    {
      "subtitle": "😮 现象很意外",
      "content": "说起来有意思，最近《经济学人》5月22日这期报道了一个现象..."
    }
  ]
}
```

## ⚙️ 高级功能

### 🎨 自定义提示词
编辑 `prompts.py` 文件可以：
- 调整写作风格和语调
- 修改图片生成样式
- 自定义输出格式

### 📊 高级功能

#### 批量处理
```bash
# 使用交互式菜单进行批量图片生成
python start.py
# 选择功能2，然后选择批量生成模式

# 或者直接调用functions模块
python functions/image_generator.py --batch prompts.txt
```

#### 直接调用模块
```python
# 如果需要在其他代码中调用功能
from functions import generate_content, generate_image

# 生成内容
generate_content(image_mode=1, model="claude-3.5-sonnet")

# 生成图片
generate_image("一只可爱的小猫", "../独立图片")
```

### 🔧 API限制处理
- 自动重试机制
- 错误恢复
- API调用频率控制

## 🚨 注意事项

### API使用
- 确保API密钥有足够额度
- 图片生成可能需要较长时间
- 建议在稳定网络环境下使用

### 文件处理
- 输入文件需要UTF-8编码
- 生成的文件会自动创建时间戳目录
- 建议定期清理输出文件

### 内容质量
- 生成内容仅供参考，请人工审核
- 不同模型效果可能有差异
- 可根据需要调整temperature参数

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 📮 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 [GitHub Issue](issues)
- 邮件联系：your-email@example.com

---

*让AI帮你把严肃内容变成有趣故事！* 🎉
