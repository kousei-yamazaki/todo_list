"""
ToDo管理アプリケーション エントリポイント
"""
import sys
import os

# プロジェクトルートをパスに追加（サブモジュールの import を解決するため）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.app import TodoApp


def main() -> None:
    app = TodoApp()
    app.mainloop()


if __name__ == "__main__":
    main()
