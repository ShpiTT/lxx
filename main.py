import json
import os
import re
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class LocalKnowledgeBaseQA:
    def __init__(self, knowledge_file: str = None, knowledge_dict: Dict = None):
        """
        初始化本地知识库问答系统

        Args:
            knowledge_file: 知识库JSON文件路径
            knowledge_dict: 直接传入的知识库字典数据
        """
        self.knowledge_base = {}  # 知识库
        self.vectorizer = TfidfVectorizer(tokenizer=self._tokenize)
        self.kb_vectors = None  # 知识库的向量表示
        self.kb_ids = []  # 知识库条目的ID

        if knowledge_file:
            self.load_from_json(knowledge_file)
        elif knowledge_dict:
            self.knowledge_base = knowledge_dict
            self._build_index()
        else:
            # 默认使用空知识库
            self.knowledge_base = {}

    def _tokenize(self, text: str) -> List[str]:
        """分词函数，使用jieba分词"""
        return list(jieba.cut(text))

    def load_from_json(self, file_path: str) -> None:
        """从JSON文件加载知识库"""
        if not os.path.exists(file_path):
            print(f"错误：文件 {file_path} 不存在")
            return

        print(f"正在从文件 {file_path} 加载知识库...")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
            self._build_index()
            print(f"成功加载知识库，包含 {len(self.kb_ids)} 个知识条目")
        except Exception as e:
            print(f"加载失败: {e}")

    def _build_index(self) -> None:
        """构建知识库的向量索引"""
        documents = []
        self.kb_ids = []

        for question_id, question_data in self.knowledge_base.items():
            for evidence_id, evidence_data in question_data.get('evidences', {}).items():
                # 使用证据文本构建索引
                evidence_text = evidence_data.get('evidence', '')
                if evidence_text:
                    documents.append(evidence_text)
                    self.kb_ids.append(f"{question_id}#{evidence_id}")

        if documents:
            self.kb_vectors = self.vectorizer.fit_transform(documents)
        else:
            self.kb_vectors = None

    def search_knowledge(self, query: str, top_n: int = 3) -> List[Dict]:
        """
        在知识库中搜索与查询相关的知识条目

        Args:
            query: 查询文本
            top_n: 返回的结果数量

        Returns:
            相关知识条目的列表，每个条目包含id、content、source和相似度得分
        """
        # 修复矩阵判断逻辑
        if self.kb_vectors is None or self.kb_vectors.size == 0 or not query.strip():
            return []

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.kb_vectors).flatten()

        # 获取相似度最高的top_n个索引
        top_indices = similarities.argsort()[::-1][:top_n]
        results = []

        for idx in top_indices:
            if similarities[idx] > 0:  # 只返回有一定相似度的结果
                full_id = self.kb_ids[idx]
                question_id, evidence_id = full_id.split('#', 1)

                # 获取问题和证据信息
                question_data = self.knowledge_base.get(question_id, {})
                evidence_data = question_data.get('evidences', {}).get(evidence_id, {})

                results.append({
                    "id": full_id,
                    "question": question_data.get('question', ''),
                    "answer": evidence_data.get('answer', []),
                    "evidence": evidence_data.get('evidence', ''),
                    "score": float(similarities[idx])  # 转换为普通float以便JSON序列化
                })

        return results

    def generate_answer(self, query: str, top_n: int = 3) -> Dict:
        """
        基于知识库生成问题的答案

        Args:
            query: 用户问题
            top_n: 参考的知识条目数量

        Returns:
            包含答案和参考知识的字典
        """
        results = self.search_knowledge(query, top_n)

        if not results:
            return {
                "answer": "抱歉，没有找到相关信息。",
                "references": []
            }

        # 提取第一个匹配结果的答案
        best_result = results[0]
        answers = best_result.get('answer', [])

        # 如果答案列表中包含"no_answer"，则返回默认提示
        if "no_answer" in answers:
            return {
                "answer": "抱歉，没有找到相关答案。",
                "references": [
                    {
                        "question": best_result.get('question', ''),
                        "evidence": best_result.get('evidence', ''),
                        "score": best_result.get('score', 0)
                    }
                ]
            }

        # 优先使用第一个答案，否则使用证据的第一段落
        if answers:
            final_answer = answers[0]
        else:
            evidence = best_result.get('evidence', '')
            paragraphs = re.split(r'\n\s*\n', evidence.strip())
            final_answer = paragraphs[0] if paragraphs else evidence

        return {
            "answer": final_answer,
            "references": [
                {
                    "question": best_result.get('question', ''),
                    "evidence": best_result.get('evidence', ''),
                    "score": best_result.get('score', 0)
                }
            ]
        }


