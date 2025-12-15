"""
変更履歴サービス
"""
from typing import Optional, Any, Dict
from sqlalchemy.orm import Session
from ..models.change_history import ChangeHistory as ChangeHistoryModel
from ..models.case import Case as CaseModel
from datetime import datetime
import json


def serialize_value(value: Any) -> Optional[str]:
    """
    値を文字列にシリアライズ

    Args:
        value: シリアライズする値

    Returns:
        文字列化された値
    """
    if value is None:
        return None

    if isinstance(value, (int, float, str, bool)):
        return str(value)

    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, default=str)

    return str(value)


def record_change_history(
    db: Session,
    case_id: int,
    change_type: str,
    changed_by: Optional[int],
    old_case: Optional[CaseModel] = None,
    new_case: Optional[CaseModel] = None,
    changes: Optional[Dict[str, Any]] = None,
    notes: Optional[str] = None,
    case_number_snapshot: Optional[str] = None,
) -> ChangeHistoryModel:
    """
    変更履歴を記録

    Args:
        db: データベースセッション
        case_id: 案件ID
        change_type: 変更タイプ（CREATE/UPDATE/DELETE）
        changed_by: 変更者ID
        old_case: 変更前の案件データ（UPDATE/DELETEの場合）
        new_case: 変更後の案件データ（CREATE/UPDATEの場合）
        changes: 変更内容の辞書（フィールド名と新旧値のペア）
        notes: 備考

    Returns:
        ChangeHistoryModel: 作成された変更履歴
    """
    # 案件番号スナップショット（履歴表示用）
    snapshot_case_number = (
        case_number_snapshot
        or (getattr(new_case, "case_number", None) if new_case else None)
        or (getattr(old_case, "case_number", None) if old_case else None)
    )

    change_history = ChangeHistoryModel(
        case_id=case_id,
        changed_by=changed_by,
        change_type=change_type,
        notes=notes
    )

    # 変更タイプに応じて履歴を記録
    if change_type == "CREATE" and new_case:
        # 新規作成時は全フィールドを記録
        changes_dict = {}
        for field in [
            'case_number', 'trade_type', 'customer_id', 'supplier_name',
            'product_id', 'quantity', 'unit', 'sales_unit_price',
            'purchase_unit_price', 'shipment_date', 'status', 'pic', 'notes'
        ]:
            value = getattr(new_case, field, None)
            if value is not None:
                changes_dict[field] = {
                    'old': None,
                    'new': serialize_value(value)
                }

        change_history.changes_json = changes_dict
        change_history.field_name = None
        change_history.old_value = None
        change_history.new_value = None

    elif change_type == "UPDATE":
        # 更新時は変更されたフィールドのみ記録
        if changes:
            # 明示的な変更辞書が指定されている場合
            changes_dict = {}
            single_field_changes = []

            for field_name, change_data in changes.items():
                if isinstance(change_data, dict) and 'old' in change_data and 'new' in change_data:
                    changes_dict[field_name] = {
                        'old': serialize_value(change_data['old']),
                        'new': serialize_value(change_data['new'])
                    }
                    single_field_changes.append((field_name, change_data['old'], change_data['new']))

            change_history.changes_json = changes_dict

            # 単一フィールド変更の場合は、最初の変更をフィールド名として記録
            if len(single_field_changes) == 1:
                field_name, old_val, new_val = single_field_changes[0]
                change_history.field_name = field_name
                change_history.old_value = serialize_value(old_val)
                change_history.new_value = serialize_value(new_val)
            else:
                change_history.field_name = None
                change_history.old_value = None
                change_history.new_value = None

        elif old_case and new_case:
            # 変更前後のオブジェクトを比較
            changes_dict = {}
            changed_fields = []

            for field in [
                'case_number', 'trade_type', 'customer_id', 'supplier_name',
                'product_id', 'quantity', 'unit', 'sales_unit_price',
                'purchase_unit_price', 'shipment_date', 'status', 'pic', 'notes'
            ]:
                old_value = getattr(old_case, field, None)
                new_value = getattr(new_case, field, None)

                # 値が変更されているかチェック
                if old_value != new_value:
                    changes_dict[field] = {
                        'old': serialize_value(old_value),
                        'new': serialize_value(new_value)
                    }
                    if not changed_fields:
                        change_history.field_name = field
                        change_history.old_value = serialize_value(old_value)
                        change_history.new_value = serialize_value(new_value)

            change_history.changes_json = changes_dict

    elif change_type == "DELETE" and old_case:
        # 削除時は削除されたデータを記録
        changes_dict = {}
        for field in [
            'case_number', 'trade_type', 'customer_id', 'supplier_name',
            'product_id', 'quantity', 'unit', 'sales_unit_price',
            'purchase_unit_price', 'shipment_date', 'status', 'pic', 'notes'
        ]:
            value = getattr(old_case, field, None)
            if value is not None:
                changes_dict[field] = {
                    'old': serialize_value(value),
                    'new': None
                }

        change_history.changes_json = changes_dict
        change_history.field_name = None
        change_history.old_value = None
        change_history.new_value = None

    # 案件番号スナップショットをchanges_jsonに保存
    if snapshot_case_number:
        if change_history.changes_json is None:
            change_history.changes_json = {}
        change_history.changes_json["_case_number_snapshot"] = snapshot_case_number

    db.add(change_history)
    db.flush()  # IDを取得するためにflush
    db.refresh(change_history)

    return change_history
