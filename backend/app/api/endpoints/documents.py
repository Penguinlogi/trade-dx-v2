"""
ドキュメント生成API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.document import (
    DocumentGenerateRequest,
    DocumentResponse,
    DocumentListResponse
)
from app.services.document_generator import DocumentGenerator


router = APIRouter()


@router.post("/invoice", response_model=DocumentResponse, summary="Invoice生成")
async def generate_invoice(
    request: DocumentGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    指定された案件のInvoice（請求書）を生成します

    - **case_id**: 案件ID
    - **document_type**: "invoice"
    - **template_name**: テンプレート名（オプション）
    """
    if request.document_type != "invoice":
        raise HTTPException(status_code=400, detail="document_type must be 'invoice'")

    try:
        generator = DocumentGenerator(db)
        document = generator.generate_invoice(
            case_id=request.case_id,
            user_id=current_user.id,
            template_name=request.template_name
        )
        return document
    except ValueError as e:
        print(f"ValueError in generate_invoice: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Exception in generate_invoice: {error_detail}")
        raise HTTPException(status_code=500, detail=f"Failed to generate invoice: {str(e)}")


@router.post("/packing-list", response_model=DocumentResponse, summary="Packing List生成")
async def generate_packing_list(
    request: DocumentGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    指定された案件のPacking List（梱包リスト）を生成します

    - **case_id**: 案件ID
    - **document_type**: "packing_list"
    - **template_name**: テンプレート名（オプション）
    """
    if request.document_type != "packing_list":
        raise HTTPException(status_code=400, detail="document_type must be 'packing_list'")

    try:
        generator = DocumentGenerator(db)
        document = generator.generate_packing_list(
            case_id=request.case_id,
            user_id=current_user.id,
            template_name=request.template_name
        )
        return document
    except ValueError as e:
        print(f"ValueError in generate_packing_list: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Exception in generate_packing_list: {error_detail}")
        raise HTTPException(status_code=500, detail=f"Failed to generate packing list: {str(e)}")


@router.get("", response_model=DocumentListResponse, summary="ドキュメント一覧取得")
async def get_documents(
    case_id: Optional[int] = Query(None, description="案件IDでフィルタリング"),
    document_type: Optional[str] = Query(None, description="ドキュメントタイプでフィルタリング"),
    skip: int = Query(0, ge=0, description="スキップ数"),
    limit: int = Query(100, ge=1, le=1000, description="取得件数上限"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    生成されたドキュメントの一覧を取得します

    - **case_id**: 案件IDでフィルタリング（オプション）
    - **document_type**: ドキュメントタイプでフィルタリング（オプション）
    - **skip**: スキップ数
    - **limit**: 取得件数上限
    """
    try:
        generator = DocumentGenerator(db)
        documents, total = generator.get_documents(
            case_id=case_id,
            document_type=document_type,
            skip=skip,
            limit=limit
        )
        return DocumentListResponse(documents=documents, total=total)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get documents: {str(e)}")


@router.get("/{document_id}/download", summary="ドキュメントダウンロード")
async def download_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    指定されたドキュメントをダウンロードします

    - **document_id**: ドキュメントID
    """
    try:
        generator = DocumentGenerator(db)
        filepath = generator.get_document_file(document_id)

        # ドキュメント情報を取得してファイル名を取得
        from app.models.document import Document
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        return FileResponse(
            path=str(filepath),
            filename=document.file_name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download document: {str(e)}")
