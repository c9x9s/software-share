#!/usr/bin/env python3
"""
Second pass: Fix remaining first-person/subjective expressions in HTML files.
"""
import re
import os
import glob

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_line = line
        
        # Only process within visible text content (between > and <)
        # We'll process the entire line with targeted replacements
        
        # === Comprehensive replacements for all remaining patterns ===
        
        replacements = [
            # 1. "我选择" at start or after punctuation
            (r'我选择', '选择'),
            # 2. "我是从" at start of content
            (r'我是从', '从'),
            # 3. "我在" at start of content text
            (r'^我在', '在'),
            # 4. "我用" at start of content (after >)
            (r'>我用', '>使用'),
            (r'>我用了', '>使用了'),
            (r'>我用过', '>使用过'),
            (r'>我用它', '>可将其'),
            # 5. "我把" 
            (r'>我把', '>可将'),
            # 6. "我的" - most common
            (r'我的编码体验', '编码体验'),
            (r'我的 Windows 使用体验', 'Windows 使用体验'),
            (r'我的拖延症', '拖延症'),
            (r'我的所有想象', '所有想象'),
            (r'我的项目', '项目'),
            (r'我的个人网站', '个人网站'),
            (r'我的密码', '密码'),
            (r'我的笔记', '笔记'),
            (r'我的数据', '数据'),
            (r'我的账号', '账号'),
            (r'我的编码', '编码'),
            (r'我的学习', '学习'),
            (r'我的团队', '团队'),
            (r'我的全部', '全部'),
            # More generic "我的" removal in tag content
            (r'(?<=[>，。；：、\s])我的(?=[^<]*?<)', ''),
            # But preserve "我的" in quoted strings and attributes
            # Actually handle "数据在我手里" carefully
            (r'数据在我手里', '数据在用户自己手里'),
            # 7. "我最爱" / "我最喜欢" / "我最常用" 
            (r'我最喜欢', '其亮点是'),
            (r'我最常用', '常用'),
            (r'我最爱', '深受喜爱的'),
            (r'最爱的功能', '核心功能'),
            # 8. "我见过最好用的" → 极好用的
            (r'是我见过最好用的', '是极好用的'),
            # 9. "我电脑上" → "电脑上"
            (r'是我每台电脑必备的', '是每台电脑必备的'),
            (r'我每台电脑', '每台电脑'),
            (r'我的电脑上', '电脑上'),
            # 10. "让我" various
            (r'让我改变', '改变'),
            (r'让我重新爱上', '让开发者重新爱上'),
            (r'让我很安心', '让人安心'),
            (r'让我现在很难', '让用户现在很难'),
            (r'让我佩服', '令人佩服'),
            (r'让我满意', '令人满意'),
            (r'让我坚持', '帮助坚持'),
            # 11. "吸引我的是" → "突出特点"
            (r'最吸引我的是', '突出特点是'),
            # 12. "我找到" → "可以找到"
            (r'我找到', '可以找到'),
            # 13. "我才发现" → "可以发现"
            (r'我才发现', '可以发现'),
            # 14. "我所有" → "所有"
            (r'我所有', '所有'),
            # 15. "我把自己" → "可将"
            (r'我把自己', '可将'),
            # 16. "我还在用" → "还在用"
            (r'我还在用', '还在用'),
            # 17. "我用了" → "用了"
            (r'我用了', '使用了'),
            # 18. "我用来" → "可用于"
            (r'我用来', '可用于'),
            # 19. "我使用" → "使用"
            (r'我使用', '使用'),
            # 20. "我现在" → "现在"
            (r'我现在', '现在'),
            (r'^我现在', '现在'),
            # 21. "让我" (generic)
            (r'(?<=[，。；：\s])让我', '让用户'),
            # 22. "给我" 
            (r'给我', '给用户'),
            # 23. "我团队" → "团队"
            (r'我团队', '团队'),
            # 24. "我把它" → "可将其"
            (r'我把它', '可将其'),
            # 25. "我已经" → "已经"
            (r'我已经', '已经'),
            # 26. "我是" at content start
            (r'^我是', ''),
            # 27. "我最近" → "近期"
            (r'我最近', '近期'),
            # 28. "我每天" → "每天"
            (r'我每天', '每天'),
            # 29. "我一直" → "一直"
            (r'我一直', '一直'),
            # 30. "我从" → "从"
            (r'^我从', '从'),
            (r'我从', '从'),  # in middle of line too
            # 31. "我" as standalone after punctuation in tag content
            (r'(?<=[。，；：])我(?=[^<])', ''),
            (r'(?<=[。，；：]\s)我(?=[^<])', ''),  # with space after punctuation
            (r'^[ \t]*我(?=[^<])', ''),  # at line start with whitespace
            (r'^[ \t]*我在', '在'),
            (r'^[ \t]*我用', '使用'),
            (r'^[ \t]*我是', ''),
            # 32. "你" cleanup in certain contexts
            (r'适合你需要', '适合需要'),
            (r'适合你适合', '适合'),
            # 33. Phrases with 你 that should be objective
            (r'让你发现', '帮助发现'),
            (r'让你知道', '可以了解'),
            (r'让你感觉', '带来'),
            (r'让你打开', '打开'),
            (r'你的知识', '知识'),
            (r'你的代码', '代码'),
            (r'你的数据', '数据'),
            # 34. Clean up "你是" in non-conditional contexts
            # 35. "你怎么" → "如何"
            # 36. "你就能" → "就能"
            (r'你就能', '就能'),
            # 37. Remove "你的" after punctuation
            (r'(?<=[，。；：、])你的', ''),
            # 38. "能让你" → "能让"
            (r'能让你', '能让'),
            # 39. "我们" → "用户"
            (r'我们', '用户'),
            # 40. Clean up artifacts from previous replacements
            (r'  ', ' '),
            (r'的的', '的'),
            (r'。。', '。'),
            (r'，，', '，'),
            (r'。。', '。'),
            (r'是是', '是'),
            (r'适合适合', '适合'),
            (r'变得让用户得', '变得'),
            # 41. "让我" at line start (after >)
            (r'>让我', '>让用户'),
            # 42. Additional specific phrases from bilibili
            (r'把我"已收藏"当笔记本用', '将\"已收藏\"当作笔记本使用'),
            (r'"我在 B 站学 XX"', '\"在 B 站学习 XX\"'),
            (r'在 B 站学 XX', '在 B 站学习各种内容'),
            # 43. "我走过的" → "走过的"
            (r'我走过的', '走过的'),
            # 44. "我最近沉迷" → "近期备受关注"
            (r'我最近沉迷', '近期备受关注'),
            # 45. "陪我走过" → "历经"
            (r'陪伴我走过了近十年', '历经近十年'),
            (r'陪着我走过来', '沉淀多年'),
            # 46. "我每天都" → "每天都"
            (r'我每天都', '每天都'),
            # 47. From vscode: "改变了我的编码体验"
            (r'了我的编码体验', '了编码体验'),
            # 48. From blender: "满足了我对" → "满足了对"
            (r'满足了我对', '满足了对'),
            # 49. "我平时" → "平时"
            (r'我平时', '平时'),
            # 50. "我朋友" → "身边用户"
            (r'我朋友', '身边用户'),
            (r'我身边的朋友', '周围用户'),
            # 51. "我还" → "还"
            (r'(?<=[>，。；])我还', '还'),
            # 52. "我也是" → "也是"
            (r'我也是', '也是'),
            # 53. "我也可以" → '也可以'
            (r'我也可以', '也可以'),
            # 54. "我主要" → "主要"
            (r'我主要', '主要'),
            # 55. "我经常" → "经常"
            (r'我经常', '经常'),
            # 56. "我曾经" → "曾经"
            (r'我曾经', '曾经'),
            # 57. "我的确是" → "的确是"
            (r'我的确是', '的确是'),
            # 58. "我现在" surviving
            (r'(?<=[>。，！？])我现在', '现在'),
            # 59. Clean "你" at start of new sentences
            (r'(?<=[。，])你(?=[^<]*<)', '用户'),
            # 60. "你就" → "就"
            (r'(?<=[，。])你就', '就'),
            # 61. Fix any remaining
            (r'(?<=[>])我(?=[^<])', ''),
        ]
        
        for pattern, replacement in replacements:
            new_line = re.sub(pattern, replacement, new_line)
        
        # Final cleanup: remove leftover standalone 我 between tags
        # Only when "我" appears between > and <
        def clean_remaining_my(match):
            prefix = match.group(1)
            content = match.group(2)
            suffix = match.group(3)
            # Remove 我 that appears alone or after punctuation
            content = re.sub(r'我', '', content)
            return prefix + content + suffix
        
        new_line = re.sub(r'(>)([^<]*?我[^<]*?)(<)', clean_remaining_my, new_line)
        
        new_lines.append(new_line)
    
    content = '\n'.join(new_lines)
    
    # Clean up empty paragraphs and double blank lines
    content = re.sub(r'<p>\s*</p>', '', content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    software_dir = '/mnt/c/Users/zc199/software-share/software/'
    html_files = sorted(glob.glob(os.path.join(software_dir, '*.html')))
    
    fixed_count = 0
    for filepath in html_files:
        basename = os.path.basename(filepath)
        if basename == '_template.html':
            continue
        if fix_file(filepath):
            fixed_count += 1
            print(f"  ✓ Fixed: {basename}")
    
    print(f"\nSecond pass complete! Fixed: {fixed_count} files")

if __name__ == '__main__':
    main()
