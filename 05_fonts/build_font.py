import os, re, glob

# find chinese characters in files
file_ext = ["html", "js", "ejs", "css", "py", "md", "txt"]
input_font_path = os.path.join(os.path.expanduser("~"), "Downloads", "LXGWWenKaiMono-Regular.ttf")
output_font_path = os.path.join(".", "public", "assets", "main-font-subset.woff")

from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

# subset font
def subset_font(input_font_path, output_font_path, text, flavor="woff"):
    font = TTFont(input_font_path)
    options = Options()
    options.flavor = flavor
    options.text = text
    subsetter = Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    os.makedirs(os.path.dirname(output_font_path), exist_ok=True)
    font.save(output_font_path)

def collect_chinese_chars_in_directory(
    dir_path=".", 
    extensions=file_ext, 
    encoding="utf-8", 
    recursive=True,
    pattern=r"[\u4E00-\u9FFF]+"
):
    """
    在指定目录下，遍历所有具有指定后缀的文件，收集其中出现的中文字符
    
    :param dir_path: 要搜索的根目录(默认为当前目录 ".").
    :param extensions: 要匹配的文件扩展名元组或列表，如 ("txt", "html", "md")
    :param encoding: 打开文件时使用的编码(默认为 "utf-8")
    :param recursive: 是否递归扫描子目录(默认 True)
    :param pattern: 用于匹配中文字符的正则表达式，默认为基本汉字区 [\u4E00-\u9FFF]
                    如果需要扩展区，可自行修改为:
                    r"[\u4E00-\u9FFF\u3400-\u4DBF\u20000-\u2A6DF\uF900-\uFAFF]+"
    :return: 字符串 包含所有去重且按Unicode排序的中文字符
    """
    
    # 编译正则，提高重复匹配效率
    chinese_pattern = re.compile(pattern)
    
    # 用于收集所有中文字符(去重)
    all_chinese_chars = set()

    # 遍历指定扩展名
    for ext in extensions:
        # 如果 recursive=True，则使用 **/ 形式遍历子目录
        # 如果 recursive=False，可以改为 os.path.join(dir_path, f"*.{ext}")
        if recursive:
            file_pattern = os.path.join(dir_path, f"**/*.{ext}")
        else:
            file_pattern = os.path.join(dir_path, f"*.{ext}")

        # 使用 glob.iglob 获取匹配到的文件列表
        for file_path in glob.iglob(file_pattern, recursive=recursive):
            if os.path.isfile(file_path):
                try:
                    # 逐个文件读取内容
                    with open(file_path, "r", encoding=encoding) as f:
                        content = f.read()
                    
                    # 匹配所有连续的中文片段
                    matches = chinese_pattern.findall(content)
                    for m in matches:
                        # m 可能是一个包含若干字符的片段
                        # 将片段拆分为单个字符并放入 set 去重
                        all_chinese_chars.update(m)
                
                except UnicodeDecodeError:
                    # 如果文件不是指定的编码，可以根据情况自行处理或跳过
                    print(f"[Warn] 无法用 {encoding} 编码读取文件：{file_path}")
                except Exception as e:
                    print(f"[Error] 读取文件 {file_path} 发生错误：{e}")

    # 把收集到的所有字符按Unicode顺序排序并拼成一个字符串
    chinese_str = "".join(sorted(all_chinese_chars))
    return chinese_str

if __name__ == "__main__":
    result_str = collect_chinese_chars_in_directory(
        dir_path=".", 
        extensions=file_ext,
        recursive=True,
        pattern=r"[\u4E00-\u9FFF\u3400-\u4DBF\u20000-\u2A6DF\uF900-\uFAFF\u3000-\u303F\uFF00-\uFFEF\u0020-\u007F]+"
    )
    """
    \u4E00-\u9FFF          # 基本汉字
    \u3400-\u4DBF          # CJK 扩展 A
    \u20000-\u2A6DF        # CJK 扩展 B 等更多扩展
    \uF900-\uFAFF          # CJK 兼容汉字
    \u3000-\u303F          # CJK 符号和标点
    \uFF00-\uFFEF          # 半角及全角形状
    \u0020-\u007F          # 半角英文字符 (仅 ASCII 可打印部分)
    """

    subset_font(input_font_path, output_font_path, result_str, "woff")

    # write to file
    with open("font_subset.txt", "w", encoding="utf-8") as f:
        f.write(result_str)

    print(f"build font {output_font_path} success, {len(result_str)} chars")