# 交互式命令行界面
def main():
    print("===== 本地知识库问答系统 =====")

    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    knowledge_file = os.path.join(current_dir, "knowledge_base.json")

    # 检查知识库文件是否存在
    if os.path.exists(knowledge_file):
        print(f"找到知识库文件: {knowledge_file}")
        print("正在加载知识库...")
        qa_system = LocalKnowledgeBaseQA(knowledge_file=knowledge_file)
    else:
        print(f"未找到知识库文件: {knowledge_file}")
        print("1. 从其他JSON文件加载知识库")
        print("2. 使用示例知识库")
        choice = input("请选择: ")

        if choice == '1':
            file_path = input("请输入知识库JSON文件路径: ")
            qa_system = LocalKnowledgeBaseQA(knowledge_file=file_path)
        else:
            # 使用示例知识库
            sample_knowledge = {
                "Q_DAY_001": {
                    "question": "一天有多少小时",
                    "evidences": {
                        "Q_DAY_001#00": {
                            "answer": ["24小时"],
                            "evidence": "地球自转一周的时间约为24小时，这是一天的时间长度来源。"
                        }
                    }
                },
                "Q_DAY_002": {
                    "question": "一年有多少个月",
                    "evidences": {
                        "Q_DAY_002#00": {
                            "answer": ["12个月"],
                            "evidence": "公历中一年分为12个月，每月天数从28天到31天不等。"
                        }
                    }
                },
                "Q_DAY_003": {
                    "question": "水的沸点是多少摄氏度",
                    "evidences": {
                        "Q_DAY_003#00": {
                            "answer": ["100摄氏度"],
                            "evidence": "在标准大气压下，纯净水的沸点为100摄氏度，海拔升高沸点会降低。"
                        }
                    }
                }
            }
            qa_system = LocalKnowledgeBaseQA(knowledge_dict=sample_knowledge)
            print("已加载示例知识库")

    while True:
        print("\n===== 操作菜单 =====")
        print("1. 提问")
        print("2. 搜索知识库")
        print("3. 查看知识库统计信息")
        print("q. 退出")

        cmd = input("请选择操作: ")

        if cmd == '1':
            question = input("请输入您的问题: ")
            if not question.strip():
                continue

            answer_data = qa_system.generate_answer(question)

            print("\n答案:")
            print(answer_data["answer"])

            if answer_data["references"]:
                print("\n参考资料:")
                for i, ref in enumerate(answer_data["references"], 1):
                    print(f"{i}. [{ref['question']}] {ref['evidence'][:100]}... (相似度: {ref['score']:.2f})")

        elif cmd == '2':
            keyword = input("请输入搜索关键词: ")
            if not keyword.strip():
                continue

            results = qa_system.search_knowledge(keyword, top_n=5)

            if results:
                print(f"\n找到 {len(results)} 个相关知识条目:")
                for i, result in enumerate(results, 1):
                    print(f"{i}. [{result['question']}] {result['evidence'][:100]}... (相似度: {result['score']:.2f})")
            else:
                print("没有找到相关知识")

        elif cmd == '3':
            # 统计信息
            total_questions = len(qa_system.knowledge_base)
            total_evidences = len(qa_system.kb_ids)

            print("\n知识库统计信息:")
            print(f"- 问题数量: {total_questions}")
            print(f"- 证据数量: {total_evidences}")

        elif cmd.lower() == 'q':
            break

        else:
            print("无效的选择，请重新输入")


if __name__ == "__main__":
    # 确保中文分词正常工作
    jieba.setLogLevel(jieba.logging.INFO)
    main()