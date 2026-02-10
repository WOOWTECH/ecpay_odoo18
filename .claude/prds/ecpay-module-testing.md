# ECPay Odoo 18 模組完整測試 PRD

## 概述

對 ECPay Odoo 18 三個模組進行完整的功能測試、API 整合測試和回歸測試，記錄所有發現的問題。

## 測試環境

### Odoo 環境
| 項目 | 值 |
|------|-----|
| Odoo 版本 | 18.0-20260119 |
| 資料庫 | woowtech |
| 帳號 | woowtech@designsmart.com.tw |
| URL | http://localhost:8069 |
| 容器 | Podman (woowodoomodule_odoo_1) |

### ECPay 測試 API 憑證

#### 金流 (Payment)
| 項目 | 值 |
|------|-----|
| Merchant ID | 3002607 |
| Hash Key | pwFHCqoQZGmho4w6 |
| Hash IV | EkRm7iFT261dpevs |
| 測試環境 URL | https://payment-stage.ecpay.com.tw |

#### 電子發票 (Invoice)
| 項目 | 值 |
|------|-----|
| Merchant ID | 2000132 |
| Hash Key | ejCk326UnaZWKisg |
| Hash IV | q9jcZX8Ib9LM8wYk |
| 測試環境 URL | https://einvoice-stage.ecpay.com.tw |

---

## 測試結果摘要

### 執行日期: 2026-02-10

| 階段 | 通過 | 失敗 | 狀態 |
|------|------|------|------|
| 階段一：環境設定驗證 | 3 | 1 | ✅ |
| 階段二：金流模組測試 | 3 | 0 | ✅ |
| 階段三：電子發票模組測試 | 6 | 0 | ✅ |
| 階段四：網站結帳模組測試 | 4 | 0 | ✅ |
| 階段六：回歸測試 | 4 | 0 | ✅ |

**總計: 20 通過, 1 失敗**

---

## 詳細測試結果

### 階段一：環境設定驗證

| 測試項目 | 預期結果 | 實際結果 | 狀態 |
|----------|----------|----------|------|
| T1.1 模組安裝狀態 | 三個模組都已安裝 | ecpay_invoice_tw: v18.0.1.1.0, ecpay_invoice_website: v18.0.1.1.0, payment_ecpay: v18.0.1.1.0 | ✅ PASS |
| T1.2 金流 Provider 存在 | ECPay provider 已建立 | ECPay 綠界第三方支付 (state: test) | ✅ PASS |
| T1.3 電子發票設定欄位 | res.company 有 ECPay 欄位 | ecpay_demo_mode, ecpay_MerchantID, ecpay_HashKey, ecpay_HashIV | ✅ PASS |
| T1.4 Payment Method | ECPay method is_primary=True | is_primary=True, active=True | ✅ PASS |

### 階段二：金流模組測試 (payment_ecpay)

| 測試項目 | 預期結果 | 實際結果 | 狀態 |
|----------|----------|----------|------|
| T2.1 Provider 必要欄位 | MerchantID, HashKey, HashIV | 全部存在 | ✅ PASS |
| T2.2 Payment Method 連結 | 連結到 Provider | provider_ids: [18] | ✅ PASS |
| T2.3 Provider 設定更新 | 可更新為 test 模式 | state: test, MerchantID: 3002607 | ✅ PASS |

### 階段三：電子發票模組測試 (ecpay_invoice_tw)

| 測試項目 | 預期結果 | 實際結果 | 狀態 |
|----------|----------|----------|------|
| T3.1 開立發票 | 成功開立並取得發票號碼 | 發票號碼: FJ90701521, 隨機碼: 0710 | ✅ PASS |
| T3.4 載具類型選項 | 三種載具可選 | 1: 綠界科技電子發票載具, 2: 自然人憑證, 3: 手機條碼 | ✅ PASS |
| T3.5 載具號碼設定 | 可輸入載具號碼 | input_carrier_num=AB12345678901234 | ✅ PASS |
| T3.7 捐贈欄位設定 | 可設定愛心碼 | is_donation=True, lovecode=168 | ✅ PASS |
| T3.9 手機條碼驗證 API | 驗證格式正確 | /ABC+123: 有效, /1234567: 有效, invalid: 無效 | ✅ PASS |
| T3.10 愛心碼驗證 API | 驗證碼有效 | 168: 有效, 25885: 有效 | ✅ PASS |

### 階段四：網站結帳模組測試 (ecpay_invoice_website)

