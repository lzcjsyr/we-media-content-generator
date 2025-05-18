# 自媒体内容生成工具

这是一个自动化工具，可以根据输入文本生成内容摘要和配图，适合自媒体创作者使用。

## 功能

1. 读取输入文本文件
2. 使用 Claude 3.7 Sonnet 生成约500字的专业总结
3. 为总结中的每个段落生成配图
4. 输出：
   - 文本总结 (summary.txt)
   - 段落配图 (image_1.png, image_2.png, ...)
   - Markdown 格式报告 (report.md)
   - HTML 格式报告 (report.html)

## 安装依赖

```bash
uv pip install -r requirements.txt
```

## 使用方法

1. 确保 `.env` 文件中包含必要的 API 密钥
2. 准备输入文本文件 (默认为 `input.txt`)
3. 运行脚本:

```bash
python content_generator.py
```

4. 按照提示输入文件路径，或直接按回车使用默认的 `input.txt`
5. 脚本会创建一个新的输出文件夹 (`output_年月日_时分秒`)，所有生成的内容都将保存在这个文件夹中

## 输出文件夹结构

```
output_YYYYMMDD_HHMMSS/
├── summary.txt       # 生成的文本总结
├── image_1.png       # 第一个段落的配图
├── image_2.png       # 第二个段落的配图
├── ...
├── report.md         # Markdown 格式的完整报告
└── report.html       # HTML 格式的完整报告
```

## 注意事项

- 确保您有足够的 API 调用额度
- 图片生成可能需要一些时间，脚本会显示进度
- 如果遇到 API 限制，脚本会在每次图片生成之间添加延迟
