# 🚀 自媒体内容生成工具

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-Compatible-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个强大的AI驱动的自媒体内容创作工具套件，专为内容创作者设计。能够将严肃的学术期刊文章转化为生动有趣的社交媒体内容，支持多种AI模型和自动图片生成。

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
pip install -r requirements.txt
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

## 🚀 使用指南

### 📝 内容生成

#### 基础使用
```python
# 编辑 input.txt 文件，放入源文章内容
# 运行内容生成
python content_generator.py
```

#### 高级配置
```python
from content_generator import main, OPENROUTER_CLAUDE_MODEL

# 自定义配置
main(
    image_mode=1,  # 1:每段配图 2:封面图 3:无图
    model=OPENROUTER_CLAUDE_MODEL,  # 选择模型
    reqs="文章风格要活泼有趣，适合年轻人阅读",  # 额外要求
    temperature=0.7  # 创意度控制 (0-1)
)
```

#### 图片生成模式
- **模式1（推荐）**：为每个段落生成配图，适合图文并茂的公众号文章
- **模式2**：仅生成封面图，适合简洁风格
- **模式3**：不生成图片，仅文字内容

### 🔍 模型比较
```python
# 使用三个模型同时生成，对比效果
python model_comparison.py

# 自定义比较
from model_comparison import main
main(
    reqs="写作风格要专业严谨",
    temperature=0.5
)
```

### 📖 期刊摘要
```bash
# 处理单个期刊
python summarizer.py --magazine atlantic    # 大西洋月刊
python summarizer.py --magazine economist   # 经济学人
python summarizer.py --magazine new_yorker  # 纽约客

# 处理所有期刊
python summarizer.py --all
```

## 📁 项目结构

```
自媒体内容生成/
├── 📄 README.md                 # 项目说明文档
├── ⚙️ requirements.txt          # Python依赖包
├── 🔧 .env                      # 环境变量配置
├── 📝 input.txt                 # 输入文章示例
│
├── 🎯 核心模块
│   ├── content_generator.py     # 内容生成主程序
│   ├── model_comparison.py      # 模型比较工具
│   ├── summarizer.py            # 期刊摘要工具
│   └── prompts.py               # AI提示词模板
│
├── 📊 输出示例
│   ├── 西方科学家为何扎堆来中国_0531_1608/
│   │   ├── report.docx          # 生成的Word报告
│   │   ├── content.json         # 结构化内容数据
│   │   ├── image_1.png          # 段落配图
│   │   └── image_2.png
│   │
│   └── summary/                 # 期刊摘要目录
│       ├── atlantic/            # 大西洋月刊摘要
│       ├── economist/           # 经济学人摘要
│       └── new_yorker/          # 纽约客摘要
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

### 📊 批量处理
```python
# 批量处理多个文件
import os
from content_generator import generate_content_with_title

for file in os.listdir("inputs/"):
    if file.endswith(".txt"):
        # 处理每个文件
        pass
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
