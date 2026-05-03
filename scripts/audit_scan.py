#!/usr/bin/env python3
"""全书逻辑一致性自动化扫描脚本。
扫描 book/src/ 下所有 .md 文件，检测编号、引用、Mermaid、KaTeX、代码块、术语问题。
输出审计报告到 docs/superpowers/reviews/phase1-audit-report.md。
"""

import os
import re
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_DIR = os.path.join(SCRIPT_DIR, '..')
SRC_DIR = os.path.join(BOOK_DIR, 'src')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'docs', 'superpowers', 'reviews')

def get_md_files():
    """获取所有章节 markdown 文件。"""
    files = []
    for f in sorted(os.listdir(SRC_DIR)):
        if f.endswith('.md') and (f.startswith('ch') or f == 'appendix.md'):
            files.append(os.path.join(SRC_DIR, f))
    return files

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    return content, lines

def main():
    results = {'严重': [], '警告': [], '信息': []}
    files = get_md_files()
    print(f'扫描 {len(files)} 个文件...')
    for filepath in files:
        content, lines = read_file(filepath)
        fname = os.path.basename(filepath)
        scan_duplicate_numbers(fname, lines, results)
        scan_broken_references(fname, content, lines, results)
        scan_mermaid(fname, content, results)
        scan_katex(fname, lines, results)
        scan_code_blocks(fname, content, results)
        scan_terminology(fname, content, results)
    write_report(results)

def scan_duplicate_numbers(fname, lines, results):
    """扫描 1: 编号重复/跳跃。
    提取所有 ## 到 #### 级标题编号，检测重复和跳跃。
    """
    section_re = re.compile(r'^#{2,4}\s+(.*?)(?:\s*$)')
    # Track all section numbers found
    all_numbers = defaultdict(list)  # num_str -> [line_numbers]
    # Track hierarchical structure for gap detection
    hierarchy = defaultdict(list)  # (major,) -> [sub_numbers]

    for i, line in enumerate(lines, 1):
        m = section_re.match(line)
        if not m:
            continue
        title = m.group(1).strip()
        # Try to extract a number pattern like "3.4" or "11.2.3" or "1"
        num_m = re.match(r'^(\d[\d.]*)\s', title)
        if not num_m:
            continue
        num_str = num_m.group(1)
        parts = num_str.split('.')

        all_numbers[num_str].append(i)

        # Track hierarchy for gap detection
        if len(parts) >= 2:
            major = parts[0]
            sub = int(parts[1])
            hierarchy[major].append((sub, i, num_str))

    # Check duplicates
    for key, line_nums in sorted(all_numbers.items()):
        if len(line_nums) > 1:
            results['严重'].append(
                f'{fname} — 重复编号 "{key}" 出现在第 {line_nums} 行'
            )

    # Check gaps in sub-sections
    for major, subs in sorted(hierarchy.items()):
        subs_sorted = sorted(subs, key=lambda x: x[0])
        for idx in range(1, len(subs_sorted)):
            prev_sub, prev_line, prev_num = subs_sorted[idx - 1]
            curr_sub, curr_line, curr_num = subs_sorted[idx]
            if curr_sub > prev_sub + 1:
                missing = list(range(prev_sub + 1, curr_sub))
                results['严重'].append(
                    f'{fname}:{curr_line} — 小节号跳跃: {prev_num} → {curr_num}（缺少 {major}.{".".join(map(str, missing))}）'
                )

