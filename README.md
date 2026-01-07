# ECPay Odoo 18 Modules

Taiwan ECPay (綠界科技) integration modules for Odoo 18, providing e-invoice and payment gateway functionality.

## Modules Overview

| Module | Description |
|--------|-------------|
| `ecpay_invoice_tw` | E-invoice core functionality for Taiwan Uniform Invoice |
| `ecpay_invoice_website` | E-invoice options on website checkout |
| `payment_ecpay` | ECPay payment gateway integration |

## Requirements

- Odoo 18.0 (Community or Enterprise)
- Python 3.10+
- ECPay merchant account
- Valid ECPay API credentials

## Installation

### 1. Copy Modules

Copy the three module folders to your Odoo addons directory:

```bash
cp -r ecpay_invoice_tw /path/to/odoo/addons/
cp -r ecpay_invoice_website /path/to/odoo/addons/
cp -r payment_ecpay /path/to/odoo/addons/
```

### 2. Update Apps List

1. Go to **Apps** menu
2. Click **Update Apps List**
3. Search for "ecpay"

### 3. Install Modules

Install in this order:
1. **ECPay 綠界第三方電子發票模組** (ecpay_invoice_tw)
2. **ECPay 綠界第三方電子發票模組-電商網站前台** (ecpay_invoice_website)
3. **ECPay 綠界第三方金流模組** (payment_ecpay)

---

## Configuration

### E-Invoice Module Setup

#### Step 1: Access Invoice Settings

Navigate to: **Invoicing** → **Configuration** → **Settings** → **ECPay E-Invoice**

![Invoice Settings](screenshots/01-invoice-settings.png)

#### Step 2: Configure ECPay Credentials

Fill in your ECPay merchant credentials:

| Field | Description |
|-------|-------------|
| **Merchant ID** | Your ECPay merchant ID |
| **Hash Key** | ECPay Hash Key for API authentication |
| **Hash IV** | ECPay Hash IV for API authentication |
| **Test Mode** | Enable for sandbox testing |

![Invoice Config Detail](screenshots/02-invoice-config-detail.png)

> **Note:** Enable "Test Mode" when using ECPay sandbox credentials for testing.

---

### Payment Module Setup

#### Step 1: Access Payment Providers

Navigate to: **Invoicing** → **Configuration** → **Payment Providers**

#### Step 2: Configure ECPay Payment Provider

Click on **ECPay 綠界第三方支付** and configure:

![Payment Config](screenshots/03-payment-config.png)

| Field | Description |
|-------|-------------|
| **State** | Set to "Enabled" or "Test Mode" |
| **Merchant ID** | Your ECPay merchant ID |
| **Hash Key** | ECPay Hash Key |
| **Hash IV** | ECPay Hash IV |
| **Payment Methods** | Enable Credit, ATM, CVS, Barcode as needed |

---

## User Guide

### Creating E-Invoices

#### Step 1: Create and Post Invoice

1. Go to **Invoicing** → **Customers** → **Invoices**
2. Create a new invoice or select an existing draft

![Invoice List](screenshots/04-invoice-list.png)

3. Before posting, configure the ECPay invoice settings in the **綠界電子發票** tab:

![ECPay Invoice Tab](screenshots/05-invoice-ecpay-tab.png)

4. Click **Confirm** to post the invoice

![Posted Invoice](screenshots/06-posted-invoice.png)

#### Step 2: Issue E-Invoice to ECPay

After posting the invoice, click the **開立發票** (Issue Invoice) button:

![Invoice Issued](screenshots/07-invoice-issued.png)

The system will:
- Call ECPay API to issue the e-invoice
- Store the invoice number and random code
- Update the invoice status

---

### E-Invoice Carrier Types

The module supports multiple carrier types for electronic invoices:

![Carrier Options](screenshots/08-carrier-options.png)

| Carrier Type | Description | Carrier Number Format |
|--------------|-------------|----------------------|
| **綠界科技電子發票載具** | ECPay's own carrier (default) | Not required |
| **消費者自然人憑證** | Natural Person Certificate | 16 characters: 2 uppercase letters + 14 digits (e.g., `AB12345678901234`) |
| **消費者手機條碼** | Mobile Barcode | 8 characters: `/` + 7 alphanumeric characters (e.g., `/ABC+123`) |

