# ECPay Odoo 18 Modules - Test Report

## Summary
- **Epic:** ecpay-odoo18-modules-review-test
- **Branch:** epic/ecpay-odoo18-modules-review-test
- **Started:** 2025-12-30T13:42:27Z
- **Status:** In Progress

| Metric | Value |
|--------|-------|
| Total Tasks | 10 |
| Completed | 5 |
| In Progress | 0 |
| Pending | 5 |
| Success Rate | 50% |

## Task Summaries

### Task 001: Static Code Review & Odoo 18 Compatibility Audit
**Status:** ✅ PASSED
**Completed:** 2025-12-30T13:44:52Z

**Summary:**
- All Python files pass syntax validation
- No deprecated Odoo 16 APIs found (name_get, @api.multi)
- No `states=` attribute in field definitions (only comments)

**Issues Found & Fixed:**
| Issue | File | Line | Fix | Commit |
|-------|------|------|-----|--------|
| Missing `_description` | `ecpay_invoice_tw/report/uniform_invoice.py` | 8 | Added `_description = 'ECPay Invoice Report'` | b40c2dc |
| Missing `_description` | `payment_ecpay/models/order_ecpay_model.py` | 7 | Added `_description = 'ECPay Order Information'` | b40c2dc |
| Syntax warning (`is` vs `==`) | `payment_ecpay/controllers/ecpay_payment_sdk.py` | 531,533,535 | Changed `is '1'` to `== '1'` | b40c2dc |

**Non-Critical Issues (Documented):**
| Issue | File | Notes |
|-------|------|-------|
| Hardcoded test credentials | `ecpay_invoice_tw/models/company.py:10-12` | ECPay sandbox defaults - acceptable for testing |

**Security Audit:**
- ✅ No production credentials hardcoded
- ✅ Test credentials are ECPay sandbox defaults
- ✅ No API keys in code

---

### Task 002: Module Installation & Configuration Verification
**Status:** ✅ PASSED
**Completed:** 2025-12-31T10:00:00Z

**Summary:**
- All 3 ECPay modules installed and verified in Odoo 18
- ECPay Invoice module configured with test credentials
- ECPay Payment module configured (disabled, ready for testing)

**Modules Verified:**
| Module | Status | Version |
|--------|--------|---------|
| ecpay_invoice_tw | Installed | 18.0.1.0.0 |
| ecpay_invoice_website | Installed | 18.0.1.0.0 |
| payment_ecpay | Installed | 18.0.1.0.0 |

**ECPay Invoice Configuration:**
- Mode: Test (綠界測試環境)
- Merchant ID: 2000132
- Auto Issue: Manual (手動)
- Seller Tax ID: 53538851

**ECPay Payment Configuration:**
- Status: Disabled (停用) - Ready for testing
- Merchant ID: 3002607
- Payment Methods: Credit Card, Apple Pay, ATM, CVS, BNPL, TWQR

**Screenshots:** 004-009

---

### Task 003: Invoice Module - Basic Invoice Creation Tests
**Status:** ✅ PASSED
**Completed:** 2025-12-31T10:10:00Z

**Summary:**
- Successfully created and posted invoice INV/2025/00002
- ECPay e-invoice tab displays correctly with all fields
- Address validation works correctly (requires customer address)
- Successfully issued ECPay e-invoice via API

**Test Results:**
| Test Case | Result | Details |
|-----------|--------|---------|
| ECPay tab visibility | ✅ PASS | Tab displays on invoice form |
| Invoice posting | ✅ PASS | Confirm button works |
| Address validation | ✅ PASS | Shows error when address missing |
| ECPay invoice issuance | ✅ PASS | Invoice DS60014218 issued |
| Uniform Invoice record | ✅ PASS | All data stored correctly |

**ECPay Invoice Issued:**
- 統一發票號碼: **DS60014218**
- 發票月份: 114年11-12月
- 合作特店編號: 2000132
- 發票金額: 100
- 載具類別: 綠界科技電子發票載具
- 發票狀態: 已開電子發票

**Screenshots:** 010-017

---

### Task 004: Invoice Module - Carrier Types & Donation Tests
**Status:** ✅ PASSED (with bugs found)
**Completed:** 2025-12-31T10:30:00Z

