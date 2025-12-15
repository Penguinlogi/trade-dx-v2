/**
 * ドキュメント生成API
 */
import { axiosInstance } from "./axios";
import { ENDPOINTS } from "./endpoints";

// ドキュメントタイプ
export type DocumentType = "invoice" | "packing_list";

// ドキュメント生成リクエスト
export interface DocumentGenerateRequest {
  case_id: number;
  document_type: DocumentType;
  template_name?: string;
}

// ドキュメントレスポンス
export interface Document {
  id: number;
  case_id: number;
  document_type: DocumentType;
  file_name: string;
  file_path?: string;
  template_name?: string;
  generated_by: number;
  generated_at: string;
  notes?: string;
}

// ドキュメント一覧レスポンス
export interface DocumentListResponse {
  documents: Document[];
  total: number;
}

// Invoice生成
export const generateInvoice = async (
  caseId: number,
  templateName?: string
): Promise<Document> => {
  const response = await axiosInstance.post<Document>(
    ENDPOINTS.DOCUMENTS.INVOICE,
    {
      case_id: caseId,
      document_type: "invoice",
      template_name: templateName,
    }
  );
  return response.data;
};

// Packing List生成
export const generatePackingList = async (
  caseId: number,
  templateName?: string
): Promise<Document> => {
  const response = await axiosInstance.post<Document>(
    ENDPOINTS.DOCUMENTS.PACKING_LIST,
    {
      case_id: caseId,
      document_type: "packing_list",
      template_name: templateName,
    }
  );
  return response.data;
};

// ドキュメント一覧取得
export const getDocuments = async (params?: {
  case_id?: number;
  document_type?: DocumentType;
  skip?: number;
  limit?: number;
}): Promise<DocumentListResponse> => {
  const response = await axiosInstance.get<DocumentListResponse>(
    ENDPOINTS.DOCUMENTS.LIST,
    {
      params,
    }
  );
  return response.data;
};

// ドキュメントダウンロード
export const downloadDocument = async (documentId: number): Promise<void> => {
  const response = await axiosInstance.get(
    ENDPOINTS.DOCUMENTS.DOWNLOAD(documentId),
    {
      responseType: "blob",
    }
  );

  // ファイル名を取得（Content-Dispositionヘッダーから）
  const contentDisposition = response.headers["content-disposition"];
  let filename = `document_${documentId}.xlsx`;

  if (contentDisposition) {
    const filenameMatch = contentDisposition.match(/filename="?(.+?)"?$/);
    if (filenameMatch) {
      filename = filenameMatch[1];
    }
  }

  // Blobを作成してダウンロード
  const blob = new Blob([response.data], {
    type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};
