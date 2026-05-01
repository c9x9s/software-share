#!/usr/bin/env python3
"""
批量修改所有详情页文件中的第一人称和主观表述，改为客观陈述。
"""
import re
import os
import glob

def delete_score_lines(html):
    """删除所有评分/推荐指数行 (含<p>标签包围)"""
    # Pattern 1: <strong>评分：...</strong> on its own in a <p> block
    html = re.sub(
        r'<p>\s*\n?\s*<strong>评分：[^<]*</strong>\s*\n?\s*</p>',
        '',
        html
    )
    # Pattern 2: <strong>推荐指数：...</strong> in <p>
    html = re.sub(
        r'<p>\s*\n?\s*<strong>推荐指数：[^<]*</strong>\s*\n?\s*</p>',
        '',
        html
    )
    # Pattern 3: standalone <strong>评分：... or <strong>推荐指数：... without <p>
    html = re.sub(
        r'<strong>评分：[^<]*</strong>\s*',
        '',
        html
    )
    html = re.sub(
        r'<strong>推荐指数：[^<]*</strong>\s*',
        '',
        html
    )
    return html

def replace_section_titles(html):
    """替换章节标题"""
    replacements = [
        ('我的使用场景', '使用场景'),
        ('我的刷题方法', '刷题方法'),
        ('我的练习体验', '练习体验'),
        ('我的学习体验', '学习体验'),
        ('我的必装插件', '推荐插件'),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    return html

def rewrite_first_person(html):
    """重写第一人称/主观表述为客观描述"""
    lines = html.split('\n')
    new_lines = []
    
    for line in lines:
        original = line
        new_line = line
        
        # 只处理在标签内容中的文字 (<p>, <h2>, <li>, <h4>, <div class="highlight-box"> 等)
        # 跳过纯标签行、CSS、JS、meta等
        
        # 检查是否包含可见内容 (在 > 和 < 之间)
        # 更精确：只处理在 HTML 标签内的文本
        
        # === 批量替换模式 ===
        
        # 1. "我选择/我用了/我用过/我把它..." → 去掉第一人称
        # "我选择 Obsidian 的原因很简单" → "选择 Obsidian 的原因很简单"
        new_line = re.sub(r'(?<=[>。，；：])我选择', '选择', new_line)
        new_line = re.sub(r'^我选择', '选择', new_line)
        
        # "我用它来做技术文档整理" → "可用于做技术文档整理"
        new_line = re.sub(r'我用它来', '可用于', new_line)
        new_line = re.sub(r'我用它做', '可用于', new_line)
        
        # "我用过 Sketch" → "使用过 Sketch"
        new_line = re.sub(r'我用过', '使用过', new_line)
        new_line = re.sub(r'我用了', '使用了', new_line)
        
        # "我来做" → "可用于"
        new_line = re.sub(r'我来做', '可用于', new_line)
        
        # "我来说" → 去掉或改为"来说"
        # 特殊: "对我来说" → "对使用者来说"
        new_line = re.sub(r'对我来说', '对使用者来说', new_line)
        new_line = re.sub(r'对我自己来说', '对使用者来说', new_line)
        
        # "我每天打开" → "日常打开" / "用户每天打开"
        new_line = re.sub(r'我每天打开', '日常打开', new_line)
        new_line = re.sub(r'我每天', '每天', new_line)
        
        # "我把..." → "可将..."
        new_line = re.sub(r'我把', '可将', new_line)
        
        # "我的个人博客" → "个人博客"
        new_line = re.sub(r'我的个人博客', '个人博客', new_line)
        
        # "我从 X 开始" → "从 X 开始"
        new_line = re.sub(r'(?<=[>。，；])我从', '从', new_line)
        new_line = re.sub(r'^我是从', '从', new_line)
        
        # "我在 X 上完成了" → "在 X 上完成了"
        new_line = re.sub(r'(?<=[>。，；])我在', '在', new_line)
        new_line = re.sub(r'^我在', '在', new_line)
        
        # "我的真实感受" → "真实感受" (when after other words)
        new_line = re.sub(r'我的真实感受', '真实使用体验', new_line)
        
        # "我的职业生涯" → "职业生涯"
        new_line = re.sub(r'我的职业生涯', '职业生涯', new_line)
        
        # "我用它来做" → "可用于做"
        new_line = re.sub(r'我用它来做', '可用于做', new_line)
        
        # "我用它来" → "可用于"
        new_line = re.sub(r'我用它来', '可用于', new_line)
        
        # "我都在..." → "都在..."
        new_line = re.sub(r'(?<=[>，。；])我都在', '都在', new_line)
        
        # "我推荐" → "适合"
        new_line = re.sub(r'我推荐', '适合推荐给', new_line)
        
        # 2. "我的主力" → "核心"
        new_line = re.sub(r'我的主力', '核心', new_line)
        
        # "我的最爱" / "我最爱" → "推荐" / "广受喜爱"
        new_line = re.sub(r'我的最爱', '推荐', new_line)
        new_line = re.sub(r'我最爱的功能', '推荐功能', new_line)
        new_line = re.sub(r'我最爱', '深受喜爱', new_line)
        
        # "我必装" → "推荐"
        new_line = re.sub(r'我必装', '推荐', new_line)
        
        # "我电脑上不可或缺的" → "电脑上不可或缺的" (keep as-is but remove first person lead-in)
        # Actually this pattern is "XXX 是我电脑上不可或缺的" → keep objective
        new_line = re.sub(r'是我电脑上不可或缺的', '是电脑上不可或缺的', new_line)
        
        # "我离不开" / "让我离不开" → "常用" / "核心"
        new_line = re.sub(r'让我离不开的功能', '核心功能', new_line)
        new_line = re.sub(r'让我每天都离不开的功能', '日常高频功能', new_line)
        new_line = re.sub(r'让我每天在用', '日常高频使用', new_line)
        new_line = re.sub(r'让我离不开', '成为日常必用', new_line)
        new_line = re.sub(r'我离不开', '是日常工作中离不开的', new_line)
        new_line = re.sub(r'根本离不开', '是必不可少的', new_line)
        
        # "我安利" / "安利" → "推荐"
        new_line = re.sub(r'安利', '推荐', new_line)
        
        # "我强烈建议" → "建议"
        new_line = re.sub(r'我强烈建议', '建议', new_line)
        
        # "让我眼前一亮" → "表现令人印象深刻"
        new_line = re.sub(r'让我眼前一亮', '表现令人印象深刻', new_line)
        
        # "让我爱不释手" → "非常实用" / "备受喜爱"
        new_line = re.sub(r'让我爱不释手的功能', '备受喜爱的功能', new_line)
        new_line = re.sub(r'让我爱不释手', '非常实用', new_line)
        
        # "让我惊叹" → "令人惊叹"
        new_line = re.sub(r'让我惊叹', '令人惊叹', new_line)
        
        # "让我很安心" → "更让人安心"
        new_line = re.sub(r'让我很安心', '让人更安心', new_line)
        
        # "让我佩服" → "令人佩服"
        new_line = re.sub(r'让我佩服', '令人佩服', new_line)
        
        # "让我喜欢" → "深受欢迎"
        new_line = re.sub(r'让我喜欢', '深受欢迎', new_line)
        
        # "我最喜欢" → "其核心亮点"
        new_line = re.sub(r'我最喜欢', '其核心亮点是', new_line)
        
        # "最适合我" → "非常适合"
        new_line = re.sub(r'最适合我', '非常适合', new_line)
        
        # "我最常用" → "常用"
        new_line = re.sub(r'我最常用的功能', '常用功能', new_line)
        new_line = re.sub(r'我最常用', '常用', new_line)
        
        # "我被它" → "它被"
        new_line = re.sub(r'我被它', '它被', new_line)
        
        # "我装了几十个" → "可安装数十个"
        new_line = re.sub(r'我装了几十个', '支持安装数十个', new_line)
        
        # "我所在团队" → "团队"
        new_line = re.sub(r'我所在团队', '团队', new_line)
        new_line = re.sub(r'我的团队', '团队', new_line)
        
        # "我仍然推荐它" → "仍然值得推荐"
        new_line = re.sub(r'我仍然推荐它', '它仍然值得推荐', new_line)
        
        # "我的使用感受" → "使用感受"
        new_line = re.sub(r'我的使用感受', '使用感受', new_line)
        
        # "我的所有内容" → "所有内容"
        new_line = re.sub(r'我的所有内容', '所有内容', new_line)
        
        # "我粉丝" → "用户"
        new_line = re.sub(r'我的粉丝', '关注的用户', new_line)
        
        # "我劝你别用" → "不建议使用"
        # "我劝你" → "建议"
        
        # "我的日常" → "日常"
        new_line = re.sub(r'我的日常', '日常', new_line)
        
        # "我还在用它" → "仍在广泛使用"
        new_line = re.sub(r'我还在用它', '仍在广泛使用中', new_line)
        
        # "我在 B 站学过" → "可在 B 站学习"
        new_line = re.sub(r'我在 B 站学过', '可在 B 站学习', new_line)
        
        # "我从事" → "从事"
        new_line = re.sub(r'(?<=[>。，；])我从事', '从事', new_line)
        
        # "我经常" → "通常"
        new_line = re.sub(r'(?<=[>。，；])我经常', '通常', new_line)
        new_line = re.sub(r'^我经常', '通常', new_line)
        
        # "我喜欢" → "适合"
        # Be careful: only replace "我喜欢" when it's about user preference
        # In "如果你喜欢" - keep as is
        new_line = re.sub(r'(?<=[，。；])我喜欢', '适合喜欢', new_line)
        new_line = re.sub(r'^我喜欢', '适合喜欢', new_line)
        # But NOT "如果你喜欢" → fix if we broke it
        new_line = re.sub(r'如果你适合喜欢', '如果你喜欢', new_line)
        
        # "我感觉" → "体验"
        new_line = re.sub(r'我感觉', '整体体验是', new_line)
        new_line = re.sub(r'我的感受', '使用体验', new_line)
        
        # "我的数据" → "数据"
        new_line = re.sub(r'我的数据', '数据', new_line)
        
        # "我的笔记" → "笔记"
        new_line = re.sub(r'我的笔记', '笔记', new_line)
        
        # "我的密码" → "密码"
        new_line = re.sub(r'我的密码', '密码', new_line)
        
        # "我的账号" → "账号"
        new_line = re.sub(r'我的账号', '账号', new_line)
        
        # "我的项目" → "项目"
        new_line = re.sub(r'我的项目', '项目', new_line)
        
        # 3. "让人觉得惊叹" / "让人惊叹" → 去掉或改为客观
        new_line = re.sub(r'让人惊叹', '令人印象深刻', new_line)
        new_line = re.sub(r'惊艳到我了', '表现出色', new_line)
        new_line = re.sub(r'让我惊艳', '令人惊艳', new_line)
        new_line = re.sub(r'最让我惊艳', '最令人惊艳', new_line)
        new_line = re.sub(r'最让我满意', '非常令人满意', new_line)
        new_line = re.sub(r'惊艳', '出色', new_line)
        
        # 4. "首选" → keep but make objective where personal
        # "我的首选" → "首选"
        new_line = re.sub(r'我的首选', '首选', new_line)
        # "我首选" → "首选"
        new_line = re.sub(r'我首选', '首选', new_line)
        # But "依然是首选" or "是首选" - keep
        
        # 5. "强烈推荐" → "适合"
        new_line = re.sub(r'强烈推荐', '适合', new_line)
        new_line = re.sub(r'强烈建议', '建议', new_line)
        
        # 6. "不得不" → handle context
        new_line = re.sub(r'不得不推荐', '值得推荐', new_line)
        new_line = re.sub(r'不得不承认', '不得不承认', new_line)  # can keep if third person
        # "不得不提" → "值得提及"
        new_line = re.sub(r'不得不提', '值得提及', new_line)
        
        # 7. "必须装" → "必备"
        new_line = re.sub(r'必须装', '必备', new_line)
        new_line = re.sub(r'必装', '必备', new_line)
        new_line = re.sub(r'必上', '值得使用', new_line)
        
        # 8. "如果你..." → 改为客观条件描述
        # Keep "如果用户..." or restructure
        # "如果你喜欢" → "适合喜欢...的用户"
        # But this is complex, handle specific cases:
        # "如果你做前端开发" → "适合前端开发"
        # Actually, "如果你" can stay in many cases as it's addressing the reader (not first person)
        # But requirement says to change it to objective condition description
        # Let's handle common patterns:
        new_line = re.sub(r'如果你做 <strong>', '适合 <strong>', new_line)
        new_line = re.sub(r'如果你做（', '适合（', new_line)
        new_line = re.sub(r'如果你做', '适合', new_line)
        new_line = re.sub(r'如果你需要', '适合需要', new_line)
        new_line = re.sub(r'如果你还在用', '对于还在使用', new_line)
        new_line = re.sub(r'如果你还没有', '对于还没有', new_line)
        new_line = re.sub(r'如果你对', '适合对', new_line)
        new_line = re.sub(r'如果你运营', '适合运营', new_line)
        new_line = re.sub(r'如果你使用', '适合使用', new_line)
        new_line = re.sub(r'如果你是', '适合', new_line)
        new_line = re.sub(r'如果你要', '适合需要', new_line)
        new_line = re.sub(r'如果你习惯', '适合习惯', new_line)
        new_line = re.sub(r'如果你在乎', '适合注重', new_line)
        new_line = re.sub(r'如果你想', '适合想要', new_line)
        new_line = re.sub(r'如果你主要', '适合主要', new_line)
        new_line = re.sub(r'如果你在', '适合正在', new_line)
        new_line = re.sub(r'如果你经常', '适合经常', new_line)
        new_line = re.sub(r'如果用户', '适合', new_line)
        
        # Fix any "适合如果" artifacts
        new_line = re.sub(r'适合如果', '如果', new_line)
        
        # 9. "让我" overall cleanup (remaining)
        new_line = re.sub(r'让我', '让用户', new_line)
        new_line = re.sub(r'给我', '给用户', new_line)
        
        # 10. Remove remaining standalone "我" at start of sentences in content
        # Only within tag content area (between > and <)
        # Simple case: "我" after punctuation or at beginning of tag content
        new_line = re.sub(r'。我', '。', new_line)
        new_line = re.sub(r'！我', '！', new_line)
        new_line = re.sub(r'？我', '？', new_line)
        new_line = re.sub(r'；我', '；', new_line)
        new_line = re.sub(r'：我', '：', new_line)
        
        # 11. "我们" → 去掉或改为"用户"
        new_line = re.sub(r'我们', '用户', new_line)
        
        # 12. "你是" in context of "如果你是" already handled, but also:
        # "你就能" → "就能"
        new_line = re.sub(r'你就能', '就能', new_line)
        # "你的代码" → "代码"
        new_line = re.sub(r'(?<=[，。；、])你的', '', new_line)
        
        # 13. Clean up artifacts: double spaces, empty sentences
        new_line = re.sub(r'  ', ' ', new_line)
        new_line = re.sub(r'\.。', '。', new_line)
        new_line = re.sub(r'，，', '，', new_line)
        new_line = re.sub(r'。。', '。', new_line)
        new_line = re.sub(r'；。', '。', new_line)
        new_line = re.sub(r'，。', '。', new_line)
        
        # Fix: "适合喜欢 <strong>" → keep proper
        # Fix: "适合适合" → "适合"
        new_line = re.sub(r'适合适合', '适合', new_line)
        
        # Fix punctuation spacing
        new_line = re.sub(r'>。', '>。', new_line)  # ensure tag closing before period
        
        new_lines.append(new_line)
    
    return '\n'.join(new_lines)


def final_check_and_fix(html):
    """Final pass to catch any remaining first-person in content tags"""
    lines = html.split('\n')
    new_lines = []
    
    for line in lines:
        # Only process lines that have visible tag content (between > and <)
        # Check if this line contains text between HTML tags
        # Simple approach: if line contains > text < pattern
        new_line = line
        
        # Catch any remaining "我" that appears between > and < (tag content)
        # But preserve "我" in HTML attributes like title="我的..."
        
        # Use regex to find text between > and < on the same line
        def replace_my_in_content(match):
            prefix = match.group(1)
            content = match.group(2)
            suffix = match.group(3)
            
            # Skip if it's inside an HTML attribute
            # Already handled by the regex ensuring we're in tag content
            
            # Replace 我 at start or after punctuation
            content = re.sub(r'(^|[。，；：！？、\s])我($|[。，；：！？、\s])', r'\1\2', content)
            content = re.sub(r'(^|[。，；：！？、\s])我的($|[。，；：！？、\s])', r'\1\2', content)
            
            # Remove standalone 我
            content = re.sub(r'\b我\b', '', content)
            
            return prefix + content + suffix
        
        # 匹配 >内容< 模式
        new_line = re.sub(r'(>)([^<]*)(<)', replace_my_in_content, new_line)
        
        # Remove 我的 in content between tags
        new_line = re.sub(r'(>)([^<]*?)我的([^<]*?)(<)', 
                         lambda m: m.group(1) + m.group(2) + m.group(3) + m.group(4), new_line)
        
        new_lines.append(new_line)
    
    return '\n'.join(new_lines)


def clean_artifacts(html):
    """Clean up any artifacts from the replacements"""
    # Remove empty paragraphs
    html = re.sub(r'<p>\s*</p>', '', html)
    
    # Remove double blank lines
    html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)
    
    # Clean up leading/trailing whitespace on lines
    lines = html.split('\n')
    lines = [line.rstrip() for line in lines]
    html = '\n'.join(lines)
    
    return html