#### Carrier Number Input

When selecting carrier type 2 (自然人憑證) or type 3 (手機條碼), a carrier number input field will appear:

1. **自然人憑證 (Natural Person Certificate)**
   - Format: 2 uppercase letters followed by 14 digits
   - Example: `AB12345678901234`
   - Total length: 16 characters

2. **手機條碼 (Mobile Barcode)**
   - Format: `/` followed by 7 characters (letters, numbers, `+`, `-`, `.`)
   - Example: `/ABC+123` or `/-12.456`
   - Total length: 8 characters
   - The leading `/` is required

#### Donation Invoices

For donation invoices, select "捐贈" and enter the Love Code:

![Donation Invoice](screenshots/09-donation-invoice.png)

**Love Code (愛心碼) Format:**
- 3 to 7 digits
- Common examples:
  - `168` - Common charitable code
  - `25885` - Social welfare organizations
  - `919` - Cancer Foundation
- Verify codes at: https://www.einvoice.nat.gov.tw/

---

### Voiding Invoices

To void an issued e-invoice:

1. Open the posted invoice
2. Click **作廢發票** (Void Invoice)
3. The system calls ECPay to void the invoice

![Voided Invoice](screenshots/10-invoice-voided.png)

---

### Creating Allowance (折讓)

When creating a credit note for a partial refund:

1. Open the original invoice
2. Click **Credit Note** → **Add Credit Note**
3. Post the credit note
4. The system automatically creates an allowance in ECPay

![Allowance Issued](screenshots/11-allowance-issued.png)

---

## Website Checkout Guide

### Step 1: Add Products to Cart

Browse products and add them to your cart:

![Product Page](screenshots/12-product-page.png)

![Shopping Cart](screenshots/13-shopping-cart.png)

### Step 2: Checkout Process

Proceed to checkout and enter delivery information:

![Checkout Delivery](screenshots/14-checkout-delivery.png)

### Step 3: E-Invoice Options

On the payment page, you'll see the e-invoice options:

![Checkout E-Invoice](screenshots/15-checkout-einvoice.png)

#### Available Options:

**Electronic Invoice (電子發票)**

Select carrier type from dropdown:

![Carrier Dropdown](screenshots/16-carrier-dropdown.png)

- **會員載具** - ECPay member carrier
- **自然人憑證** - Natural person certificate (enter 16-digit code)
- **手機條碼** - Mobile barcode (format: /XXXXXXX)

**Paper Invoice (紙本發票)**

Select for printed invoice delivery:

![Paper Invoice](screenshots/17-paper-invoice.png)

- Enter delivery address
- Optionally add company name and tax ID (統一編號)

**Donation (捐贈發票)**

- Enter Love Code (愛心碼)
- System validates the code with ECPay

### Step 4: Payment

Select ECPay as payment method and proceed:

![Payment Gateway](screenshots/18-payment-gateway.png)

Complete payment on ECPay's secure page:

![Payment Success](screenshots/19-payment-success.png)

### Step 5: Order Confirmation

After successful payment, you'll see order confirmation:

![Order Confirmed](screenshots/20-order-confirmed.png)

---

## Admin Features

### Viewing E-Invoice Data on Orders

Sales orders store e-invoice preferences in the **綠界電商資料** tab:

| Field | Description |
|-------|-------------|
| **列印** | Paper invoice requested |
| **捐贈** | Donation invoice |
| **愛心碼** | Love Code for donation |
| **發票抬頭** | Company name |
| **統一編號** | Tax ID |
| **發票寄送地址** | Invoice delivery address |
| **載具類別** | Carrier type |
| **載具號碼** | Carrier number |

### Viewing Payment Records

Payment transactions are recorded with:

| Field | Description |
|-------|-------------|
| **廠商訂單編號** | Merchant order number |
| **付款日期** | Payment date |
| **付款方式** | Payment method (Credit/ATM/CVS) |
| **付款狀態** | Payment status |
| **交易訊息** | Transaction message |
| **交易金額** | Transaction amount |
| **綠界金流訂單編號** | ECPay transaction ID |

---

## Troubleshooting

### Common Issues

#### Settings Page Error (BUG-007 - Fixed in v18.0.1.1.0)

