#!/usr/bin/env python3
"""
将 Markdown 周报转换为 PDF
支持多种转换方式，提高兼容性
"""

import sys
import os
import subprocess

def check_dependencies():
    """检查可用的依赖并返回最佳转换方式"""
    # 方式 1: 尝试使用 markdown-pdf（优先，因为用户已安装）
    try:
        import markdown_pdf
        return "markdown-pdf", markdown_pdf
    except ImportError:
        pass

    # 方式 2: 尝试使用 weasyprint
    try:
        import markdown
        from weasyprint import HTML, CSS
        return "weasyprint", (markdown, HTML, CSS)
    except ImportError:
        pass
    except OSError:
        pass

    # 方式 3: 尝试使用 pandoc
    try:
        subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
        return "pandoc", None
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # 方式 4: 尝试使用 markdown + pdfkit
    try:
        import markdown
        import pdfkit
        return "pdfkit", (markdown, pdfkit)
    except ImportError:
        pass

    return None, None

def md_to_html(md_content, title="周报"):
    """将 Markdown 转换为 HTML（用于多种转换方式）"""
    try:
        import markdown
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    except ImportError:
        # 如果没有 markdown 库，简单处理
        html_content = md_content.replace('\n', '<br>\n')

    # 添加样式
    css = '''
        <style>
            @page {
                size: A4;
                margin: 2.5cm;
            }
            body {
                font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
                font-size: 12pt;
                line-height: 1.8;
                color: #333;
            }
            h1 {
                font-size: 16pt;
                text-align: center;
                margin-bottom: 30px;
                color: #000;
            }
            h3 {
                font-size: 14pt;
                margin-top: 25px;
                margin-bottom: 15px;
                color: #000;
                border-bottom: 1px solid #ddd;
                padding-bottom: 5px;
            }
            ol {
                margin-left: 0;
                padding-left: 25px;
            }
            li {
                margin-bottom: 8px;
            }
            strong {
                font-weight: bold;
                color: #000;
            }
        </style>
    '''

    # 包装成完整 HTML
    full_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        {css}
    </head>
    <body>
        {html_content}
    </body>
    </html>
    '''
    return full_html

def md_to_pdf_markdown_pdf(md_content, output_path, title="周报"):
    """使用 markdown-pdf 转换（推荐）"""
    import markdown_pdf

    # 创建 MarkdownPdf 实例
    pdf = markdown_pdf.MarkdownPdf(toc_level=3)

    # 添加自定义 CSS 来支持中文和美化样式
    custom_css = '''
        body {
            font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
            font-size: 12pt;
            line-height: 1.8;
            color: #333;
        }
        h1 {
            font-size: 16pt;
            text-align: center;
            margin-bottom: 30px;
            color: #000;
        }
        h3 {
            font-size: 14pt;
            margin-top: 25px;
            margin-bottom: 15px;
            color: #000;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }
        ol {
            margin-left: 0;
            padding-left: 25px;
        }
        li {
            margin-bottom: 8px;
        }
        strong {
            font-weight: bold;
            color: #000;
        }
    '''

    # 创建 section 并添加到 pdf
    section = markdown_pdf.Section(md_content, toc=False, paper_size='A4', borders=(72, 72, -72, -72))
    pdf.add_section(section, user_css=custom_css)

    # 保存 PDF
    pdf.save(output_path)
    print(f"PDF 已生成 (markdown-pdf): {output_path}")

def md_to_pdf_weasyprint(md_content, output_path, title="周报"):
    """使用 weasyprint 转换"""
    import markdown
    from weasyprint import HTML, CSS

    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    css = CSS(string='''
        @page {
            size: A4;
            margin: 2.5cm;
        }
        body {
            font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
            font-size: 12pt;
            line-height: 1.8;
            color: #333;
        }
        h1 {
            font-size: 16pt;
            text-align: center;
            margin-bottom: 30px;
            color: #000;
        }
        h3 {
            font-size: 14pt;
            margin-top: 25px;
            margin-bottom: 15px;
            color: #000;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }
        ol {
            margin-left: 0;
            padding-left: 25px;
        }
        li {
            margin-bottom: 8px;
        }
        strong {
            font-weight: bold;
            color: #000;
        }
    ''')

    full_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    '''

    HTML(string=full_html).write_pdf(output_path, stylesheets=[css])
    print(f"PDF 已生成 (weasyprint): {output_path}")

def md_to_pdf_pandoc(input_file, output_path):
    """使用 pandoc 转换"""
    cmd = ['pandoc', input_file, '-o', output_path, '--pdf-engine=xelatex', '-V', 'CJKmainfont=PingFang SC']
    subprocess.run(cmd, check=True)
    print(f"PDF 已生成 (pandoc): {output_path}")

def md_to_pdf_simple(md_content, output_path, title="周报"):
    """简单方案：生成 HTML 文件，指导用户用浏览器打开并打印为 PDF"""
    html_content = md_to_html(md_content, title)
    html_path = output_path.replace('.pdf', '.html')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML 文件已生成: {html_path}")
    print("")
    print("由于系统缺少 PDF 转换依赖，请按以下步骤操作：")
    print(f"1. 在浏览器中打开: {html_path}")
    print("2. 按 Cmd+P (Mac) 或 Ctrl+P (Windows/Linux) 打开打印对话框")
    print("3. 选择 '保存为 PDF' 或 'Save as PDF'")
    print(f"4. 保存为: {output_path}")

def md_to_pdf(md_content, output_path, title="周报", input_file=None):
    """主转换函数，自动选择最佳方式"""
    method, deps = check_dependencies()

    if method == "markdown-pdf":
        try:
            md_to_pdf_markdown_pdf(md_content, output_path, title)
            return
        except Exception as e:
            print(f"markdown-pdf 转换失败: {e}")

    if method == "weasyprint":
        try:
            md_to_pdf_weasyprint(md_content, output_path, title)
            return
        except Exception as e:
            print(f"weasyprint 转换失败: {e}")

    if method == "pandoc" and input_file:
        try:
            md_to_pdf_pandoc(input_file, output_path)
            return
        except Exception as e:
            print(f"pandoc 转换失败: {e}")

    # 回退到简单方案
    md_to_pdf_simple(md_content, output_path, title)

def main():
    if len(sys.argv) < 3:
        print("用法: python md_to_pdf.py <输入.md> <输出.pdf>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"错误: 文件不存在 {input_file}")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    md_to_pdf(md_content, output_file, title="周报", input_file=input_file)

if __name__ == '__main__':
    main()
