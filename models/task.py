"""
タスクデータモデル
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    """タスクを表すデータクラス"""
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def to_dict(self) -> dict:
        """辞書形式に変換する"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """辞書からTaskオブジェクトを生成する"""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
        )
