"""
JSONファイルへのデータ永続化モジュール
"""
import json
import os
from pathlib import Path
from typing import List

from models.task import Task

# データ保存先ファイルパス
DATA_DIR = Path(__file__).parent
DATA_FILE = DATA_DIR / "tasks.json"


def load_tasks() -> List[Task]:
    """JSONファイルからタスク一覧を読み込む"""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Task.from_dict(item) for item in data]
    except (json.JSONDecodeError, KeyError):
        return []


def save_tasks(tasks: List[Task]) -> None:
    """タスク一覧をJSONファイルに保存する"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([task.to_dict() for task in tasks], f, ensure_ascii=False, indent=2)


def get_next_id(tasks: List[Task]) -> int:
    """次に使用するIDを返す"""
    if not tasks:
        return 1
    return max(task.id for task in tasks) + 1
