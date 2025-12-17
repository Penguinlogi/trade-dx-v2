"""
変更履歴テーブルに案件番号スナップショットを付与する補正スクリプト

既存の履歴レコードには `_case_number_snapshot` が存在しないため、
案件番号が後から変わった場合に表示が上書きされてしまう。
このスクリプトを実行すると、可能な限り過去の履歴にもスナップショットを補完する。
"""

from __future__ import annotations

from collections import defaultdict

from app.core.database import SessionLocal
from app.models.change_history import ChangeHistory


def extract_case_number_from_changes(history: ChangeHistory) -> tuple[None | str, None | str]:
    """
    changes_json から case_number の新旧値を取得する。

    Returns:
        tuple(old, new)
    """
    if not history.changes_json or not isinstance(history.changes_json, dict):
        return None, None

    entry = history.changes_json.get("case_number")
    if isinstance(entry, dict):
        return entry.get("old"), entry.get("new")

    if isinstance(entry, str):
        # 文字列で保存されている場合は old/new の区別は出来ない
        return entry, entry

    return None, None


def main() -> None:
    session = SessionLocal()
    try:
        histories = (
            session.query(ChangeHistory)
            .order_by(ChangeHistory.case_id.asc(), ChangeHistory.changed_at.asc(), ChangeHistory.id.asc())
            .all()
        )

        current_case_number = defaultdict(lambda: None)
        updated = 0

        for history in histories:
            case_id = history.case_id
            old_number, new_number = extract_case_number_from_changes(history)
            snapshot_value = None

            if history.change_type == "CREATE":
                snapshot_value = new_number or old_number
                current_case_number[case_id] = snapshot_value
            elif history.change_type == "DELETE":
                snapshot_value = old_number or current_case_number[case_id]
                current_case_number[case_id] = None
            else:
                # UPDATE など
                snapshot_value = (new_number or old_number) or current_case_number[case_id]
                if new_number:
                    current_case_number[case_id] = new_number

            if not snapshot_value:
                snapshot_value = current_case_number[case_id]

            if snapshot_value:
                if history.changes_json is None or not isinstance(history.changes_json, dict):
                    history.changes_json = {}
                if not history.changes_json.get("_case_number_snapshot"):
                    history.changes_json["_case_number_snapshot"] = snapshot_value
                    updated += 1

        session.commit()
        print(f"[完了] {_safe_int(len(histories))}件中 {updated}件の履歴にスナップショットを追加しました。")
    finally:
        session.close()


def _safe_int(value) -> int:
    try:
        return int(value)
    except Exception:
        return 0


if __name__ == "__main__":
    main()








