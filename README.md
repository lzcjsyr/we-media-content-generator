# 自媒体内容生成工具

这是一个强大的自动化工具，专为自媒体创作者设计，能够处理多种内容生成任务，包括文章创作、杂志摘要生成和内容比较。工具支持多种AI模型，并可以生成包含配图的专业文档。

## 主要功能

1. **内容生成**
   - 根据输入文本生成包含多个标题方案的文章
   - 自动生成引言和分段落内容
   - 支持多种AI模型（Gemini, Claude, DeepSeek）

2. **杂志摘要**
   - 处理EPUB格式的杂志文件
   - 自动提取和总结文章内容
   - 支持多种国际知名杂志（经济学人、纽约客、大西洋月刊等）

3. **模型比较**
   - 并行使用多个AI模型生成内容
   - 生成详细的比较报告
   - 帮助选择最适合特定内容需求的模型

4. **文档输出**
   - 生成格式规范的Word文档
   - 自动添加配图
   - 支持多种输出样式和格式

## 安装

1. 克隆仓库
```bash
git clone <repository-url>
cd 自媒体内容生成
```

2. 安装依赖
```bash
uv pip install -r requirements.txt
```

3. 配置环境变量
创建 `.env` 文件并添加必要的API密钥：
```
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
AIHUBMIX_API_KEY=your_aihubmix_api_key
AIHUBMIX_BASE_URL=your_aihubmix_base_url
```

## 使用方法

### 1. 内容生成
```bash
python content_generator.py
```

### 2. 模型比较
```bash
python model_comparison.py
```

### 3. 杂志摘要
```bash
python summarizer.py --magazine atlantic  # 处理大西洋月刊
python summarizer.py --magazine new_yorker  # 处理纽约客
python summarizer.py --all  # 处理所有支持的杂志
```

## 项目结构

```
.
├── README.md                 # 项目说明
├── requirements.txt          # Python依赖
├── content_generator.py      # 内容生成主程序
├── model_comparison.py       # 模型比较工具
├── summarizer.py             # 杂志摘要工具
├── prompts.py                # AI提示词模板
├── input.txt                 # 示例输入文件
└── summary/                  # 生成的摘要文件
    ├── atlantic/            # 大西洋月刊摘要
    └── new_yorker/          # 纽约客摘要
```

## 依赖

- Python 3.8+
- 主要依赖包：
  - openai
  - python-dotenv
  - python-docx
  - ebooklib
  - beautifulsoup4

## 注意事项

1. 确保您的API密钥有足够的调用额度
2. 图片生成可能需要较长时间，请耐心等待
3. 建议在稳定的网络环境下使用
4. 处理大量文件时，请注意API调用频率限制

## 许可证

[MIT License](LICENSE)