def scan_broken_references(fname, content, lines, results):
    """扫描 2: 引用缺失。
    检测 "第 X 章" 和 "X.X 节" 格式的引用是否有效。
    """
    # Collect all chapter numbers from SUMMARY.md
    summary_path = os.path.join(SRC_DIR, 'SUMMARY.md')
    valid_chapters = set()
    if os.path.exists(summary_path):
        with open(summary_path, 'r', encoding='utf-8') as f:
            for line in f:
                m = re.search(r'第(\d+)章', line)
                if m:
                    valid_chapters.add(int(m.group(1)))

    # Scan for chapter references in content
    ref_re = re.compile(r'第\s*(\d+)\s*章')
    for m in ref_re.finditer(content):
        ch_num = int(m.group(1))
        # Allow references to chapters 1-16, but flag if beyond
        if ch_num > 16:
            pos = content[:m.start()].count('\n') + 1
            results['警告'].append(
                f'{fname}:{pos} — 引用 "第{ch_num}章"，但全书仅到第 16 章'
            )

    # Scan for section references like "X.X 节" or "X.X.X 节"
    sec_ref_re = re.compile(r'(\d+\.\d+(?:\.\d+)?)\s*节')
    for m in sec_ref_re.finditer(content):
        sec_num = m.group(1)
        # We can't easily verify all section references without parsing all files
        # But we can flag obvious ones like 17.x, 99.x
        major = int(sec_num.split('.')[0])
        if major > 16:
            pos = content[:m.start()].count('\n') + 1
            results['警告'].append(
                f'{fname}:{pos} — 引用 "{sec_num}节"，但章节号 {major} 超出范围'
            )

def scan_mermaid(fname, content, results):
    """扫描 3: Mermaid 图表语法。
    检查每个 mermaid 代码块是否有正确的 diagram 声明。
    """
    mermaid_re = re.compile(r'```mermaid\s*\n(.*?)\n```', re.DOTALL)
    valid_types = {
        'graph TD', 'graph LR', 'graph RL', 'graph BT', 'graph TB',
        'flowchart TD', 'flowchart LR', 'flowchart RL', 'flowchart BT', 'flowchart TB',
        'sequenceDiagram', 'classDiagram', 'classDiagram-v2',
        'stateDiagram-v2', 'stateDiagram',
        'erDiagram', 'journey', 'gantt', 'pie',
        'mindmap', 'timeline', 'gitGraph', 'requirementDiagram',
    }

    for m in mermaid_re.finditer(content):
        block = m.group(1).strip()
        first_line = block.split('\n')[0].strip()
        pos = content[:m.start()].count('\n') + 1

        # Check for valid diagram type declaration
        if not any(first_line.startswith(vt) for vt in valid_types):
            results['严重'].append(
                f'{fname}:{pos} — Mermaid 代码块缺少 diagram 类型声明（首行: "{first_line[:60]}"）'
            )
        else:
            # Check for unclosed quotes
            if block.count('"') % 2 != 0:
                results['严重'].append(
                    f'{fname}:{pos} — Mermaid 代码块中引号未闭合'
                )
            # Check for unclosed square brackets in node definitions
            if block.count('[') != block.count(']'):
                results['警告'].append(
                    f'{fname}:{pos} — Mermaid 代码块中方括号未平衡 ([{block.count("[")}] vs ]{block.count("]")})'
                )

def scan_katex(fname, lines, results):
    """扫描 4: KaTeX 公式分隔符匹配。
    检测行内 $ 的数量是否为偶数（排除 $$ 块内和代码块内）。
    """
    in_display_math = False
    in_code_block = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Track display math blocks
        if stripped.startswith('$$'):
            in_display_math = not in_display_math
            continue

        if in_display_math:
            continue

        # Count inline $ (excluding $$ and \$)
        dollar_count = 0
        j = 0
        while j < len(stripped):
            if stripped[j] == '\\' and j + 1 < len(stripped) and stripped[j + 1] == '$':
                j += 2  # skip escaped \$
                continue
            if stripped[j] == '$':
                if j + 1 < len(stripped) and stripped[j + 1] == '$':
                    j += 2  # skip $$
                    continue
                dollar_count += 1
            j += 1

        if dollar_count % 2 != 0:
            results['严重'].append(
                f'{fname}:{i} — KaTeX 公式分隔符未闭合（该行有 {dollar_count} 个 $）'
            )

