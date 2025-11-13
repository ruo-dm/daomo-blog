import os
import re

def get_posts_folder():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    posts_dir = os.path.join(script_dir, 'source', '_posts')
    return posts_dir

def find_md_files_by_name(name, root_dir):
    matches = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file == f'{name}.md':
                matches.append(os.path.join(root, file))
    return matches

def convert_image_links_in_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # ✅ 匹配两种图片语法：
    # 1. Markdown 语法：![alt](./dir/image.png)
    # 2. HTML 语法：<img src="./dir/image.png" ...>
    pattern = re.compile(
        r'(?:!\[[^\]]*\]\(\s*(?:\./)?([^)\s]+?\.(?:png|jpg|jpeg|gif|webp|svg))(?:\s+(?:"[^"]*"|\'[^\']*\'))?\s*\))'
        r'|(?:<img[^>]*src=["\'](?:\./)?([^"\']+?\.(?:png|jpg|jpeg|gif|webp|svg))["\'][^>]*>)',
        re.IGNORECASE
    )

    def repl(m):
        # m.group(1) 对应 markdown 图片路径
        # m.group(2) 对应 html 图片路径
        path = m.group(1) or m.group(2)
        filename = os.path.basename(path)
        return '{% asset_img ' + filename + ' %}'

    new_content, n_subs = pattern.subn(repl, content)

    if n_subs > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'✅ 已处理: {file_path} （共替换 {n_subs} 处图片链接）')
    else:
        print(f'⚠️ 无需修改: {file_path} （未匹配到图片链接）')

def main():
    posts_dir = get_posts_folder()
    if not os.path.exists(posts_dir):
        print(f"❌ 未找到目录: {posts_dir}")
        return

    name = input("请输入要处理的 Markdown 文件名（不含路径和扩展名，例如 a）：").strip()
    matches = find_md_files_by_name(name, posts_dir)

    if not matches:
        print("❌ 在 source/_posts 中未找到任何匹配的 .md 文件。")
        return

    if len(matches) == 1:
        confirm = input(f"只找到一个 {name}.md 文件：{matches[0]}\n确认执行操作？Y/N：").strip().lower()
        if confirm == 'y':
            convert_image_links_in_md(matches[0])
        else:
            print("🚫 操作已取消。")
    else:
        print(f"🔍 找到多个 {name}.md 文件，请选择要处理的文件路径：")
        for i, path in enumerate(matches):
            print(f"{i + 1}. {path}")
        choice = input("请输入要处理的文件相对路径（例如 source/_posts/xxx.md）：").strip()
        full_choice = os.path.join(os.getcwd(), choice)
        if full_choice in matches:
            convert_image_links_in_md(full_choice)
        else:
            print("❌ 输入路径无效，操作取消。")

if __name__ == '__main__':
    main()
