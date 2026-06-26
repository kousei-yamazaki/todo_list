"""
タスク追加・編集ダイアログ
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple


class TaskDialog(tk.Toplevel):
    """タスクの追加・編集を行うダイアログウィンドウ"""

    def __init__(
        self,
        parent: tk.Widget,
        title: str = "タスク",
        initial_title: str = "",
        initial_description: str = "",
    ):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.grab_set()  # モーダルダイアログにする

        self.result: Optional[Tuple[str, str]] = None

        self._build_ui(initial_title, initial_description)
        self._center(parent)
        self.wait_window()

    def _build_ui(self, initial_title: str, initial_description: str) -> None:
        """UIを構築する"""
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill=tk.BOTH, expand=True)

        # タイトル入力
        ttk.Label(frame, text="タイトル（必須）:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 4)
        )
        self._title_var = tk.StringVar(value=initial_title)
        self._title_entry = ttk.Entry(frame, textvariable=self._title_var, width=40)
        self._title_entry.grid(row=1, column=0, sticky=tk.EW, pady=(0, 12))
        self._title_entry.focus_set()

        # メモ入力
        ttk.Label(frame, text="メモ:").grid(row=2, column=0, sticky=tk.W, pady=(0, 4))
        self._desc_text = tk.Text(frame, width=40, height=6, wrap=tk.WORD)
        self._desc_text.insert("1.0", initial_description)
        self._desc_text.grid(row=3, column=0, sticky=tk.EW, pady=(0, 16))

        # ボタン
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, sticky=tk.E)

        ttk.Button(btn_frame, text="キャンセル", command=self.destroy).pack(
            side=tk.RIGHT, padx=(8, 0)
        )
        ttk.Button(btn_frame, text="保存", command=self._on_save).pack(side=tk.RIGHT)

        frame.columnconfigure(0, weight=1)

        # Enterキーで保存
        self.bind("<Return>", lambda e: self._on_save())
        self.bind("<Escape>", lambda e: self.destroy())

    def _on_save(self) -> None:
        """保存ボタン押下時の処理"""
        title = self._title_var.get().strip()
        if not title:
            self._title_entry.focus_set()
            self._title_entry.config(style="Error.TEntry")
            return
        description = self._desc_text.get("1.0", tk.END).strip()
        self.result = (title, description)
        self.destroy()

    def _center(self, parent: tk.Widget) -> None:
        """親ウィンドウの中央に配置する"""
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width() // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        w = self.winfo_width()
        h = self.winfo_height()
        self.geometry(f"+{pw - w // 2}+{ph - h // 2}")