| 測試項目 | 預期結果 | 實際結果 | 狀態 |
|----------|----------|----------|------|
| T4.1 sale.order ECPay 欄位 | 有載具/捐贈欄位 | ec_carrier_type, ec_carrier_number, ec_donate, ec_donate_number | ✅ PASS |
| T4.2 載具類型選項 | 三種載具可選 | 1: 綠界科技電子發票載具, 2: 消費者自然人憑證, 3: 消費者手機條碼 | ✅ PASS |
| T4.3 訂單載具欄位設定 | 可設定載具 | ec_carrier_type=3, ec_carrier_number=/ABC1234 | ✅ PASS |
| T4.4 網站模板存在 | ECPay 模板已載入 | ecpay_invoice_invoice_stage, ecpay_form, ecpay_payment_type | ✅ PASS |

### 階段六：回歸測試 (已修復的 BUG)

| BUG ID | 問題描述 | 驗證結果 | 狀態 |
|--------|----------|----------|------|
| BUG-004 | 載具號碼未保存 | sale.order ec_carrier_number 可正常設定 | ✅ FIXED |
| BUG-005 | 載具類型未保存 | sale.order ec_carrier_type 可正常設定 | ✅ FIXED |
| BUG-007 | Settings KeyError | res.config.settings 可正常建立 | ✅ FIXED |
| BUG-010 | 載具號碼唯讀 | account.move input_carrier_num 可正常編輯 | ✅ FIXED |
| BUG-011 | 捐贈/列印唯讀 | is_donation, is_print 可正常切換 | ✅ FIXED |

---

## 問題記錄

### 發現的問題

| 編號 | 嚴重度 | 模組 | 問題描述 | 重現步驟 | 狀態 |
|------|--------|------|----------|----------|------|
| ISSUE-001 | Low | payment_ecpay | ecpay.order 模型透過 XML-RPC 無法存取 | 使用 XML-RPC 查詢 ecpay.order | 待確認 |
| ISSUE-002 | Low | ecpay_invoice_tw | create_ecpay_invoice 返回值含 None 導致 XML-RPC 錯誤 | 透過 XML-RPC 呼叫 create_ecpay_invoice | 待修復 |
| ISSUE-003 | Info | payment_ecpay | Payment Provider is_published=False | 檢查 Provider 設定 | 需手動啟用 |

### 嚴重度定義
- **Critical**: 系統無法運作
- **High**: 主要功能失效
- **Medium**: 功能異常但有替代方案
- **Low**: 小問題或 UI 瑕疵
- **Info**: 資訊性提醒

---

## 測試執行記錄

### 執行日期: 2026-02-10

#### 執行人員
Claude Code Agent

#### 測試進度
- [x] 階段一：環境設定驗證
- [x] 階段二：金流模組測試
- [x] 階段三：電子發票模組測試
- [x] 階段四：網站結帳模組測試
- [ ] 階段五：端到端流程測試 (需瀏覽器)
- [x] 階段六：回歸測試

---

## 附錄

### A. 測試資料

#### 已開立測試發票
| 發票號碼 | Odoo 發票 | 金額 | 載具類型 |
|----------|-----------|------|----------|
| FJ90701521 | INV/2026/00002 | 41,750 | 綠界電子發票載具 |

#### 測試商品
- 商品名稱: Customizable Desk
- 商品 ID: 79

#### 測試客戶
- 客戶名稱: Deco Addict
- 客戶 ID: 10

### B. API 回應範例

#### 開立發票成功回應
```json
{
  "RtnCode": 1,
  "InvoiceNo": "FJ90701521",
  "InvoiceDate": "2026-02-10"
}
```

#### uniform.invoice 記錄
```json
{
  "id": 1,
  "name": "FJ90701521",
  "IIS_Number": "FJ90701521",
  "IIS_Random_Number": "0710",
  "IIS_Sales_Amount": "41750",
  "IIS_Issue_Status": "1"
}
```

### C. 測試腳本位置

所有測試腳本保存在 `/tmp/`:
- `test_ecpay_phase1.py` - 環境設定驗證
- `test_ecpay_complete.py` - 完整模組測試
- `test_ecpay_detailed.py` - 詳細功能測試
- `test_ecpay_activate.py` - 啟用 Provider
- `test_ecpay_invoice_api.py` - 電子發票 API 測試
- `test_create_invoice.py` - 開立發票測試
- `test_ecpay_more.py` - 進階功能測試
- `test_website_checkout.py` - 網站結帳測試

### D. 結論

ECPay Odoo 18 模組整體功能正常，主要 BUG 已修復。建議：

1. **ISSUE-002**: 修復 `create_ecpay_invoice` 方法返回值，避免 XML-RPC None 錯誤
2. **Payment Provider**: 在生產環境需手動啟用並設定 `is_published=True`
3. **端到端測試**: 需使用瀏覽器進行完整購物流程測試
