import json
import sys
import re

def find_existing_ids(data):
    """查找所有现有的问题ID"""
    existing_ids = []
    for key in data.keys():
        if isinstance(key, str):
            existing_ids.append(key)
    return existing_ids

def generate_new_id(existing_ids, base_prefix="Q_HEALTH_"):
    """生成不重复的新ID"""
    # 提取现有编号中的数字部分
    existing_numbers = []
    for id_str in existing_ids:
        match = re.match(rf"{base_prefix}(\d+)", id_str)
        if match:
            existing_numbers.append(int(match.group(1)))
    
    # 生成新编号：现有最大编号+1
    new_number = max(existing_numbers) + 1 if existing_numbers else 1
    return f"{base_prefix}{new_number:03d}"

def update_evidence_ids(data, old_id, new_id):
    """更新证据ID中的问题ID部分"""
    if old_id in data:
        question = data[old_id]
        if "evidences" in question:
            evidences = question["evidences"]
            new_evidences = {}
            for evidence_id, evidence_data in evidences.items():
                # 替换证据ID中的问题ID部分
                new_evidence_id = evidence_id.replace(old_id, new_id)
                new_evidences[new_evidence_id] = evidence_data
            question["evidences"] = new_evidences

def renumber_question(input_file, output_file, old_id, new_id=None):
    """
    重新编号JSON数据中的特定问题条目
    
    参数:
    input_file (str): 输入JSON文件路径
    output_file (str): 输出JSON文件路径
    old_id (str): 要修改的旧问题ID
    new_id (str, optional): 新的问题ID，如果为None则自动生成
    """
    try:
        # 读取JSON文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查旧ID是否存在
        if old_id not in data:
            print(f"错误: 找不到问题ID '{old_id}'")
            return False
        
        # 如果没有提供新ID，自动生成一个不重复的
        if new_id is None:
            existing_ids = find_existing_ids(data)
            new_id = generate_new_id(existing_ids)
            print(f"自动生成新ID: {new_id}")
        
        # 检查新ID是否已存在
        if new_id in data:
            print(f"错误: 新ID '{new_id}' 已存在")
            return False
        
        # 更新证据ID
        update_evidence_ids(data, old_id, new_id)
        
        # 获取对应的数据
        question_data = data[old_id]
        
        # 移除旧ID并添加新ID
        del data[old_id]
        data[new_id] = question_data
        
        # 保存修改后的JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"成功将问题ID '{old_id}' 重命名为 '{new_id}'")
        return True
    
    except FileNotFoundError:
        print(f"错误: 文件 '{input_file}' 不存在")
        return False
    except json.JSONDecodeError:
        print(f"错误: 文件 '{input_file}' 不是有效的JSON格式")
        return False
    except Exception as e:
        print(f"发生未知错误: {e}")
        return False

def main():
    """主函数，处理命令行参数并执行重新编号操作"""
    # 如果没有提供参数，使用默认值
    if len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
        print("使用方法:")
        print("  python json_renumber.py [输入文件] [输出文件] [旧ID] [新ID]")
        print("  如果不提供参数，将处理当前目录下的'knowledge_base.json'文件")
        print("  如果不提供新ID，将自动生成一个不重复的ID")
        sys.exit(0)
    
    input_file = sys.argv[1] if len(sys.argv) > 1 else "knowledge_base.json"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "knowledge_base_new.json"
    old_id = sys.argv[3] if len(sys.argv) > 3 else "Q_HEALTH_043"
    new_id = sys.argv[4] if len(sys.argv) > 4 else None
    
    print(f"处理文件: {input_file}")
    print(f"旧ID: {old_id}")
    if new_id:
        print(f"新ID: {new_id}")
    else:
        print("新ID: 自动生成")
    
    success = renumber_question(input_file, output_file, old_id, new_id)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()