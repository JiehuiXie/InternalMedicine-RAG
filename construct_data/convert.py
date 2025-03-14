import json

# 读取 sampled_data.json 文件
with open('sampled_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 创建一个新的列表来存储所有的样本字符串（包括节点和关系）
all_strings = []

# 处理 nodes 数据：拼接 id, entity_type 和 description
for node in data['nodes']:
    node_str = f"{node['id']} {node['entity_type']} {node['description']}"
    all_strings.append(node_str)

# 处理 edges 数据：拼接 source, target, description 和 keywords
for edge in data['edges']:
    edge_str = f"{edge['source']} {edge['target']} {edge['description']} {edge['keywords']}"
    all_strings.append(edge_str)

# 创建一个新的字典，包含所有样本字符串
new_data = {
    'samples': all_strings
}

# 将新的数据保存到新的 JSON 文件
with open('all_samples_strings.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)

print("500 nodes and 500 edges have been successfully processed and saved to 'all_samples_strings.json'.")
