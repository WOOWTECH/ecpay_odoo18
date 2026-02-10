# ECPay API 參考文件

## 官方資源連結

### 開發者文件
| 文件 | 連結 |
|------|------|
| ECPay Developers 首頁 | https://developers.ecpay.com.tw/ |
| 全方位金流 API | https://developers.ecpay.com.tw/?p=2509 |
| B2C 電子發票 API | https://developers.ecpay.com.tw/?p=7809 |
| B2B 電子發票 (存證) | https://developers.ecpay.com.tw/?p=24139 |
| B2B 電子發票 (交換) | https://developers.ecpay.com.tw/?p=25224 |

### SDK 下載
| SDK | 連結 |
|-----|------|
| Python 金流 SDK | https://github.com/ECPay/ECPayAIO_Python |
| .NET 電子發票 SDK | https://github.com/ECPay/Invoice_Net |
| PHP SDK | https://github.com/ECPay/SDK_PHP |
| Ruby SDK | https://github.com/ECPay/ECPayAIO_RoR |

---

## 測試環境資訊

### 金流測試環境
| 項目 | 值 |
|------|-----|
| 測試 Merchant ID | 3002607 |
| 測試 Hash Key | pwFHCqoQZGmho4w6 |
| 測試 Hash IV | EkRm7iFT261dpevs |
| 測試環境 URL | https://payment-stage.ecpay.com.tw |

### 電子發票測試環境
| 項目 | 值 |
|------|-----|
| 測試 Merchant ID | 2000132 |
| 測試 Hash Key | ejCk326UnaZWKisg |
| 測試 Hash IV | q9jcZX8Ib9LM8wYk |
| 測試環境 URL | https://einvoice-stage.ecpay.com.tw |

---

## 金流 API 端點

### 基本 URL
- 正式環境: `https://payment.ecpay.com.tw`
- 測試環境: `https://payment-stage.ecpay.com.tw`

### 主要 API
| API | 端點 | 說明 |
|-----|------|------|
| 建立訂單 | /Cashier/AioCheckOut/V5 | 產生付款頁面 |
| 訂單查詢 | /Cashier/QueryTradeInfo/V5 | 查詢訂單狀態 |
| 信用卡授權 | /Cashier/QueryCreditCardPeriodInfo | 定期定額查詢 |
| 信用卡關帳 | /CreditDetail/DoAction | 請/退款操作 |

### 支援付款方式
- Credit (信用卡)
- WebATM (網路 ATM)
- ATM (ATM 櫃員機)
- CVS (超商代碼)
- BARCODE (超商條碼)
- ApplePay
- TWQR

---

## 電子發票 API 端點

### 基本 URL
- 正式環境: `https://einvoice.ecpay.com.tw`
- 測試環境: `https://einvoice-stage.ecpay.com.tw`

### B2C 電子發票 API
| API | 端點 | 說明 |
|-----|------|------|
| 開立發票 | /B2CInvoice/Issue | 一般開立發票 |
| 延遲開立 | /B2CInvoice/DelayIssue | 延遲/預約開立 |
| 觸發開立 | /B2CInvoice/TriggerIssue | 觸發延遲發票 |
| 作廢發票 | /B2CInvoice/Invalid | 作廢已開立發票 |
| 開立折讓 | /B2CInvoice/AllowanceByCollegiate | 開立折讓單 |
| 作廢折讓 | /B2CInvoice/AllowanceInvalid | 作廢折讓單 |
| 查詢發票 | /B2CInvoice/GetIssue | 查詢發票明細 |
| 發票通知 | /B2CInvoice/InvoiceNotify | 發送發票通知 |
| 手機載具驗證 | /B2CInvoice/CheckMobileBarCode | 驗證手機條碼 |
| 愛心碼驗證 | /B2CInvoice/CheckLoveCode | 驗證捐贈碼 |

### 載具類別代碼
| 代碼 | 說明 | 載具號碼格式 |
|------|------|-------------|
| 0 | 無載具 (紙本) | - |
| 1 | 綠界電子發票載具 | 會員編號 |
| 2 | 自然人憑證 | 2字母+14數字 (共16碼) |
| 3 | 手機條碼 | `/` + 7碼英數字 (共8碼) |

### 發票類別代碼
| 代碼 | 說明 |
|------|------|
| 07 | 一般稅額 |
| 08 | 特種稅額 |

### 課稅類別代碼
| 代碼 | 說明 |
|------|------|
| 1 | 應稅 |
| 2 | 零稅率 |
| 3 | 免稅 |
| 9 | 混合稅率 |

---

## CheckMacValue 加密流程

### 步驟
1. 將參數依照 Key 字母順序排序
2. 組成 `key1=value1&key2=value2...` 格式
3. 前後加上 HashKey 和 HashIV: `HashKey={}&...&HashIV={}`
4. URL Encode (小寫)
5. SHA256 加密
6. 轉大寫

### Python 範例
```python
import hashlib
import urllib.parse

def generate_check_mac_value(params, hash_key, hash_iv):
    # 1. 依 key 排序
    sorted_params = sorted(params.items())
    # 2. 組成查詢字串
    param_str = '&'.join(f'{k}={v}' for k, v in sorted_params)
    # 3. 加上 HashKey 和 HashIV
    raw_str = f'HashKey={hash_key}&{param_str}&HashIV={hash_iv}'
    # 4. URL Encode (小寫)
    encoded_str = urllib.parse.quote_plus(raw_str).lower()
    # 5. SHA256 加密並轉大寫
    return hashlib.sha256(encoded_str.encode('utf-8')).hexdigest().upper()
```

---

## 技術支援

- 綠界技術服務信箱: techsupport@ecpay.com.tw
- 商務洽詢: https://www.ecpay.com.tw/
- 測試環境後台: https://vendor-stage.ecpay.com.tw/

---

## 本地 SDK 檔案

已下載的 SDK 位於 `docs/ecpay_api/` 目錄：
- `python_sdk/` - Python 全方位金流 SDK
- `invoice_dotnet_sdk/` - .NET 電子發票 SDK
