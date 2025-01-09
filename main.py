import os
import json
import re



def folder_exec(path,config):
    for idx, name in enumerate(os.listdir(path)):
        cuerrent_path = os.path.join(path, name)
        if os.path.isdir(cuerrent_path):
            if is_chinese(name):
                new_folder_name = f"{idx + 1:06d}"  # 001, 002, ...
                new_folder_path = os.path.join(path, new_folder_name)
                os.rename(cuerrent_path, new_folder_path)
                update_json_url(config, f'/{name}/', f'/{new_folder_name}/')
            else :
                new_folder_path = cuerrent_path
                
            folder_exec(new_folder_path,config)
        
        if os.path.isfile(cuerrent_path) and is_chinese(name):
            new_file_name = f"{idx + 1:06d}{os.path.splitext(name)[1]}"  # 001.svg, 002.svg, ...
            new_file_path = os.path.join(path, new_file_name)
            # 重命名文件
            os.rename(cuerrent_path, new_file_path)
            update_json_url(config, f'{name}', f'{new_file_name}')

    
    # 保存更新后的 JSON 配置文件
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print("JSON 配置文件已更新！")



def update_json_url(config, old_name, new_name):
    """
    更新 JSON 配置文件中的 url 字段。
    :param config: JSON 配置数据
    :param old_name: 旧名称（文件夹或文件）
    :param new_name: 新名称（文件夹或文件）
    :param old_folder_name: 旧文件夹名称（如果是文件）
    :param new_folder_name: 新文件夹名称（如果是文件）
    """
    print(f"更新 JSON 配置文件中的 url 字段：{old_name} -> {new_name}")
    for category in config:
        for item in category["items"]:
            if old_name is not None:
                pattern = re.compile(re.escape(old_name))
                if "url" in item:
                    if pattern.search(item["url"]):
                        print(f"更新 JSON 配置文件中的 url 字段：{item['url']} -> {pattern.sub(new_name, item['url'])}")
                        item["url"] = pattern.sub(new_name, item["url"])
                if "image" in item:
                    if pattern.search(item["image"]):
                        print(f"更新 JSON 配置文件中的 image 字段：{item['image']} -> {pattern.sub(new_name, item['image'])}")
                        item["image"] = pattern.sub(new_name, item["image"])

                if "blurb" in item:
                    if pattern.search(item["blurb"]):
                        print(f"更新 JSON 配置文件中的 blurb 字段：{item['blurb']} -> {pattern.sub(new_name, item['blurb'])}")
                        item["blurb"] = pattern.sub(new_name, item["blurb"])

def is_chinese(text):
    """
    判断字符串是否包含中文字符。
    :param text: 输入的字符串
    :return: True（包含中文） / False（不包含中文）
    """
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

if __name__ == "__main__":
    aaa = [
            {
                "root_dir":"images/doodle_material",
                "config_path":"data/doodle_materials.json"
            },
            {
                "root_dir":"images/layer_material",
                "config_path":"data/layer_materials.json"
            },
            {
                "root_dir":"fonts",
                "config_path":"data/fonts.json"
            }
        ]

    for dd in aaa:
        config_path = dd["config_path"]
        root_dir = dd["root_dir"]
        print(config_path)
        print(root_dir)
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        folder_exec(root_dir,config)
        print("重命名完成！")