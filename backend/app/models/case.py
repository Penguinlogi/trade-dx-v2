"""
案件モデル
"""
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Text, ForeignKey, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class Case(Base):
    """案件テーブル"""
    __tablename__ = "cases"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(20), unique=True, nullable=False, index=True, comment="案件番号 (例: 2025-EX-001)")

    # 区分
    trade_type = Column(String(10), nullable=False, comment="区分（輸出/輸入）")

    # 顧客・仕入先情報
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, comment="顧客ID")
    supplier_name = Column(String(100), nullable=True, comment="仕入先名")

    # 商品情報
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="商品ID")
    quantity = Column(Numeric(15, 3), nullable=False, comment="数量")
    unit = Column(String(10), nullable=False, comment="単位")

    # 価格情報
    sales_unit_price = Column(Numeric(15, 2), nullable=False, comment="販売単価")
    purchase_unit_price = Column(Numeric(15, 2), nullable=False, comment="仕入単価")
    sales_amount = Column(Numeric(15, 2), nullable=True, comment="売上額（計算値）")
    gross_profit = Column(Numeric(15, 2), nullable=True, comment="粗利額（計算値）")
    gross_profit_rate = Column(Numeric(5, 2), nullable=True, comment="粗利率%（計算値）")

    # スケジュール
    shipment_date = Column(Date, nullable=True, comment="船積予定日")

    # ステータス
    status = Column(String(20), nullable=False, comment="ステータス（見積中/受注済/船積済/完了/キャンセル）")

    # 担当者
    pic = Column(String(50), nullable=False, comment="担当者名")

    # 備考
    notes = Column(Text, nullable=True, comment="備考")

    # 作成・更新情報
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="作成者ID")
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="更新者ID")
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), onupdate=func.now(), nullable=False)

    # リレーション
    customer = relationship("Customer", back_populates="cases")
    product = relationship("Product", back_populates="cases")
    # 変更履歴は案件削除後も残すため、cascadeを設定しない
    # passive_deletes=Trueを設定して、削除時に変更履歴を更新しない
    change_histories = relationship("ChangeHistory", back_populates="case", passive_deletes=True)
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Case(id={self.id}, case_number={self.case_number}, customer={self.customer.customer_name if self.customer else 'N/A'})>"

    def calculate_amounts(self):
        """金額を計算する"""
        if self.quantity and self.sales_unit_price and self.purchase_unit_price:
            self.sales_amount = self.quantity * self.sales_unit_price
            total_cost = self.quantity * self.purchase_unit_price
            self.gross_profit = self.sales_amount - total_cost
            if self.sales_amount > 0:
                self.gross_profit_rate = (self.gross_profit / self.sales_amount) * 100
            else:
                self.gross_profit_rate = 0
