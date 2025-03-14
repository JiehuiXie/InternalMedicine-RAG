import json
import random

# 读取原始 JSON 文件
with open(r'F:\CODE\项目2\project2\LightRAG\dickens\graph_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(len(data['nodes']), len(data['edges']))  # 输出原始数据中的节点数和边数
# 从 nodes 和 edges 中随机选择 500 个
nodes_sample = random.sample(data['nodes'], 500)  # 从 nodes 中随机选择 500 个
edges_sample = random.sample(data['edges'], 500)  # 从 edges 中随机选择 500 个

# 创建新的数据结构
new_data = {
    'nodes': nodes_sample,
    'edges': edges_sample
}

# 将新的数据保存到新的 JSON 文件
with open('sampled_data.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)

print("500 nodes and 500 edges have been successfully sampled and saved to 'sampled_data.json'.")