def process_file(filepath):
    """Process a single HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Step 1: Delete score/recommendation lines
    content = delete_score_lines(content)
    
    # Step 2: Replace section titles
    content = replace_section_titles(content)
    
    # Step 3: Rewrite first-person/subjective content
    content = rewrite_first_person(content)
    
    # Step 4: Final check
    content = final_check_and_fix(content)
    
    # Step 5: Clean artifacts
    content = clean_artifacts(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, "modified"
    else:
        return False, "unchanged"


def main():
    software_dir = '/mnt/c/Users/zc199/software-share/software/'
    html_files = sorted(glob.glob(os.path.join(software_dir, '*.html')))
    
    print(f"Found {len(html_files)} HTML files")
    
    modified_count = 0
    unchanged_count = 0
    
    for filepath in html_files:
        basename = os.path.basename(filepath)
        if basename == '_template.html':
            print(f"  Skipping template: {basename}")
            continue
        
        try:
            changed, status = process_file(filepath)
            if changed:
                modified_count += 1
                print(f"  ✓ Modified: {basename}")
            else:
                unchanged_count += 1
                print(f"  - Unchanged: {basename}")
        except Exception as e:
            print(f"  ✗ Error processing {basename}: {e}")
    
    print(f"\nDone! Modified: {modified_count}, Unchanged: {unchanged_count}")


if __name__ == '__main__':
    main()
