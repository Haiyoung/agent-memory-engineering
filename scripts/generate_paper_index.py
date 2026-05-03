#!/usr/bin/env python3
"""
从 paper/ 目录扫描所有论文简报，按 arxiv ID 排序，
输出可用于书籍附录的索引表。
"""
import os
import re
import json
from pathlib import Path

def extract_arxiv_id(filename):
    """从文件名提取 arxiv ID"""
    match = re.match(r'(\d{4}\.\d{4,5})', filename)
    return match.group(1) if match else None

def extract_title(filepath):
    """从论文简报提取标题（第一行 # 标题）"""
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('# '):
                return line[2:].strip()
    return 'Unknown'

def scan_papers(root='paper'):
    """扫描所有论文"""
    papers = []
    for year_dir in sorted(os.listdir(root)):
        year_path = os.path.join(root, year_dir)
        if not os.path.isdir(year_path):
            continue
        for fname in os.listdir(year_path):
            if not fname.endswith('.md'):
                continue
            arxiv_id = extract_arxiv_id(fname)
            if arxiv_id:
                title = extract_title(os.path.join(year_path, fname))
                papers.append({
                    'arxiv_id': arxiv_id,
                    'title': title,
                    'year': year_dir,
                    'file': os.path.join(year_path, fname)
                })
    return sorted(papers, key=lambda x: x['arxiv_id'])

def generate_index(papers):
    """生成 Markdown 索引表"""
    lines = ['# 论文索引\n\n']
    lines.append(f'共收录 {len(papers)} 篇论文，按 arxiv ID 排序。\n\n')
    lines.append('| arxiv ID | 标题 | 年份 | 书籍章节 |\n')
    lines.append('|----------|------|------|----------|\n')
    for p in papers:
        lines.append(f"| {p['arxiv_id']} | {p['title']} | {p['year']} | |\n")
    return ''.join(lines)

if __name__ == '__main__':
    papers = scan_papers()
    index = generate_index(papers)
    print(index)
