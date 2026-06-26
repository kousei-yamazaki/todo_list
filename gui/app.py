"""
メインGUIアプリケーション
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional

from models.task import Task
from data.storage import load_tasks, save_tasks, get_next_id
from gui.dialogs import TaskDialog


class TodoApp(tk.Tk):
    """ToDoアプリのメインウィンドウ"""

    def __init__(self):
        super().__init__()
        self.title("ToDo管理アプリ")
        self.geometry("680x520")
        self.minsize(500, 400)

        self._tasks: List[Task] = load_tasks()
        self._build_ui()
        self._refresh()

    # ──────────────────────────────────────────
    # UI構築
    # ──────────────────────────────────────────

    def _build_ui(self) -> None:
        """UIを構築する"""
        self._setup_styles()

        # ── ツールバー ──
        toolbar = ttk.Frame(self, padding=(8, 6))
        toolbar.pack(fill=tk.X)

        ttk.Button(toolbar, text="＋ タスクを追加", command=self._add_task).pack(
            side=tk.LEFT
        )

        # ── メインコンテンツ（スクロール可能） ──
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._scroll_frame = ttk.Frame(canvas)
        self._scroll_window = canvas.create_window(
            (0, 0), window=self._scroll_frame, anchor=tk.NW
        )

        self._scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(self._scroll_window, width=e.width),
        )
        # マウスホイールスクロール
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        self._canvas = canvas

    def _setup_styles(self) -> None:
        """ttk スタイルを設定する"""
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Section.TLabel", font=("Yu Gothic UI", 11, "bold"), foreground="#444")
        style.configure("Task.TFrame", background="#f9f9f9", relief="flat")
        style.configure("Done.TLabel", foreground="#aaa")
        style.configure(
            "Action.TButton",
            padding=(4, 2),
            font=("Yu Gothic UI", 9),
        )

    # ──────────────────────────────────────────
    # タスク一覧の描画
    # ──────────────────────────────────────────

    def _refresh(self) -> None:
        """タスク一覧を再描画する"""
        for widget in self._scroll_frame.winfo_children():
            widget.destroy()

        incomplete = [t for t in self._tasks if not t.completed]
        complete = [t for t in self._tasks if t.completed]

        # 未完了タスク
        self._render_section("📋 未完了タスク", incomplete, row_start=0)

        # 完了タスク
        sep_row = len(incomplete) + 2
        ttk.Separator(self._scroll_frame, orient=tk.HORIZONTAL).grid(
            row=sep_row, column=0, columnspan=4, sticky=tk.EW, pady=8
        )
        self._render_section("✅ 完了タスク", complete, row_start=sep_row + 1)

        self._scroll_frame.columnconfigure(1, weight=1)

    def _render_section(self, heading: str, tasks: List[Task], row_start: int) -> None:
        """セクション見出しとタスク行を描画する"""
        ttk.Label(self._scroll_frame, text=heading, style="Section.TLabel").grid(
            row=row_start, column=0, columnspan=4, sticky=tk.W, padx=4, pady=(8, 4)
        )

        if not tasks:
            ttk.Label(
                self._scroll_frame,
                text="  タスクはありません",
                foreground="#bbb",
            ).grid(row=row_start + 1, column=0, columnspan=4, sticky=tk.W, padx=16)
            return

        for i, task in enumerate(tasks):
            self._render_task_row(task, row=row_start + 1 + i)

    def _render_task_row(self, task: Task, row: int) -> None:
        """1タスク分の行を描画する"""
        # チェックボックス
        var = tk.BooleanVar(value=task.completed)
        chk = ttk.Checkbutton(
            self._scroll_frame,
            variable=var,
            command=lambda t=task, v=var: self._toggle_complete(t, v),
        )
        chk.grid(row=row, column=0, padx=(8, 4), pady=3, sticky=tk.W)

        # タイトル＋メモ
        label_style = "Done.TLabel" if task.completed else "TLabel"
        title_text = task.title
        if task.description:
            title_text += f"\n  📝 {task.description}"

        lbl = ttk.Label(
            self._scroll_frame,
            text=title_text,
            style=label_style,
            wraplength=380,
            justify=tk.LEFT,
        )
        lbl.grid(row=row, column=1, sticky=tk.W, padx=4, pady=3)

        # 編集ボタン
        ttk.Button(
            self._scroll_frame,
            text="編集",
            style="Action.TButton",
            command=lambda t=task: self._edit_task(t),
        ).grid(row=row, column=2, padx=4, pady=3)

        # 削除ボタン
        ttk.Button(
            self._scroll_frame,
            text="削除",
            style="Action.TButton",
            command=lambda t=task: self._delete_task(t),
        ).grid(row=row, column=3, padx=(0, 8), pady=3)

    # ──────────────────────────────────────────
    # タスク操作
    # ──────────────────────────────────────────

    def _add_task(self) -> None:
        """タスク追加ダイアログを開く"""
        dialog = TaskDialog(self, title="タスクを追加")
        if dialog.result:
            title, description = dialog.result
            new_task = Task(
                id=get_next_id(self._tasks),
                title=title,
                description=description,
            )
            self._tasks.append(new_task)
            self._persist()
            self._refresh()

    def _edit_task(self, task: Task) -> None:
        """タスク編集ダイアログを開く"""
        dialog = TaskDialog(
            self,
            title="タスクを編集",
            initial_title=task.title,
            initial_description=task.description,
        )
        if dialog.result:
            title, description = dialog.result
            task.title = title
            task.description = description
            self._persist()
            self._refresh()

    def _toggle_complete(self, task: Task, var: tk.BooleanVar) -> None:
        """完了状態を切り替える"""
        task.completed = var.get()
        self._persist()
        self._refresh()

    def _delete_task(self, task: Task) -> None:
        """タスクを削除する（確認ダイアログあり）"""
        confirmed = messagebox.askyesno(
            "削除の確認",
            f"「{task.title}」を削除しますか？",
            parent=self,
        )
        if confirmed:
            self._tasks = [t for t in self._tasks if t.id != task.id]
            self._persist()
            self._refresh()

    def _persist(self) -> None:
        """現在のタスク一覧をJSONに保存する"""
        save_tasks(self._tasks)
