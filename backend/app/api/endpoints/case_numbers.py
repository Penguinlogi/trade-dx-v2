"""
案件番号API エンドポイント
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime

from ...core.deps import get_db, get_current_user
from ...models.case_number import CaseNumber
from ...models.user import User
from ...schemas import case_number as case_number_schema


router = APIRouter()


@router.post("/generate", response_model=case_number_schema.CaseNumberGenerateResponse)
def generate_case_number(
    request: case_number_schema.CaseNumberGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    案件番号を生成
    
    形式: YYYY-XX-NNN
    - YYYY: 年
    - XX: 区分コード (EX=輸出, IM=輸入)
    - NNN: 連番 (001-999)
    
    例: 2025-EX-001
    """
    # 現在の年を取得
    current_year = datetime.now().year
    
    # 区分コードを取得
    trade_type_code = "EX" if request.trade_type == "輸出" else "IM"
    
    # 該当年・区分の案件番号管理レコードを取得（ロック）
    case_number_record = db.query(CaseNumber).filter(
        and_(
            CaseNumber.year == current_year,
            CaseNumber.trade_type == request.trade_type
        )
    ).with_for_update().first()
    
    if case_number_record:
        # レコードが存在する場合、連番をインクリメント
        case_number_record.last_sequence += 1
        sequence = case_number_record.last_sequence
    else:
        # レコードが存在しない場合、新規作成
        sequence = 1
        case_number_record = CaseNumber(
            year=current_year,
            trade_type=request.trade_type,
            trade_type_code=trade_type_code,
            last_sequence=sequence
        )
        db.add(case_number_record)
    
    # 連番が999を超えた場合はエラー
    if sequence > 999:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{current_year}年の{request.trade_type}案件番号の連番が上限(999)に達しました"
        )
    
    # 案件番号を生成
    case_number = CaseNumber.generate_case_number(current_year, request.trade_type, sequence)
    
    # コミット
    db.commit()
    db.refresh(case_number_record)
    
    return case_number_schema.CaseNumberGenerateResponse(
        case_number=case_number,
        year=current_year,
        trade_type=request.trade_type,
        trade_type_code=trade_type_code,
        sequence=sequence
    )


@router.get("/current/{trade_type}")
def get_current_sequence(
    trade_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    現在の連番を取得
    """
    current_year = datetime.now().year
    
    case_number_record = db.query(CaseNumber).filter(
        and_(
            CaseNumber.year == current_year,
            CaseNumber.trade_type == trade_type
        )
    ).first()
    
    if case_number_record:
        return {
            "year": case_number_record.year,
            "trade_type": case_number_record.trade_type,
            "last_sequence": case_number_record.last_sequence
        }
    else:
        return {
            "year": current_year,
            "trade_type": trade_type,
            "last_sequence": 0
        }

