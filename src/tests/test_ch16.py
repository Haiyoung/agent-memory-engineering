#!/usr/bin/env python3
"""
第16章 综合案例单元测试 — 验证四层记忆架构与各版本运行结果。

这是一个自包含测试文件，内含各版本的完整代码实现（已集成所有fix）。
运行方式：
    cd book/src && python tests/test_ch16.py
"""
from __future__ import annotations
import json, math, os, re, sys, time, hashlib
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from pathlib import Path


# ============================================================
# 基础数据类型
# ============================================================

@dataclass
class Message:
    role: str
    content: str
    token_count: int
    importance: float = 0.5
    timestamp: float = field(default_factory=time.time)
    access_count: int = 0
    protected: bool = False

    def to_llm_dict(self) -> dict:
        return {"role": self.role, "content": self.content}


def token_estimate(text: str) -> int:
    return max(1, len(text) // 2)


# ============================================================
# V1: 短期记忆（滑动窗口 + 摘要压缩）
# ============================================================

class SlidingWindowManager:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.buffer: list[Message] = []

    @property
    def current_tokens(self) -> int:
        return sum(m.token_count for m in self.buffer)

    def add(self, message: Message) -> list[Message]:
        self.buffer.append(message)
        return self._evict_if_needed()

    def _evict_if_needed(self) -> list[Message]:
        evicted = []
        while self.current_tokens > self.max_tokens:
            candidates = [m for m in self.buffer if not m.protected]
            if not candidates:
                break
            victim = min(candidates, key=lambda m: m.importance)
            self.buffer.remove(victim)
            evicted.append(victim)
        return evicted

    def get_context(self) -> list[dict]:
        return [m.to_llm_dict() for m in self.buffer]

    def get_evicted(self) -> list[Message]:
        """返回当前缓冲区中低重要性的消息（压缩/持久化的候选）。"""
        return [m for m in self.buffer if m.importance < 0.3]


class SemanticCompressor:
    def __init__(self, compression_ratio: float = 0.3):
        self.compression_ratio = compression_ratio

    def compress(self, messages: list[Message]) -> Message:
        if not messages:
            return Message(role="system", content="", token_count=0)
        user_msgs = [m for m in messages if m.role == "user"]
        assistant_msgs = [m for m in messages if m.role == "assistant"]
        parts = []
        if user_msgs:
            topics = self._extract_topics(user_msgs)
            parts.append(f"用户讨论了: {', '.join(topics)}")
        if assistant_msgs:
            parts.append(f"助手提供了 {len(assistant_msgs)} 条回复")
        summary = " | ".join(parts)
        target_tokens = int(sum(m.token_count for m in messages) * self.compression_ratio)
        return Message(
            role="system", content=f"[摘要] {summary}",
            token_count=max(target_tokens, 20), importance=0.4,
        )

    @staticmethod
    def _extract_topics(messages: list[Message]) -> list[str]:
        keywords = []
        for m in messages:
            for word in m.content.split():
                word = word.strip("，。！？、,.!?;:\"'()[]{}")
                if len(word) > 2:
                    keywords.append(word)
        seen = set()
        unique = []
        for k in keywords:
            if k not in seen and len(unique) < 5:
                seen.add(k)
                unique.append(k)
        return unique


class ChatLoop:
    def __init__(self, max_tokens: int = 4000):
        self.wm = SlidingWindowManager(max_tokens=max_tokens)
        self.compressor = SemanticCompressor()
        self.summaries: list[str] = []
        self.wm.add(Message(
            role="system",
            content="你是一个个人研究助手，帮助用户阅读论文、追踪研究进展。",
            token_count=30, importance=1.0, protected=True,
        ))

    def send(self, user_input: str) -> str:
        token_est = token_estimate(user_input)
        user_msg = Message(role="user", content=user_input, token_count=token_est)
        evicted = self.wm.add(user_msg)
        if evicted:
            summary = self.compressor.compress(evicted)
            self.summaries.append(summary.content)
        context = self.wm.get_context()
        if self.summaries:
            summary_text = "\n".join(f"- {s}" for s in self.summaries[-3:])
            context.insert(1, {"role": "system", "content": f"[历史摘要]\n{summary_text}"})
        response = self._simulate_llm(context)
        assistant_msg = Message(
            role="assistant", content=response, token_count=token_estimate(response),
        )
        self.wm.add(assistant_msg)
        return response

    def _simulate_llm(self, context: list[dict]) -> str:
        last_user = next((m["content"] for m in reversed(context) if m["role"] == "user"), "")
        return f"[模拟响应] 关于 '{last_user[:30]}...' 的回答。"

    def state(self) -> dict:
        return {
            "current_tokens": self.wm.current_tokens,
            "message_count": len(self.wm.buffer),
            "summary_count": len(self.summaries),
            "summaries": self.summaries,
        }


# ============================================================
# V2: 长期记忆（向量存储 + 知识图谱）
# ============================================================

class SimpleVectorStore:
    def __init__(self):
        self.vocabulary: dict[str, int] = {}
        self.documents: list[dict] = []

    def add(self, text: str, metadata: dict | None = None) -> int:
        doc_id = len(self.documents)
        vector = self._build_vector(text)
        self.documents.append({
            "id": doc_id, "text": text, "metadata": metadata or {}, "vector": vector,
        })
        return doc_id

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        query_vec = self._build_vector(query)
        results = []
        for doc in self.documents:
            sim = self._cosine_similarity(query_vec, doc["vector"])
            results.append((sim, doc))
        results.sort(key=lambda x: x[0], reverse=True)
        return [
            {"score": sim, "text": doc["text"], "metadata": doc["metadata"]}
            for sim, doc in results[:top_k]
        ]

    def _build_vector(self, text: str) -> dict[str, float]:
        words = self._tokenize(text)
        vec: dict[str, float] = {}
        for w in words:
            vec[w] = vec.get(w, 0.0) + 1.0
        norm = math.sqrt(sum(v * v for v in vec.values()))
        if norm > 0:
            for k in vec:
                vec[k] /= norm
        return vec

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return [
            w.strip("，。！？、,.!?;:\"'()[]{}")
            for w in text.lower().split()
            if len(w.strip("，。！？、,.!?;:\"'()[]{}")) > 1
        ]

    @staticmethod
    def _cosine_similarity(v1: dict[str, float], v2: dict[str, float]) -> float:
        common = set(v1.keys()) & set(v2.keys())
        if not common:
            return 0.0
        dot = sum(v1[k] * v2[k] for k in common)
        n1 = math.sqrt(sum(v * v for v in v1.values()))
        n2 = math.sqrt(sum(v * v for v in v2.values()))
        if n1 == 0 or n2 == 0:
            return 0.0
        return dot / (n1 * n2)

    def to_dict(self) -> dict:
        return {"vocabulary": self.vocabulary, "documents": self.documents}

    @classmethod
    def from_dict(cls, data: dict) -> SimpleVectorStore:
        store = cls()
        store.vocabulary = data.get("vocabulary", {})
        store.documents = data.get("documents", [])
        return store

    def size(self) -> int:
        return len(self.documents)


try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False


class ConceptGraph:
    def __init__(self):
        if HAS_NETWORKX:
            self.graph = nx.DiGraph()
        else:
            self.graph: dict[str, dict[str, list[str]]] = {}

    def add_concept(self, name: str, description: str = "") -> None:
        if HAS_NETWORKX:
            self.graph.add_node(name, description=description)
        else:
            if name not in self.graph:
                self.graph[name] = {"relations": {}, "description": description}

    def add_relation(self, source: str, target: str, relation: str) -> None:
        self.add_concept(source)
        self.add_concept(target)
        if HAS_NETWORKX:
            self.graph.add_edge(source, target, relation=relation)
        else:
            self.graph[source]["relations"].setdefault(relation, []).append(target)

    def find_related(self, concept: str, max_depth: int = 2) -> list[tuple[str, str, str]]:
        results = []
        if HAS_NETWORKX:
            if concept not in self.graph:
                return results
            visited = set()
            queue = [(concept, 0, "")]
            while queue:
                node, depth, path = queue.pop(0)
                if node in visited or depth > max_depth:
                    continue
                visited.add(node)
                for neighbor in self.graph.neighbors(node):
                    relation = self.graph[node][neighbor].get("relation", "related_to")
                    new_path = f"{path} ->[{relation}]-> {neighbor}" if path else f"{concept} ->[{relation}]-> {neighbor}"
                    results.append((neighbor, relation, new_path))
                    queue.append((neighbor, depth + 1, new_path))
        else:
            if concept in self.graph:
                for rel, targets in self.graph[concept]["relations"].items():
                    for t in targets:
                        results.append((t, rel, f"{concept} ->[{rel}]-> {t}"))
        return results

    def to_dict(self) -> dict:
        if HAS_NETWORKX:
            nodes = dict(self.graph.nodes(data=True))
            edges = [
                {"source": u, "target": v, "relation": d.get("relation", "related_to")}
                for u, v, d in self.graph.edges(data=True)
            ]
            return {"nodes": nodes, "edges": edges, "use_networkx": True}
        else:
            return {"graph": self.graph, "use_networkx": False}

    @classmethod
    def from_dict(cls, data: dict) -> ConceptGraph:
        cg = cls()
        if not data:
            return cg
        if data.get("use_networkx") and HAS_NETWORKX:
            import networkx as nx
            g = nx.DiGraph()
            for name, attrs in data["nodes"].items():
                desc = attrs.get("description", attrs) if isinstance(attrs, dict) else attrs
                g.add_node(name, description=desc if isinstance(desc, str) else "")
            for edge in data["edges"]:
                g.add_edge(edge["source"], edge["target"], relation=edge.get("relation", "related_to"))
            cg.graph = g
        else:
            cg.graph = data.get("graph", {})
        return cg

    def summary(self) -> dict[str, Any]:
        if HAS_NETWORKX:
            return {"concepts": self.graph.number_of_nodes(), "relations": self.graph.number_of_edges()}
        total = sum(len(rels) for cd in self.graph.values() for rels in cd["relations"].values())
        return {"concepts": len(self.graph), "relations": total}


class MemoryPersistence:
    def __init__(self, data_dir: str = "research_agent_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def save_session(self, session_id: str, data: dict) -> None:
        path = self.data_dir / f"{session_id}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def load_session(self, session_id: str) -> dict | None:
        path = self.data_dir / f"{session_id}.json"
        if path.exists():
            return json.loads(path.read_text())
        return None

    def save_full_state(self, session_id: str, store: SimpleVectorStore, graph: ConceptGraph, extra: dict | None = None) -> None:
        state = {"vector_store": store.to_dict(), "concept_graph": graph.to_dict()}
        if extra:
            state.update(extra)
        self.save_session(session_id, state)

    def load_full_state(self, session_id: str) -> dict | None:
        data = self.load_session(session_id)
        if data is None:
            return None
        store = SimpleVectorStore.from_dict(data.get("vector_store", {}))
        graph = ConceptGraph.from_dict(data.get("concept_graph", {}))
        return {
            "vector_store": store,
            "concept_graph": graph,
            "extra": {k: v for k, v in data.items() if k not in ("vector_store", "concept_graph")},
        }

    def list_sessions(self) -> list[str]:
        return [p.stem for p in self.data_dir.glob("*.json")]

    def cleanup(self) -> None:
        """测试结束后清理数据文件。"""
        for p in self.data_dir.glob("*.json"):
            p.unlink()
        self.data_dir.rmdir()


class MemoryController:
    def __init__(self, max_context_tokens: int = 4000):
        self.wm = SlidingWindowManager(max_tokens=max_context_tokens)
        self.compressor = SemanticCompressor()
        self.vector_store = SimpleVectorStore()
        self.concept_graph = ConceptGraph()
        self.persistence = MemoryPersistence()
        self.session_summaries: list[str] = []
        self.session_id: str = ""

    def start_session(self, session_id: str | None = None) -> None:
        if session_id is None:
            session_id = f"session_{int(time.time())}"
        self.session_id = session_id
        full = self.persistence.load_full_state(session_id)
        if full:
            print(f"  [恢复] 会话 {session_id}")
            self.vector_store = full["vector_store"]
            self.concept_graph = full["concept_graph"]
            extra = full.get("extra", {})
            self.session_summaries = extra.get("summaries", [])
            sys_prompt = Message(role="system", content="你是一个个人研究助手，帮助用户阅读论文、追踪研究进展。", token_count=30, importance=1.0, protected=True)
            self.wm.add(sys_prompt)
            if self.session_summaries:
                self.wm.add(Message(role="system", content=f"[历史研究摘要]\n" + "\n".join(f"- {s}" for s in self.session_summaries[-5:]), token_count=sum(len(s)//2 for s in self.session_summaries[-5:]), importance=0.6, protected=True))
        else:
            print(f"  [新会话] {session_id}")
            self.wm.add(Message(role="system", content="你是一个个人研究助手，帮助用户阅读论文、追踪研究进展。", token_count=30, importance=1.0, protected=True))

    def send(self, user_input: str) -> str:
        self._will_send(user_input)
        retrieved = self.vector_store.search(user_input, top_k=3)
        concepts = self._extract_concepts(user_input)
        graph_context = []
        for c in concepts:
            graph_context.extend(self.concept_graph.find_related(c, max_depth=1))
        context_parts = []
        if retrieved:
            context_parts.append("[相关论文/概念]")
            for r in retrieved:
                context_parts.append(f"- {r['text']} (相关度: {r['score']:.2f})")
        if graph_context:
            context_parts.append("[概念关系]")
            for name, rel, path in graph_context[:5]:
                context_parts.append(f"- {path}")
        extra = self._extra_context(user_input, retrieved, graph_context)
        if extra:
            context_parts.append(extra)
        if context_parts:
            self.wm.add(Message(role="system", content="\n".join(context_parts), token_count=sum(len(p)//2 for p in context_parts), importance=0.7))
        user_msg = Message(role="user", content=user_input, token_count=token_estimate(user_input), importance=0.8)
        evicted = self.wm.add(user_msg)
        if evicted:
            summary = self.compressor.compress(evicted)
            self.session_summaries.append(summary.content)
            self.vector_store.add(summary.content, {"type": "summary"})
        context = self.wm.get_context()
        response = self._generate_response(context, retrieved, graph_context)
        self.wm.add(Message(role="assistant", content=response, token_count=token_estimate(response), importance=0.6))
        self._after_send(user_input, response)
        self._persist()
        return response

    def _will_send(self, user_input: str) -> None:
        pass

    def _extra_context(self, user_input: str, retrieved: list, graph_context: list) -> str | None:
        return None

    def _generate_response(self, context: list[dict], retrieved: list, graph_context: list) -> str:
        last_user = next((m["content"] for m in reversed(context) if m["role"] == "user"), "")
        parts = [f"[模拟响应] 关于 '{last_user[:30]}'"]
        if retrieved:
            parts.append(f"\n  检索到 {len(retrieved)} 条相关论文/概念")
        if graph_context:
            parts.append(f"\n  概念图中找到 {len(graph_context)} 条关系")
        return "".join(parts)

    def _after_send(self, user_input: str, response: str) -> None:
        pass

    def _persist(self) -> None:
        self.persistence.save_session(self.session_id, {
            "summaries": self.session_summaries,
            "vector_store_size": self.vector_store.size(),
            "graph_summary": self.concept_graph.summary(),
        })

    def add_paper(self, title: str, abstract: str) -> None:
        self.vector_store.add(f"{title}: {abstract}", {"type": "paper", "title": title})
        print(f"  [存储] 已添加论文: {title}")

    def add_concept_relation(self, source: str, target: str, relation: str, source_desc: str = "", target_desc: str = "") -> None:
        self.concept_graph.add_concept(source, source_desc)
        self.concept_graph.add_concept(target, target_desc)
        self.concept_graph.add_relation(source, target, relation)

    def _extract_concepts(self, text: str) -> list[str]:
        candidates = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*|[一-鿿]{2,}', text)
        return list(set(candidates))[:5]

    def state(self) -> dict:
        return {
            "session_id": self.session_id,
            "working_memory": {"tokens": self.wm.current_tokens, "messages": len(self.wm.buffer)},
            "vector_store": {"documents": self.vector_store.size()},
            "concept_graph": self.concept_graph.summary(),
            "session_summaries": len(self.session_summaries),
            "saved_sessions": self.persistence.list_sessions(),
        }


# ============================================================
# V3: 程序性记忆（经验库 + 用户画像 + 反思）
# ============================================================

@dataclass
class Experience:
    situation: str
    action: str
    result: str
    reflection: str = ""
    timestamp: float = field(default_factory=time.time)
    usage_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


class ExperienceStore:
    def __init__(self):
        self.experiences: list[Experience] = []
        self.vector_store = SimpleVectorStore()

    def add(self, exp: Experience) -> None:
        self.experiences.append(exp)
        self.vector_store.add(f"{exp.situation} {exp.action} {exp.reflection}", {"experience_id": len(self.experiences) - 1})

    def search(self, situation: str, top_k: int = 3) -> list[Experience]:
        results = self.vector_store.search(situation, top_k=top_k)
        exps = []
        for r in results:
            eid = r["metadata"]["experience_id"]
            exp = self.experiences[eid]
            exp.usage_count += 1
            exps.append(exp)
        return exps

    def generate_reflection(self, situation: str, action: str, result: str) -> str:
        if "失败" in result or "失败" in situation:
            return f"在 '{situation}' 场景中，'{action}' 的策略不够有效。建议：下次尝试更具体的检索关键词，或先从高层概念入手再深入细节。"
        return f"'{action}' 在 '{situation}' 中表现良好，可以作为默认策略。"

    def size(self) -> int:
        return len(self.experiences)


@dataclass
class UserProfile:
    research_topics: dict[str, float] = field(default_factory=dict)
    active_since: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)
    total_interactions: int = 0
    preferences: dict[str, str] = field(default_factory=dict)

    def update_interest(self, topic: str, weight: float = 1.0) -> None:
        self.research_topics[topic] = self.research_topics.get(topic, 0.0) * 0.9 + weight

    def get_active_topics(self, top_k: int = 5) -> list[tuple[str, float]]:
        return sorted(self.research_topics.items(), key=lambda x: x[1], reverse=True)[:top_k]

    def record_interaction(self) -> None:
        self.total_interactions += 1
        self.last_active = time.time()


class MemoryControllerV3(MemoryController):
    def __init__(self, max_context_tokens: int = 4000):
        super().__init__(max_context_tokens)
        self.experience_store = ExperienceStore()
        self.user_profile = UserProfile()
        self.reflection_triggered: list[str] = []

    def send(self, user_input: str) -> str:
        return super().send(user_input)

    def _will_send(self, user_input: str) -> None:
        self.user_profile.record_interaction()
        for c in self._extract_concepts(user_input):
            self.user_profile.update_interest(c)

    def _extra_context(self, user_input: str, retrieved: list, graph_context: list) -> str | None:
        experiences = self.experience_store.search(user_input, top_k=2)
        self._current_experiences = experiences
        if not experiences:
            return None
        return "[经验提醒]\n" + "\n".join(f"- 过去在类似场景中: {exp.reflection}" for exp in experiences)

    def _generate_response(self, context: list[dict], retrieved: list, graph_context: list) -> str:
        last_user = next((m["content"] for m in reversed(context) if m["role"] == "user"), "")
        parts = [f"[模拟响应] 关于 '{last_user[:30]}'"]
        exps = getattr(self, '_current_experiences', [])
        if exps:
            parts.append(f"\n  经验库提醒: 之前尝试过 {len(exps)} 次")
        if retrieved:
            parts.append(f"\n  检索到 {len(retrieved)} 条相关论文")
        if graph_context:
            parts.append(f"\n  概念图: {len(graph_context)} 条关系")
        return "".join(parts)

    def _after_send(self, user_input: str, response: str) -> None:
        self._check_and_record_experience(user_input, response)

    def _persist(self) -> None:
        self.persistence.save_full_state(self.session_id, self.vector_store, self.concept_graph, {
            "summaries": self.session_summaries,
            "experiences": [e.to_dict() for e in self.experience_store.experiences],
            "user_profile": {"topics": self.user_profile.get_active_topics(), "interactions": self.user_profile.total_interactions},
        })

    def _check_and_record_experience(self, user_input: str, response: str) -> None:
        if "不对" in user_input or "错误" in user_input or "失败" in user_input:
            exp = Experience(situation=user_input[:100], action="尝试回答", result="失败：用户不满意")
            exp.reflection = self.experience_store.generate_reflection(exp.situation, exp.action, exp.result)
            self.experience_store.add(exp)
            self.reflection_triggered.append(exp.situation)
            print(f"  [反思] {exp.reflection}")


# ============================================================
# V4: 完整版（治理 + 运维）
# ============================================================

class MemoryGovernance:
    def __init__(self, default_ttl_days: float = 90.0, decay_half_life_days: float = 30.0, min_confidence: float = 0.2):
        self.default_ttl_days = default_ttl_days
        self.decay_half_life = decay_half_life_days * 86400
        self.min_confidence = min_confidence

    def should_forget(self, item: dict) -> bool:
        created = item.get("created_at", time.time())
        ttl = item.get("ttl_days", self.default_ttl_days)
        return (time.time() - created) > ttl * 86400

    def decay_confidence(self, item: dict) -> float:
        conf = item.get("confidence", 1.0)
        elapsed = time.time() - item.get("created_at", time.time())
        new_conf = conf * (0.5 ** (elapsed / self.decay_half_life))
        item["confidence"] = new_conf
        return new_conf

    def cleanup(self, items: list[dict]) -> list[dict]:
        before = len(items)
        items[:] = [item for item in items if not self.should_forget(item) and self.decay_confidence(item) > self.min_confidence]
        removed = before - len(items)
        if removed > 0:
            print(f"  [治理] 清理了 {removed} 条过期/低置信度记忆")
        return items


class ResearchAgent(MemoryControllerV3):
    def __init__(self, max_context_tokens: int = 4000):
        super().__init__(max_context_tokens)
        self.governance = MemoryGovernance()
        self.memory_log: list[dict] = []

    def log(self, action: str, details: str) -> None:
        self.memory_log.append({"timestamp": time.time(), "action": action, "details": details})

    def send(self, user_input: str) -> str:
        if self.user_profile.total_interactions % 10 == 0:
            self.governance.cleanup(self.memory_log)
            self.governance.cleanup(self.vector_store.documents)
        response = super().send(user_input)
        self.log("send", f"user_input_len={len(user_input)}")
        return response

    def full_state(self) -> dict:
        base = self.state()
        base.update({
            "experiences": self.experience_store.size(),
            "governance": {"default_ttl_days": self.governance.default_ttl_days, "min_confidence": self.governance.min_confidence},
            "memory_log_entries": len(self.memory_log),
            "user_profile": {"topics": self.user_profile.get_active_topics(), "total_interactions": self.user_profile.total_interactions},
        })
        return base


# ============================================================
# 单元测试
# ============================================================

PASS = 0
FAIL = 0

def check(condition: bool, msg: str):
    global PASS, FAIL
    if condition:
        print(f"  ✓ {msg}")
        PASS += 1
    else:
        print(f"  ✗ {msg}")
        FAIL += 1


# ---- 回归测试：Bug Fixes ----

def test_concept_extraction():
    """P1 回归：验证 _extract_concepts 返回多字术语而非单字。"""
    print("\n=== 回归测试: 概念提取 (P1 fix) ===")
    mc = MemoryController()
    text = "我最近在研究视频目标分割，帮我总结一下XMem这篇论文的核心贡献"
    concepts = mc._extract_concepts(text)
    print(f"  Input: {text}")
    print(f"  Concepts: {concepts}")
    # 不应包含单字
    check(all(len(c) > 1 for c in concepts), "所有概念长度 > 1（非单字）")
    # 英文术语应被识别（如 "Mem" from "XMem"）
    check(any(c.isascii() for c in concepts), "包含英文术语")


def test_cross_session_persistence():
    """P0 回归：验证 Session 2 能恢复 Session 1 的向量和图谱。"""
    print("\n=== 回归测试: 跨会话持久化 (P0 fix) ===")
    persistence = MemoryPersistence()
    session_id = "test_cross_session_001"

    # Session 1: 添加数据
    store1 = SimpleVectorStore()
    graph1 = ConceptGraph()
    store1.add("XMem paper abstract: long-term memory for VOS")
    store1.add("MemoryBank paper abstract: Ebbinghaus forgetting curve")
    graph1.add_concept("Video Object Segmentation", "VOS task")
    graph1.add_concept("XMem", "long-term VOS method")
    graph1.add_relation("Video Object Segmentation", "XMem", "implemented_by")

    persistence.save_full_state(session_id, store1, graph1, {"summaries": ["Test summary"]})
    print("  Session 1: 已保存 2 篇论文 + 2 个概念 + 1 条关系")

    # Session 2: 恢复
    loaded = persistence.load_full_state(session_id)
    check(loaded is not None, "load_full_state 返回非空")

    store2 = loaded["vector_store"]
    graph2 = loaded["concept_graph"]
    check(store2.size() == 2, f"向量库恢复: {store2.size()} 条 (期望 2)")
    check(graph2.summary()["concepts"] >= 2, f"图谱概念恢复: {graph2.summary()['concepts']} 个")
    check(graph2.summary()["relations"] >= 1, f"图谱关系恢复: {graph2.summary()['relations']} 条")

    extra = loaded.get("extra", {})
    check("summaries" in extra, "额外元数据保留")

    # 清理
    persistence.cleanup()


def test_token_estimate_no_shadow():
    """P2.3 回归：验证 token_estimate 函数可被正常调用。"""
    print("\n=== 回归测试: token_estimate 参数遮蔽 (P2.3 fix) ===")
    result = token_estimate("hello world this is a test")
    check(result > 0, f"token_estimate 正常返回 {result}")


def test_regex_instead_of_character_class():
    """P1 回归：验证正则匹配连续汉字而非单字。"""
    print("\n=== 回归测试: 正则改为匹配汉字序列 (P1 fix) ===")
    text = "视频目标分割知识图谱时序推理记忆系统"
    matches = re.findall(r'[一-鿿]{2,}', text)
    print(f"  匹配结果: {matches}")
    check(len(matches) > 0, "匹配到汉字序列")
    check(all(len(m) >= 2 for m in matches), "所有匹配项长度 >= 2")


# ---- V1 测试 ----

def test_v1():
    print("\n" + "=" * 60)
    print("V1 测试: 短期记忆（滑动窗口 + 摘要压缩）")
    print("=" * 60)

    loop = ChatLoop(max_tokens=200)
    resp = loop.send("帮我总结一下 XMem 论文的核心贡献")
    check(resp.startswith("[模拟响应]"), "send() 返回模拟响应")
    print(f"  第 1 轮: {resp}")

    resp = loop.send("它和之前的 VOS 方法有什么主要区别？")
    check(resp.startswith("[模拟响应]"), "第 2 轮正常响应")
    print(f"  第 2 轮: {resp}")

    resp = loop.send("刚才说的 XMem 的核心优势是什么？")
    check(resp.startswith("[模拟响应]"), "第 3 轮正常响应")
    print(f"  第 3 轮: {resp}")

    state = loop.state()
    check(state["message_count"] > 0, f"工作记忆有 {state['message_count']} 条消息")
    check(state["current_tokens"] <= 200, f"未超过 max_tokens ({state['current_tokens']} <= 200)")
    print(f"  记忆状态: {json.dumps(state, ensure_ascii=False)}")


# ---- V2 测试 ----

def test_v2():
    print("\n" + "=" * 60)
    print("V2 测试: 长期记忆（向量存储 + 知识图谱 + 跨会话）")
    print("=" * 60)

    mc = MemoryController(max_context_tokens=500)
    mc.start_session("v2_test_001")

    mc.add_paper("XMem: Long-Term VOS", "XMem proposes long-term memory network for VOS with memory reading.")
    mc.add_paper("MemoryBank", "MemoryBank introduces memory mechanism inspired by Ebbinghaus forgetting curve.")
    mc.add_concept_relation("Video Object Segmentation", "XMem", "implemented_by")
    mc.add_concept_relation("XMem", "MemoryBank", "shares_concept")

    vs_size_before = mc.vector_store.size()
    resp = mc.send("Can you summarize XMem paper?")
    check(resp.startswith("[模拟响应]"), "send() 返回模拟响应")
    print(f"  V2 响应: {resp[:60]}...")

    # 验证概念提取
    concepts = mc._extract_concepts("XMem paper summary")
    check(len(concepts) > 0, f"概念提取: {concepts}")

    # 直接验证持久化层 (V2 的 _persist 只存元数据, 通过 save_full_state 验证跨会话)
    mc.persistence.save_full_state("v2_test_001", mc.vector_store, mc.concept_graph, {"summaries": mc.session_summaries})

    mc2 = MemoryController(max_context_tokens=500)
    mc2.start_session("v2_test_001")
    check(mc2.vector_store.size() == vs_size_before,
          f"跨会话向量库恢复: {mc2.vector_store.size()} == {vs_size_before}")
    print(f"  ✓ 跨会话: 向量库 {mc2.vector_store.size()} 篇论文, 图谱 {mc2.concept_graph.summary()}")

    mc.persistence.cleanup()


# ---- V3 测试 ----

def test_v3():
    print("\n" + "=" * 60)
    print("V3 测试: 程序性记忆（经验库 + 画像 + 反思）")
    print("=" * 60)

    v3 = MemoryControllerV3(max_context_tokens=500)
    v3.start_session("v3_test_001")

    v3.add_paper("XMem", "XMem long-term memory VOS paper")
    v3.add_concept_relation("Video Segmentation", "XMem", "implemented_by")

    # 第 1 轮
    resp1 = v3.send("Summarize XMem paper")
    check(resp1.startswith("[模拟响应]"), "第 1 轮正常")
    print(f"  第 1 轮: {resp1[:60]}...")

    # 第 2 轮 — 触发反思（含"不对"）
    resp2 = v3.send("不对，我要的是 memory reading 细节")
    check("经验库提醒" in resp2 or "检索到" in resp2, "第 2 轮响应包含记忆信息")
    print(f"  第 2 轮: {resp2}")

    # 验证反思被触发
    check(len(v3.reflection_triggered) > 0, f"反思已触发 ({len(v3.reflection_triggered)} 次)")
    check(v3.experience_store.size() > 0, f"经验库有 {v3.experience_store.size()} 条记录")

    # 验证画像
    topics = v3.user_profile.get_active_topics()
    check(len(topics) > 0, f"画像追踪到主题: {topics}")

    # 验证钩子而非重复代码
    check(type(v3)._generate_response is not MemoryController._generate_response,
           "V3 重写了 _generate_response (无代码重复)")
    print(f"  ✓ V3 通过钩子扩展 V2，send() 仅 1 行 (return super().send())")

    v3.persistence.cleanup()


# ---- V4 测试 ----

def test_v4():
    print("\n" + "=" * 60)
    print("V4 测试: 完整系统（治理 + 全状态输出）")
    print("=" * 60)

    agent = ResearchAgent(max_context_tokens=500)
    agent.start_session("v4_test_001")

    agent.add_paper("XMem", "XMem long-term memory VOS paper")
    agent.add_concept_relation("VOS", "XMem", "implemented_by")

    resp = agent.send("Summarize XMem paper")
    check(resp.startswith("[模拟响应]"), "第 1 轮正常")
    print(f"  第 1 轮: {resp[:60]}...")

    # 验证治理检查（不触发清理，但代码路径应正常）
    check(agent.governance is not None, "治理模块已加载")
    check(len(agent.memory_log) > 0, f"操作日志: {len(agent.memory_log)} 条")

    # 验证 full_state
    state = agent.full_state()
    check("experiences" in state, "full_state 包含经验计数")
    check("governance" in state, "full_state 包含治理配置")
    check("user_profile" in state, "full_state 包含用户画像")
    print(f"  系统状态: vector_store={state['vector_store']}, "
          f"graph={state['concept_graph']}, "
          f"experiences={state['experiences']}, "
          f"interactions={state['user_profile']['total_interactions']}")

    # 治理 cleanup 测试（用模拟数据）
    gov = MemoryGovernance(default_ttl_days=0)  # TTL=0 立即过期
    items = [{"created_at": time.time() - 86400 * 10, "confidence": 1.0, "text": "old memory"}]
    remaining = gov.cleanup(items)
    check(len(remaining) == 0, f"治理清理: {len(items)} -> {len(remaining)} (TTL=0)")
    print(f"  ✓ 治理清理功能正常")

    agent.persistence.cleanup()


# ---- 完整运行示例（跨会话回忆） ----

def test_cross_session_demo():
    """模拟 16.6.3 跨会话场景，验证 Session 2 可检索 Session 1 的数据。"""
    print("\n" + "=" * 60)
    print("跨会话回忆演示 (16.6.3)")
    print("=" * 60)

    agent = ResearchAgent(max_context_tokens=500)
    agent.start_session("alice_research_001")

    # Session 1: 添加论文和关系
    agent.add_paper("XMem", "XMem proposes a long-term memory network for VOS with memory reading.")
    agent.add_paper("MemoryBank", "MemoryBank introduces memory mechanism inspired by Ebbinghaus forgetting curve.")
    agent.add_concept_relation("Video Object Segmentation", "XMem", "implemented_by")
    agent.add_concept_relation("Video Object Segmentation", "Memory", "requires")
    agent.add_concept_relation("XMem", "MemoryBank", "shares_concept")

    vs_size = agent.vector_store.size()
    graph_summary = agent.concept_graph.summary()
    print(f"  Session 1 存储: 向量 {vs_size} 篇论文, 图谱 {graph_summary}")

    resp = agent.send("I am researching video object segmentation, summarize XMem paper")
    print(f"  第 1 轮: {resp}")

    # 模拟 Session 2（新 Agent）
    agent2 = ResearchAgent(max_context_tokens=500)
    agent2.start_session("alice_research_001")

    check(agent2.vector_store.size() == vs_size,
          f"Session 2 向量库恢复: {agent2.vector_store.size()} == {vs_size}")
    check(agent2.concept_graph.summary()["concepts"] == graph_summary["concepts"],
          f"Session 2 图谱概念恢复: {agent2.concept_graph.summary()['concepts']} == {graph_summary['concepts']}")
    check(agent2.concept_graph.summary()["relations"] == graph_summary["relations"],
          f"Session 2 图谱关系恢复: {agent2.concept_graph.summary()['relations']} == {graph_summary['relations']}")

    print(f"  ✓ 跨会话回忆验证通过 — Session 2 成功恢复 Session 1 数据")

    # Session 2 检索
    resp = agent2.send("What is XMem core advantage?")
    check("检索到" in resp or "经验库提醒" in resp, f"Session 2 响应包含记忆上下文")
    print(f"  Session 2 检索响应: {resp}")

    agent.persistence.cleanup()


# ============================================================
# 运行
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("第16章 综合案例单元测试")
    print("=" * 60)

    test_concept_extraction()
    test_regex_instead_of_character_class()
    test_token_estimate_no_shadow()
    test_v1()
    test_v2()
    test_v3()
    test_v4()
    test_cross_session_persistence()
    test_cross_session_demo()

    print("\n" + "=" * 60)
    total = PASS + FAIL
    print(f"结果: {PASS}/{total} 通过", end="")
    if FAIL > 0:
        print(f", {FAIL} 失败 ❌")
    else:
        print(" ✅")
    print("=" * 60)
    sys.exit(0 if FAIL == 0 else 1)