**Problem:** Settings page crashes with `KeyError: 'ecpay_invoice_mode'`

**Solution:** Update to version 18.0.1.1.0 or later. This was caused by a missing inverse method for the computed settings field.

#### E-Invoice Not Issuing

**Problem:** "開立發票" button doesn't work

**Solutions:**
1. Verify ECPay credentials in settings
2. Check if invoice is in "Posted" state
3. Review Odoo logs for API errors:
   ```bash
   tail -f /var/log/odoo/odoo.log | grep -i ecpay
   ```

#### Cannot Enter Carrier Number (BUG-010 - Fixed in v18.0.1.1.0)

**Problem:** Carrier number field is read-only

**Solutions:**
1. Update to version 18.0.1.1.0 or later
2. Ensure you have selected carrier type 2 (自然人憑證) or 3 (手機條碼) first
3. The field only appears when a carrier type requiring input is selected

#### Cannot Toggle Donation/Print Options (BUG-011 - Fixed in v18.0.1.1.0)

**Problem:** Checkboxes for donation and print invoice are read-only

**Solution:** Update to version 18.0.1.1.0 or later. The readonly attributes have been removed from these fields.

#### Payment Redirect Fails

**Problem:** Payment doesn't redirect to ECPay

**Solutions:**
1. Verify payment provider is enabled
2. Check Hash Key/Hash IV configuration
3. Ensure website URL is correct in ECPay merchant settings

#### E-Invoice Options Not Saved (BUG-004/005 - Fixed in v18.0.1.1.0)

**Problem:** Carrier type or carrier number not saved to order/invoice

**Solutions:**
1. Update to version 18.0.1.1.0 or later
2. Clear browser cache (Ctrl+Shift+R)
3. Check browser console for JavaScript errors
4. Verify `ecpay_invoice_website` module is installed

#### Invalid Carrier Number Error

**Problem:** "載具號碼錯誤" error at checkout

**Solutions:**
1. **Mobile Barcode (手機條碼):** Must start with `/` and be exactly 8 characters (e.g., `/ABC+123`)
2. **Natural Person (自然人憑證):** Must be 16 characters - 2 letters + 14 digits (e.g., `AB12345678901234`)
3. Check for extra spaces before or after the carrier number

#### Credit Note Error (BUG-003/004 - Fixed in v18.0.1.0.0)

**Problem:** Error when creating credit note

**Solution:** Ensure you're using Odoo 18.0.1.0.0 or later version of these modules which includes the fix for `reverse_moves()` compatibility.

### Debug Mode

Enable debug mode to see detailed error messages:

1. Go to **Settings** → **Activate Developer Mode**
2. Or add `?debug=1` to URL

### Log Files

Check Odoo logs for ECPay API responses:

```bash
# Filter ECPay related logs
grep -i "ecpay" /var/log/odoo/odoo.log

# Watch logs in real-time
tail -f /var/log/odoo/odoo.log | grep -i "ecpay"
```

---

## API Reference

### E-Invoice API Methods

| Method | Description |
|--------|-------------|
| `issue_ecpay_invoice()` | Issue e-invoice to ECPay |
| `void_ecpay_invoice()` | Void issued e-invoice |
| `check_carrier_num()` | Validate mobile barcode |
| `check_lovecode()` | Validate donation code |

### Payment API Methods

| Method | Description |
|--------|-------------|
| `_get_default_payment_method_codes()` | Get supported payment methods |
| `_get_redirect_form_view()` | Generate payment redirect form |
| `_process_notification_data()` | Handle ECPay callback |

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 18.0.1.1.0 | 2026-01-07 | Odoo 18 compliance fixes (BUG-007 to BUG-015) |
| 18.0.1.0.0 | 2026-01-02 | Initial Odoo 18 migration (BUG-003 to BUG-006) |

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## License

LGPL-3.0 or later - See [LICENSE](LICENSE) for details.

## Support

- **ECPay Documentation:** https://www.ecpay.com.tw/Develop/Index
- **ECPay Test Environment:** https://vendor-stage.ecpay.com.tw/
- **Odoo Documentation:** https://www.odoo.com/documentation/18.0/

---

## Credits

- Original Odoo 16 module by ECPay/ACE Solutions
- Odoo 18 migration and bug fixes by development team