**Summary:**
- ECPay carrier type (綠界科技電子發票載具) works correctly with auto-generated carrier number
- Mobile barcode and Natural Person Certificate carrier types have implementation issues
- Donation and print paper options cannot be set directly on invoices (readonly fields)

**Test Results:**
| Test Case | Result | Details |
|-----------|--------|---------|
| ECPay carrier type | ✅ PASS | Auto-generates carrier number correctly |
| Mobile barcode carrier | ⚠️ BUG | carrierNum field is readonly related field |
| Natural person certificate | ⚠️ BUG | Same issue as mobile barcode |
| Donation feature | ⚠️ LIMITATION | is_donation field is readonly |
| Print paper option | ⚠️ LIMITATION | is_print field is readonly |

**ECPay Invoices Issued:**
| Invoice | ECPay Number | Carrier Type | Carrier Number |
|---------|--------------|--------------|----------------|
| INV/2025/00003 | DS60014238 | 綠界科技電子發票載具 | 8F69AAC93FC067849ABBE438F69CD3B3 |
| INV/2025/00004 | DS60014241 | 綠界科技電子發票載具 | 8F69AAC93FC067849ABBE438F69CD3B3 |

**Bugs Found:**
| Bug | File | Line | Description |
|-----|------|------|-------------|
| BUG-001 | `account_invoice.py` | 41 | `carrierNum` is a readonly related field pointing to `ecpay_invoice_id.IIS_Carrier_Num`. Cannot be edited before invoice issuance. |
| BUG-002 | `account_invoice.py` | 34-35, 40 | `is_donation`, `is_print`, `lovecode` fields are readonly. Cannot be set on invoices via UI. |

**Design Notes:**
- Carrier number for mobile barcode/natural person cert must be entered via sale order or website checkout
- Donation options require website checkout flow (ecpay_invoice_website module)

**Screenshots:** 018-022

---

### Task 005: Invoice Module - Void & Allowance Tests
**Status:** ✅ PASSED (with bugs fixed)
**Completed:** 2025-12-31T11:10:00Z

**Summary:**
- Void function works correctly after bug fix
- Allowance (折讓) function works correctly after two bug fixes
- Two critical Odoo 18 compatibility bugs found and fixed

**Test Results:**
| Test Case | Result | Details |
|-----------|--------|---------|
| Void invoice (作廢) | ✅ PASS | INV/2025/00004 (DS60014241) voided successfully |
| Credit note creation | ✅ PASS | RINV/2025/00001 created from INV/2025/00003 |
| Allowance issuance (折讓) | ✅ PASS | Allowance 2025123111082163 issued via ECPay API |
| Remaining allowance update | ✅ PASS | 剩餘可折讓金額 changed from 115 to 0 |

**Void Test Details:**
- Invoice: INV/2025/00004
- ECPay Number: DS60014241
- Void Reason: 測試作廢
- Result: 電子發票狀態 → 已作廢

**Allowance Test Details:**
- Original Invoice: INV/2025/00003 (DS60014238)
- Credit Note: RINV/2025/00001
- Allowance Number: 2025123111082163
- Allowance Amount: $115.00
- Result: 電子發票狀態 → 已折讓, 剩餘可折讓金額 → 0

**Critical Bugs Found & Fixed:**
| Bug | File | Issue | Fix |
|-----|------|-------|-----|
| BUG-003 | `account_move_reversal.py:10` | `reverse_moves()` missing `**kwargs`, Odoo 18 passes `is_modify` parameter | Changed to `reverse_moves(self, **kwargs)` |
| BUG-004 | `account_move_reversal.py:31` | `self.refund_method` attribute removed in Odoo 18 | Replaced with `kwargs.get('is_modify', False)` |

**Screenshots:** 023-030

---

### Task 006: Payment Module - Payment Flow Tests
**Status:** 🔄 PENDING
**Depends on:** Task 002

---

### Task 007: Payment Module - Callback & Status Tests
**Status:** 🔄 PENDING
**Depends on:** Task 006

---

### Task 008: Website Module - Checkout Invoice Options Tests
**Status:** 🔄 PENDING
**Depends on:** Task 003, 004

---

### Task 009: Integration Test - Full Purchase Flow
**Status:** 🔄 PENDING
**Depends on:** Task 003-008

---

