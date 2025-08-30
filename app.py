from flask import Flask, render_template
import json
import re
import html

app = Flask(__name__)

# 全新的、极简的、更安全的文本预处理器
def preprocess_latex(text):
    # 1. 处理None和类型问题
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    if not text.strip():
        return ""
        
    # 2. 清理 HTML 标签和 [[...]] 标记
    #   - 常见块级标签替换为换行；其余标签移除
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'</?(div|p|center|section|article|ol|ul|li|table|tr|td|th|thead|tbody|tfoot)[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    
    # 更精确的HTML标签匹配，避免误删数学表达式中的不等号
    # 只匹配真正的HTML标签格式：<tagname...> 或 </tagname>
    text = re.sub(r'</?[a-zA-Z][a-zA-Z0-9]*[^<>]*>', '', text)
    
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)

    # 3. 不压缩反斜杠（json.loads 已经做过一次转义），避免破坏 LaTeX 的 \\ 与命令

    # 4. 处理 \hdots -> \ldots
    text = re.sub(r'\\hdots', r'\\ldots', text)

    # 5. 在 "Show that it is" 前断行，并把其后的“裸”表达式包成 $...$
    text = re.sub(r'(\$[^$]*\$)\s*(Show that it is)', r'\1\n\n\2', text)
    def _wrap_show(line: str) -> str:
        m = re.search(r'(Show that it is)\s*([^\n]+)', line)
        if not m:
            return line
        lhs, rhs = m.group(1), m.group(2).strip()
        if re.search(r'(\$|\\\(|\\\[)', rhs):
            return line
        rhs = re.sub(r'\.*\s*$', '', rhs)
        return line[:m.start()] + f"{lhs} $" + rhs + "$" + line[m.end():]
    text = '\n'.join(_wrap_show(ln) for ln in text.splitlines())

    # 6. 升级/包裹常见块环境（array/tabular/align/cases 等）
    def ensure_blocks(s: str) -> str:
        envs = ['align', 'align*', 'cases', 'array', 'matrix', 'pmatrix', 'bmatrix', 'Bmatrix', 'vmatrix', 'Vmatrix', 'smallmatrix', 'tabular']
        # 先将 $\begin{env}...\end{env}$ 升级为 $$...$$
        for env in envs:
            s = re.sub(rf'\$\s*(\\begin\{{{env}\}}[\s\S]*?\\end\{{{env}\}})\s*\$', r'$$\1$$', s)
        # 再把裸露块用 $$ 包裹，但避免处于 $/\( /\[ 环境内的情况
        for env in envs:
            pattern = rf'(\\begin\{{{env}\}}[\s\S]*?\\end\{{{env}\}})'
            def wrap_if_needed(m: re.Match) -> str:
                block = m.group(1)
                start = m.start(1)
                end = m.end(1)
                # 扩大搜索范围到前后10个字符，更准确地检测是否在数学环境内
                left_context = s[max(0, start-10):start]
                right_context = s[end:end+10]
                # 检查是否在 \[...\] 或 \(...\) 或 $...$ 内
                if (left_context.count('\\[') > left_context.count('\\]') or
                    left_context.count('\\(') > left_context.count('\\)') or
                    left_context.count('$') % 2 == 1):
                    return block
                return '$$' + block + '$$'
            s = re.sub(pattern, wrap_if_needed, s)
        return s
    text = ensure_blocks(text)

    # 7. 针对 162：移除被误加在 cases 周围的 $$
    text = re.sub(r'(=|:)\s*\$\$\s*(\\begin\{cases\}[\s\S]*?\\end\{cases\})\s*\$\$', r' \2', text)

    # 8. 合并多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text

# 读取并解析JSONL文件
def load_data():
    data = []
    with open('processed_minif2f.jsonl', 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            try:
                item = json.loads(line)
                
                # 使用全新的预处理器
                item['informal_stmt'] = preprocess_latex(item.get('informal_stmt', ''))
                item['informal_proof'] = preprocess_latex(item.get('informal_proof', ''))
                
                data.append(item)
            except (json.JSONDecodeError, Exception) as e:
                print(f"Error processing line {line_num}: {e}")
                continue
    return data

# 将数据分为valid和test两部分
data = load_data()
valid_data = data[:244]  # index 1-244
test_data = data[244:]   # index 245-488，显示为test-1到test-244

# 为test数据重新编号，用于显示
for i, item in enumerate(test_data):
    item['display_index'] = i + 1

# 为valid数据添加display_index
for i, item in enumerate(valid_data):
    item['display_index'] = i + 1

@app.route('/')
def index():
    return render_template('index.html', valid_data=valid_data, test_data=test_data)

if __name__ == '__main__':
    app.run(debug=False, port=5000)
