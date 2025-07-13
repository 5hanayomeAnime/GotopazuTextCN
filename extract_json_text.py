import json

# 你要提取的字段
TARGET_KEYS = {
    "title", "body", "linkText", "val1", "notice", "introduce", "popText",
    "name", "description", "detailDescription", "text", "effectLabel"
}

# text字段下的子字段
TEXT_SUB_KEYS = {
    "BoostGroupText", "TeamBattleText", "LotteryText", "MemberText", "SkillText", "ItemText", "RewardText",
    "ChapterText", "CardText", "HomeText", "QuestText", "PuzzleText", "GachaText", "BgmText",
    "ChallengeText", "ShopText", "PlayerTitleText", "StoryText", "LoginText", "FeatureText", "MemberLikabilitytext"
}

# 保存提取结果的 dict
flattened_output = {}
counter = 1  # 计数器

def extract_text(obj, path=""):
    global counter
    if isinstance(obj, dict):
        for k, v in obj.items():
            current_path = f"{path}.{k}" if path else k

            # 普通字段
            if k in TARGET_KEYS and k != "text" and isinstance(v, str):
                flattened_output[f"path[{counter}]"] = current_path
                counter += 1
                flattened_output[f"text[{counter}]"] = v
                counter += 1

            # 特殊处理 text 的子字段
            elif k == "text" and isinstance(v, dict):
                for sub_k, sub_v in v.items():
                    sub_path = f"{current_path}.{sub_k}"
                    if sub_k in TEXT_SUB_KEYS and isinstance(sub_v, str):
                        flattened_output[f"path[{counter}]"] = sub_path
                        counter += 1
                        flattened_output[f"text[{counter}]"] = sub_v
                        counter += 1
                    elif isinstance(sub_v, (dict, list)):
                        extract_text(sub_v, sub_path)

            else:
                extract_text(v, current_path)

    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            extract_text(item, f"{path}[{i}]")

# 主函数
def main(input_path, output_path="output.json"):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    extract_text(data)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([flattened_output], f, ensure_ascii=False, indent=2)

    print(f"提取完成，共 {len(flattened_output)//2} 条文案，已保存到 {output_path}")

# 示例调用
if __name__ == "__main__":
    main("./jpmaster.json")  # 替换为你的 JSON 文件路径