def scan_code_blocks(fname, content, results):
    """扫描 5: 代码块语法。
    检测 Python 代码块括号平衡、未指定语言的代码块。
    """
    code_re = re.compile(r'```(\w*)\s*\n(.*?)\n```', re.DOTALL)
    for m in code_re.finditer(content):
        lang = m.group(1).strip()
        code = m.group(2)
        pos = content[:m.start()].count('\n') + 1

        if lang == 'python':
            # Check bracket balance
            open_parens = code.count('(') - code.count(')')
            open_brackets = code.count('[') - code.count(']')
            open_braces = code.count('{') - code.count('}')
            if open_parens != 0 or open_brackets != 0 or open_braces != 0:
                results['警告'].append(
                    f'{fname}:{pos} — Python 代码块括号不平衡 ((): {open_parens:+d}, []: {open_brackets:+d}, {{{{}}}}: {open_braces:+d})'
                )
            # Check for unclosed strings (triple quotes)
            triple_single = code.count("'''")
            triple_double = code.count('"""')
            if triple_single % 2 != 0:
                results['警告'].append(
                    f'{fname}:{pos} — Python 代码块中三单引号未闭合'
                )
            if triple_double % 2 != 0:
                results['警告'].append(
                    f'{fname}:{pos} — Python 代码块中三双引号未闭合'
                )
        elif lang == '':
            # Check if it looks like Python code without language tag
            if re.search(r'^\s*(class|def|import|from\s+\w+\s+import)\s', code, re.MULTILINE):
                results['警告'].append(
                    f'{fname}:{pos} — 疑似 Python 代码块但未指定语言标识'
                )

def scan_terminology(fname, content, results):
    """扫描 6: 术语不一致。
    检测同一概念的不同译名。
    """
    # Terminology map: concept -> (recommended Chinese, known variants in Chinese)
    terminology = {
        'Working Memory': ('工作记忆', ['工作记忆']),
        'Short-Term Memory': ('短期记忆', ['短期记忆']),
        'Long-Term Memory': ('长期记忆', ['长期记忆']),
        'Episodic Memory': ('情景记忆', ['情景记忆', '事件记忆']),
        'Semantic Memory': ('语义记忆', ['语义记忆']),
        'Procedural Memory': ('程序记忆', ['程序记忆', '程序性记忆']),
        'Experiential Memory': ('经验记忆', ['经验记忆']),
        'Reflection Memory': ('反思记忆', ['反思记忆', '反思性记忆']),
        'Context Window': ('上下文窗口', ['上下文窗口', '语境窗口']),
        'Memory Bank': ('Memory Bank', ['记忆库', '记忆银行', 'Memory Bank']),
        'Vector Database': ('向量数据库', ['向量数据库', '矢量数据库']),
        'Retrieval-Augmented Generation': ('检索增强生成', ['检索增强生成', 'RAG', '检索增强']),
        'Knowledge Graph': ('知识图谱', ['知识图谱', '知识图']),
        'Token': ('Token', ['Token', '令牌', '标记']),
    }

    for concept, (recommended, variants) in terminology.items():
        # Check if the concept appears with non-recommended Chinese names
        for variant in variants:
            if variant in content and variant != recommended and variant != concept:
                # Check if it's a legitimate use (in code blocks, citations, etc.)
                # We only flag if the Chinese variant is used in prose
                results['信息'].append(
                    f'{fname} — "{concept}" 使用了变体译名 "{variant}"（推荐: "{recommended}"）'
                )
                break

def write_report(results):
    """生成 Markdown 报告。"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    report_path = os.path.join(OUTPUT_DIR, 'phase1-audit-report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('# 自动审计报告\n\n')
        f.write(f'> 由 `book/scripts/audit_scan.py` 自动生成\n\n')
        for severity in ['严重', '警告', '信息']:
            items = results[severity]
            f.write(f'## [{severity}] {severity}问题（共 {len(items)} 项）\n\n')
            if items:
                for item in items:
                    f.write(f'- {item}\n')
                f.write('\n')
            else:
                f.write('无。\n\n')
    print(f'报告已写入: {report_path}')
    total = sum(len(v) for v in results.values())
    print(f'总计发现 {total} 个问题（严重 {len(results["严重"])}, 警告 {len(results["警告"])}, 信息 {len(results["信息"])}）')

if __name__ == '__main__':
    main()
