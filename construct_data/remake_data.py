import json
import random

# 读取 generated_data_pairs.json 文件
with open('generated_data_pairs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 构建新的数据集
dataset = []

# 遍历每个数据对
for entry in data:
    # 提取问题和正样本
    query = entry["question"]
    pos = [entry["answerable_string"]]

    # 获取所有的 answerable_string，作为负样本候选（排除当前的正样本）
    all_strings = [e["answerable_string"] for e in data if e["answerable_string"] != entry["answerable_string"]]

    # 随机选择 10 条负样本
    neg = random.sample(all_strings, 10)

    # 构造数据对
    new_entry = {
        "query": query,
        "pos": pos,
        "neg": neg
    }

    # 将新的数据条目添加到数据集中
    dataset.append(new_entry)

# 划分训练集和测试集（比例 9:1）
train_size = int(len(dataset) * 0.9)
train_data = dataset[:train_size]
test_data = dataset[train_size:]

# # 保存训练集
# with open('train_data.json', 'w', encoding='utf-8') as f:
#     json.dump(train_data, f, ensure_ascii=False, indent=4)

# 保存测试集
with open('test_data.json', 'w', encoding='utf-8') as f:
    json.dump(test_data, f, ensure_ascii=False, indent=4)

# 将数据写入 train_data.jsonl 文件
with open('train_data.jsonl', 'w', encoding='utf-8') as f:
    for sample in train_data:
        json.dump(sample, f, ensure_ascii=False)  # 将每个样本写入一行
        f.write('\n')  # 每个样本后添加换行符

print("Train and test datasets have been successfully generated and saved as 'train_data.json' and 'test_data.json'.")