### Task 010: Final Report & Documentation
**Status:** 🔄 PENDING
**Depends on:** All tasks

---

## Bug Fixes
| Issue | File | Fix | Commit |
|-------|------|-----|--------|
| Missing _description | uniform_invoice.py | Added model description | b40c2dc |
| Missing _description | order_ecpay_model.py | Added model description | b40c2dc |
| String comparison warning | ecpay_payment_sdk.py | Use == instead of is | b40c2dc |
| BUG-003: Missing kwargs | account_move_reversal.py | Added `**kwargs` to `reverse_moves()` | f0435c1 |
| BUG-004: refund_method removed | account_move_reversal.py | Use `kwargs.get('is_modify')` | f0435c1 |

## Known Issues (Not Fixed)
| Issue | File | Description | Recommendation |
|-------|------|-------------|----------------|
| BUG-001 | account_invoice.py:41 | `carrierNum` is readonly related field, cannot store user input | Change to regular Char field with onchange handler |
| BUG-002 | account_invoice.py:34-40 | Donation/print fields are readonly, cannot be set via UI | Remove readonly or add wizard for manual entry |

## Screenshots
| # | Filename | Description |
|---|----------|-------------|
| 001 | 001-odoo-login-page.png | Odoo login page |
| 002 | 002-odoo-dashboard-logged-in.png | Dashboard after login |
| 003 | 003-odoo-apps-list.png | Apps list overview |
| 004 | 004-ecpay-modules-filtered.png | ECPay modules search (3/3) |
| 005 | 005-ecpay-invoice-module-info.png | ECPay Invoice module info |
| 006 | 006-ecpay-invoice-settings.png | Invoice settings tab |
| 007 | 007-ecpay-invoice-config-detail.png | ECPay invoice configuration |
| 008 | 008-payment-providers-list.png | Payment providers list |
| 009 | 009-ecpay-payment-config.png | ECPay payment configuration |
| 010 | 010-invoice-list.png | Invoice list view |
| 011 | 011-draft-invoice-form.png | Draft invoice form |
| 012 | 012-ecpay-invoice-tab.png | ECPay invoice tab fields |
| 013 | 013-posted-invoice-with-ecpay-button.png | Posted invoice with issue button |
| 014 | 014-ecpay-address-validation-error.png | Address validation error |
| 015 | 015-customer-profile-no-address.png | Customer profile without address |
| 016 | 016-ecpay-invoice-issued-success.png | ECPay invoice issued successfully |
| 017 | 017-uniform-invoice-record.png | Uniform Invoice record details |
| 018 | 018-ecpay-tab-carrier-options.png | ECPay tab carrier type options |
| 019 | 019-mobile-barcode-carrier-selected.png | Mobile barcode carrier selected |
| 020 | 020-mobile-barcode-carrier-number-required.png | Validation error for carrier number |
| 021 | 021-ecpay-carrier-invoice-issued.png | INV/2025/00003 with ECPay carrier issued |
| 022 | 022-donation-test-invoice-issued.png | INV/2025/00004 issued for donation test |
| 023 | 023-ecpay-invoice-voided.png | INV/2025/00004 voided successfully |
| 024 | 024-ecpay-invoice-for-allowance-test.png | INV/2025/00003 ready for allowance test |
| 025 | 025-credit-note-error-reverse-moves.png | BUG-003: reverse_moves kwargs error |
| 026 | 026-credit-note-error-refund-method.png | BUG-004: refund_method attribute error |
| 027 | 027-credit-note-created-draft.png | RINV/2025/00001 draft created |
| 028 | 028-credit-note-ecpay-tab.png | Credit note linked to original invoice |
| 029 | 029-credit-note-posted.png | Credit note posted with allowance button |
| 030 | 030-ecpay-allowance-issued-success.png | ECPay allowance issued successfully |

## Recommendations
1. Consider removing hardcoded test credentials from company.py defaults
2. Document ECPay sandbox vs production configuration clearly
3. **BUG-001 Fix:** Change `carrierNum` field from related field to regular Char field to allow user input for mobile barcode and natural person certificate carriers
4. **BUG-002 Fix:** Either remove readonly attribute from donation/print fields, or create a wizard to allow manual entry when creating invoices directly (not via e-commerce)
5. Consider adding a separate `input_carrier_num` field for user input before issuing invoice
