#!/usr/bin/env python3
"""
Claude API Report Generation Script
"""

import os
import json
from anthropic import Anthropic
import markdown2
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report_with_claude():
    """Claude APIを使用してレポートを生成"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    # リサーチ結果を読み込み
    with open('output/research_results.json', 'r', encoding='utf-8') as f:
        research_data = json.load(f)
    
    client = Anthropic(api_key=api_key)
    
    # Claudeでレポート生成
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"""Based on the following research results, create a comprehensive report in Markdown format.
                
Research Query: {research_data['query']}
Research Results: {research_data['results']}

Please structure the report with:
1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Recommendations
5. Conclusion

Make it professional and well-formatted."""
            }
        ]
    )
    
    report_content = message.content[0].text
    
    # Markdownファイルとして保存
    with open('output/research_report.md', 'w', encoding='utf-8') as f:
        f.write(f"# Research Report: {research_data['query']}\n\n")
        f.write(f"Generated on: {research_data['timestamp']}\n\n")
        f.write(report_content)
    
    # PDFとして保存
    create_pdf_report(research_data['query'], report_content)
    
    print("✅ Report generated successfully!")
    print("📄 Files created:")
    print("   - output/research_report.md")
    print("   - output/research_report.pdf")

def create_pdf_report(query, content):
    """PDFレポートを作成"""
    doc = SimpleDocTemplate("output/research_report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # タイトル
    title = Paragraph(f"Research Report: {query}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # コンテンツをHTMLに変換してPDFに追加
    html_content = markdown2.markdown(content)
    # 簡単な実装のため、プレーンテキストとして追加
    for line in content.split('\n'):
        if line.strip():
            para = Paragraph(line, styles['Normal'])
            story.append(para)
            story.append(Spacer(1, 6))
    
    doc.build(story)

if __name__ == "__main__":
    generate_report_with_claude()
