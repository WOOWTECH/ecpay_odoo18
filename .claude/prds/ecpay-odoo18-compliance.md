---
name: ecpay-odoo18-compliance
description: Comprehensive Odoo 18 compliance audit and bug fixes for ECPay modules with production readiness
status: backlog
created: 2026-01-06T10:41:39Z
updated: 2026-01-07T01:07:42Z
---

# PRD: ECPay Odoo 18 Full Compliance & Production Readiness

## Executive Summary

This PRD defines the requirements for achieving full Odoo 18 compliance and production readiness for three ECPay modules (`ecpay_invoice_tw`, `ecpay_invoice_website`, `payment_ecpay`) that were migrated from Odoo 16 to Odoo 18.

While an initial migration was completed with critical bugs fixed (BUG-003 through BUG-006), three known issues remain unresolved (BUG-001, BUG-002, BUG-007), and a comprehensive audit is needed to ensure all code patterns, APIs, and architecture fully comply with Odoo 18 standards. Additionally, UI enhancements are required for the website checkout flow, and the modules must be validated for production deployment with real ECPay merchant credentials.

**Value Proposition:**
- Ensure 100% functionality in production Odoo 18 environments
- Enable Taiwan businesses to issue e-invoices and process payments via ECPay
- Reduce manual intervention in the e-commerce to invoice flow
- Provide a maintainable, well-documented, and tested codebase

## Problem Statement

### Current Situation
Three ECPay modules have been migrated from Odoo 16 to Odoo 18 with the following status:
- **10 test tasks completed** with 5 critical bugs fixed
- Modules work in ECPay sandbox/test mode
- Core invoice issuance, void, and allowance functions operational
- Payment gateway integration functional with all payment methods

### Remaining Problems

1. **BUG-001: Carrier Number Input Not Possible**
   - The `carrierNum` field on `account.move` is a readonly related field pointing to `ecpay_invoice_id.IIS_Carrier_Num`
   - Users cannot input mobile barcode (`/XXXXXXX`) or natural person certificate carrier numbers before issuing invoices
   - Impact: Manual invoices cannot use carrier types other than ECPay carrier

2. **BUG-002: Donation/Print Fields Readonly**
   - Fields `is_donation`, `is_print`, and `lovecode` are readonly on the invoice form
   - Users cannot manually set donation or print paper options when creating invoices directly
   - Impact: Manual invoices cannot be configured for donation or paper printing

3. **BUG-007: Settings Page Crash - KeyError 'group_mrp_routings'**
   - Opening Settings page causes server error: `KeyError: 'group_mrp_routings'`
   - Error occurs in `res.config.settings` model during `default_get()` and `_get_classified_fields()`
   - The ECPay invoice module inherits from `account.res_config_settings_view_form`
   - Possible cause: Field definition conflict or missing dependency with MRP module
   - Impact: **Critical** - Administrators cannot access Settings page to configure any module
   - Error location: `ecpay_invoice_tw/models/res_config_settings.py` inheritance

4. **Missing UI Elements in Website Checkout**
   - No input field for carrier number when selecting mobile barcode or natural person certificate
   - No input field for lovecode when selecting donation option
   - Impact: Website customers cannot use these carrier types or donate their invoices

5. **Unknown Compliance Gaps**
   - No comprehensive audit of all code against Odoo 18 best practices
   - Potential deprecated patterns, missing attributes, or inefficient queries not yet identified
   - Impact: Risk of future breakage or performance issues in production

6. **Production Readiness Unknown**
   - All testing performed in ECPay sandbox mode
   - No validation with production ECPay credentials
   - No performance testing under realistic load
   - Impact: Unknown behavior in production environment

### Why This Matters Now
- Taiwan e-invoice regulations require proper carrier number handling
- Businesses need donation invoice capability for customer service
- Production deployment is blocked until full compliance is verified
- Technical debt from migration needs to be addressed before further development

## User Stories

### Persona 1: E-Commerce Customer (Taiwan)
A customer purchasing products on an Odoo 18 e-commerce website who needs to receive a Taiwan e-invoice.

#### US-1.1: Select Mobile Barcode Carrier
**As an** e-commerce customer,
**I want to** enter my mobile barcode carrier number (`/XXXXXXX`) during checkout,
**So that** my e-invoice is stored in my government-linked mobile barcode account.

**Acceptance Criteria:**
- [ ] When I select "手機條碼" (Mobile Barcode) carrier type, an input field appears
- [ ] The input field validates the format (must start with `/` followed by 7 alphanumeric characters)
- [ ] Invalid format shows clear error message in Traditional Chinese
- [ ] Valid carrier number is saved to my order and transferred to the invoice
- [ ] After purchase, my e-invoice appears in my mobile barcode app (財政部電子發票整合服務平台)

#### US-1.2: Select Natural Person Certificate Carrier
**As an** e-commerce customer,
**I want to** enter my natural person certificate carrier number during checkout,
**So that** my e-invoice is stored in my certificate-linked account.

**Acceptance Criteria:**
- [ ] When I select "自然人憑證" carrier type, an input field appears
- [ ] The input field validates the format (2 uppercase letters + 14 digits)
- [ ] Invalid format shows clear error message
- [ ] Valid carrier number is saved and transferred to the invoice

#### US-1.3: Donate Invoice to Charity
**As an** e-commerce customer,
**I want to** donate my e-invoice to a registered charity during checkout,
**So that** the charity can claim the lottery winnings if my invoice number wins.

**Acceptance Criteria:**
- [ ] When I select "捐贈發票" (Donate Invoice), a lovecode input field appears
- [ ] The system validates the lovecode against ECPay's registered charity list
- [ ] Invalid lovecode shows clear error with suggestion to verify the code
- [ ] Valid lovecode is saved and the invoice is issued as a donation invoice
- [ ] The invoice clearly shows it was donated

#### US-1.4: Request Paper Invoice with Company Name
**As an** e-commerce customer (business buyer),
**I want to** request a paper invoice with my company's tax ID (統一編號),
**So that** I can use it for business expense reporting.

**Acceptance Criteria:**
- [ ] When I select "紙本發票" (Paper Invoice), company name and tax ID fields appear
- [ ] Tax ID format is validated (8 digits)
- [ ] Delivery address field is available and required
- [ ] Paper invoice is issued and mailed to the specified address

### Persona 2: Accounting Staff
An accounting department employee who creates and manages invoices in the Odoo backend.

#### US-2.1: Create Invoice with Custom Carrier
**As an** accounting staff member,
**I want to** create an invoice and specify any carrier type and number,
**So that** I can issue invoices for phone orders or special requests.

**Acceptance Criteria:**
- [ ] I can select any carrier type (ECPay, Mobile Barcode, Natural Person Cert) on the invoice form
- [ ] I can enter the carrier number for Mobile Barcode or Natural Person Cert
- [ ] The carrier number is validated before invoice issuance
- [ ] The invoice is issued with the correct carrier configuration

#### US-2.2: Create Donation Invoice Manually
**As an** accounting staff member,
**I want to** mark an invoice as a donation and enter the lovecode,
**So that** I can fulfill customer requests to donate their invoices.

**Acceptance Criteria:**
- [ ] I can toggle the "捐贈" (Donation) option on the invoice form
- [ ] When enabled, a lovecode input field becomes visible and required
- [ ] The lovecode is validated before invoice issuance
- [ ] The invoice is issued as a donation to the specified charity

#### US-2.3: Request Paper Invoice for Customer
**As an** accounting staff member,
**I want to** mark an invoice for paper printing and enter delivery details,
**So that** customers who need physical invoices can receive them.

**Acceptance Criteria:**
- [ ] I can toggle the "列印紙本" (Print Paper) option on the invoice form
- [ ] When enabled, company name and delivery address fields are visible
- [ ] Required fields are validated before invoice issuance

### Persona 3: System Administrator
A system administrator responsible for configuring and maintaining the Odoo instance.

#### US-3.1: Configure Production ECPay Credentials
**As a** system administrator,
**I want to** configure production ECPay credentials separately from test credentials,
**So that** I can switch between test and production modes safely.

**Acceptance Criteria:**
- [ ] Clear separation between test mode and production mode settings
- [ ] Production credentials can be entered without affecting test environment
- [ ] Visual indicator shows whether system is in test or production mode
- [ ] Validation prevents accidental production API calls in test mode

#### US-3.2: Monitor ECPay API Health
**As a** system administrator,
**I want to** see the status of ECPay API connectivity and recent transactions,
**So that** I can quickly identify and troubleshoot integration issues.

**Acceptance Criteria:**
- [ ] Dashboard or log showing recent ECPay API calls
- [ ] Success/failure status for each API call
- [ ] Error messages are logged with sufficient detail for debugging

### Persona 4: Developer
A developer responsible for maintaining and extending the ECPay modules.

#### US-4.1: Comprehensive Test Suite
**As a** developer,
**I want** automated tests covering all ECPay functionality,
**So that** I can make changes confidently without breaking existing features.

**Acceptance Criteria:**
- [ ] Unit tests for all model methods
- [ ] Integration tests for API communication
- [ ] UI tests for website checkout flow
- [ ] Tests can be run with `odoo-bin -i ecpay_invoice_tw --test-enable`
- [ ] Test coverage report available

#### US-4.2: Clear Documentation
**As a** developer,
**I want** comprehensive technical documentation,
**So that** I can understand the architecture and extend the modules.

**Acceptance Criteria:**
- [ ] Architecture overview with data flow diagrams
- [ ] API documentation for all public methods
- [ ] Configuration guide for ECPay settings
- [ ] Troubleshooting guide for common issues

## Requirements

### Functional Requirements

#### FR-1: Bug Fixes

##### FR-1.1: BUG-001 - Enable Carrier Number Input on Invoices
- **Priority:** High
- **Module:** ecpay_invoice_tw
- **Current State:** `carrierNum` is a readonly related field
- **Required Change:**
  - Add new editable field `input_carrier_num` for user input
  - Create onchange handler to validate format based on carrier type
  - Transfer `input_carrier_num` to ECPay API when issuing invoice
  - Update uniform.invoice with actual carrier number from ECPay response

##### FR-1.2: BUG-002 - Enable Donation/Print Fields on Invoices
- **Priority:** High
- **Module:** ecpay_invoice_tw
- **Current State:** `is_donation`, `is_print`, `lovecode` fields are readonly
- **Required Change:**
  - Remove readonly attribute from these fields (or make conditional)
  - Add onchange handler for `is_donation` to show/require `lovecode`
  - Add onchange handler for `is_print` to show/require address fields
  - Ensure mutual exclusivity: donation invoices cannot be paper invoices

##### FR-1.3: BUG-007 - Fix Settings Page KeyError
- **Priority:** Critical
- **Module:** ecpay_invoice_tw
- **Current State:** Settings page crashes with `KeyError: 'group_mrp_routings'`
- **Error Details:**
  - Error occurs on `res.config.settings` model during `onchange` → `default_get()` → `_get_classified_fields()`
  - The field `group_mrp_routings` is expected but doesn't exist
  - Triggered when ECPay module is installed without MRP module
- **Required Investigation:**
  - Check if `res_config_settings.py` incorrectly references MRP fields
  - Check if view XML inherits from a view that requires MRP
  - Check for incorrect field definitions using `implied_group` or `group` parameters
  - Check module dependencies in `__manifest__.py`
- **Required Fix:**
  - Remove any MRP-related field references
  - Ensure proper module dependencies
  - Validate Settings page loads correctly after fix
  - Test with and without MRP module installed

#### FR-2: Website Checkout Enhancements

##### FR-2.1: Mobile Barcode Carrier Input
- **Priority:** High
- **Module:** ecpay_invoice_website
- **Required Changes:**
  - Add conditional input field in checkout template
  - Show field only when "手機條碼" carrier type is selected
  - Client-side validation: `/[0-9A-Za-z+.-]{7}$/`
  - Server-side validation via `check_carrier_num` method
  - Save to sale order and transfer to invoice

##### FR-2.2: Natural Person Certificate Input
- **Priority:** High
- **Module:** ecpay_invoice_website
- **Required Changes:**
  - Add conditional input field in checkout template
  - Show field only when "自然人憑證" carrier type is selected
  - Client-side validation: `/^[A-Z]{2}[0-9]{14}$/`
  - Server-side validation via `check_carrier_num` method
  - Save to sale order and transfer to invoice

##### FR-2.3: Donation Lovecode Input
- **Priority:** High
- **Module:** ecpay_invoice_website
- **Required Changes:**
  - Add conditional input field in checkout template
  - Show field only when "捐贈發票" option is selected
  - Client-side validation for lovecode format (3-7 digits)
  - Server-side validation via `check_lovecode` method
  - Save to sale order and transfer to invoice

#### FR-3: Odoo 18 Compliance Audit

##### FR-3.1: Python Code Audit
- **Priority:** Medium
- **Scope:** All Python files in three modules
- **Checklist:**
  - [ ] All models have `_description` attribute
  - [ ] No use of deprecated `@api.multi` or `@api.one` decorators
  - [ ] No use of deprecated `name_get()` method (use `_compute_display_name`)
  - [ ] No use of deprecated `states` attribute in field definitions
  - [ ] No use of `is` for string/integer comparison (use `==`)
  - [ ] All `super()` calls use correct Odoo 18 syntax
  - [ ] No deprecated `context.get('active_id')` patterns
  - [ ] Proper use of `sudo()` for security elevation
  - [ ] No SQL injection vulnerabilities in raw SQL

##### FR-3.2: JavaScript Code Audit
- **Priority:** Medium
- **Scope:** All JavaScript files in three modules
- **Checklist:**
  - [ ] All files use `/** @odoo-module **/` header
  - [ ] No use of deprecated `odoo.define()` pattern
  - [ ] Correct import paths for Odoo 18:
    - `@web/legacy/js/public/public_widget` (not `web.public.widget`)
    - `@web/core/network/rpc` (not `web.rpc`)
    - `@payment/js/payment_form` (not `payment.payment_form`)
  - [ ] Proper `_super` binding before async operations
  - [ ] No deprecated jQuery patterns where modern alternatives exist

##### FR-3.3: XML View Audit
- **Priority:** Medium
- **Scope:** All XML files in three modules
- **Checklist:**
  - [ ] Correct view inheritance patterns for Odoo 18
  - [ ] No deprecated `position="attributes"` without proper target
  - [ ] Proper use of `t-` directives in QWeb templates
  - [ ] No inline JavaScript in templates (use external modules)

##### FR-3.4: Manifest Audit
- **Priority:** Low
- **Scope:** `__manifest__.py` in three modules
- **Checklist:**
  - [ ] Version matches `18.0.x.x.x` format
  - [ ] `license` field is present
  - [ ] Dependencies are accurate and minimal
  - [ ] Assets declared using Odoo 18 patterns

#### FR-4: Testing Requirements

##### FR-4.1: Unit Tests
- **Priority:** High
- **Coverage Target:** 80%+ for model methods
- **Test Cases:**
  - Invoice creation with each carrier type
  - Invoice void functionality
  - Allowance/credit note functionality
  - Carrier number validation (valid and invalid formats)
  - Lovecode validation
  - Payment transaction creation
  - Payment callback handling

##### FR-4.2: Integration Tests
- **Priority:** High
- **Test Cases:**
  - End-to-end invoice issuance with ECPay API (sandbox)
  - End-to-end payment flow with ECPay API (sandbox)
  - Website checkout to invoice flow
  - Invoice void with ECPay API
  - Allowance issuance with ECPay API

##### FR-4.3: Manual Test Protocol
- **Priority:** High
- **Test Scenarios:**
  - Complete purchase with each invoice type
  - Complete purchase with each payment method
  - Backend invoice creation with each carrier type
  - Invoice void and allowance operations
  - Error handling for invalid inputs

#### FR-5: Documentation

##### FR-5.1: User Guide
- **Priority:** High
- **Audience:** End users (accounting staff, administrators)
- **Content:**
  - Module installation and setup
  - ECPay account configuration (test and production)
  - Invoice operations guide
  - Website checkout configuration
  - Payment gateway setup
  - Troubleshooting common issues
  - FAQ section

##### FR-5.2: Technical Documentation
- **Priority:** Medium
- **Audience:** Developers
- **Content:**
  - Architecture overview
  - Data model diagrams
  - API reference
  - Extension guide
  - Testing guide

### Non-Functional Requirements

#### NFR-1: Performance
- Invoice issuance should complete within 10 seconds
- Payment redirect should complete within 5 seconds
- Website checkout should not add more than 500ms latency
- No N+1 query patterns in batch operations

#### NFR-2: Security
- All ECPay credentials stored encrypted in database
- No credentials logged in plain text
- HTTPS required for all ECPay communication
- CSRF protection on all forms
- Input validation on all user-provided data

#### NFR-3: Reliability
- Graceful handling of ECPay API timeouts
- Retry logic for transient failures
- Clear error messages for users when API fails
- Transaction logging for audit trail

#### NFR-4: Maintainability
- Code follows Odoo 18 conventions
- Consistent naming conventions across modules
- No dead code or commented-out sections
- Clear separation of concerns

#### NFR-5: Compatibility
- Compatible with Odoo 18.0 Community Edition
- Compatible with Odoo 18.0 Enterprise Edition
- Works with PostgreSQL 14+
- Works with Python 3.10+

## Success Criteria

### SC-1: All Known Bugs Fixed
- [ ] BUG-001 resolved: Users can input carrier numbers on invoices
- [ ] BUG-002 resolved: Users can set donation/print options on invoices
- [ ] BUG-007 resolved: Settings page loads without KeyError

### SC-2: Website Checkout Complete
- [ ] Mobile barcode carrier input functional and validated
- [ ] Natural person certificate input functional and validated
- [ ] Donation lovecode input functional and validated
- [ ] All inputs saved correctly to sale orders and transferred to invoices

### SC-3: Odoo 18 Compliance
- [ ] Zero deprecated patterns in Python code
- [ ] Zero deprecated patterns in JavaScript code
- [ ] Zero deprecated patterns in XML views
- [ ] All manifest files comply with Odoo 18 standards

### SC-4: Test Coverage
- [ ] Unit tests pass with 80%+ coverage
- [ ] Integration tests pass against ECPay sandbox
- [ ] Manual test protocol completed with 100% pass rate

### SC-5: Production Validation
- [ ] Modules validated in production-like environment
- [ ] ECPay production API tested (with test transactions)
- [ ] No critical/high severity issues in production validation

### SC-6: Documentation Complete
- [ ] User guide published and reviewed
- [ ] Technical documentation complete
- [ ] README updated with current information

## Constraints & Assumptions

### Constraints

1. **ECPay API Limitations**
   - Cannot test production API without real merchant account
   - Some API behaviors differ between sandbox and production
   - API rate limits may apply in production

2. **Odoo Framework Constraints**
   - Must work within Odoo's ORM and view framework
   - Cannot modify core Odoo modules
   - Must maintain upgrade compatibility

3. **Taiwan Regulatory Requirements**
   - E-invoice format must comply with 財政部 regulations
   - Carrier number formats are fixed by government
   - Lovecodes are managed by registered charities

4. **Resource Constraints**
   - Limited access to production ECPay environment
   - Testing requires live Odoo 18 instance

### Assumptions

1. ECPay sandbox API accurately reflects production behavior
2. Odoo 18 stable release is the target version (not nightly builds)
3. ECPay merchant account is available for production testing
4. Users have basic knowledge of Taiwan e-invoice system
5. Internet connectivity is available for ECPay API calls

## Out of Scope

The following items are explicitly NOT included in this PRD:

1. **New Payment Methods**
   - Adding LINE Pay, JKOPay, or other non-ECPay payment methods
   - Adding cryptocurrency payment options

2. **Multi-Language Support**
   - Translations beyond Traditional Chinese
   - User interface localization for other markets

3. **Mobile App Integration**
   - Native mobile app for invoice management
   - Push notifications for invoice status

4. **Advanced Reporting**
   - Business intelligence dashboards
   - Invoice analytics and trends

5. **Accounting Integration**
   - Integration with external accounting software
   - Automated reconciliation features

6. **Other Taiwan Tax Features**
   - 營業稅申報 (business tax filing)
   - 退稅 (tax refund) processing

7. **ECPay Non-Invoice Services**
   - ECPay logistics integration
   - ECPay customer service integration

## Dependencies

### Internal Dependencies

| Dependency | Type | Description |
|------------|------|-------------|
| Odoo 18 Base | Framework | Core Odoo 18 installation |
| account module | Odoo Module | Base accounting functionality |
| sale module | Odoo Module | Sales order management |
| payment module | Odoo Module | Payment provider framework |
| website_sale module | Odoo Module | E-commerce checkout |

### External Dependencies

| Dependency | Type | Description |
|------------|------|-------------|
| ECPay Invoice API | External API | E-invoice issuance service |
| ECPay Payment API | External API | Payment gateway service |
| pycryptodomex | Python Package | AES encryption for API security |
| PostgreSQL 14+ | Database | Data storage |

### Team Dependencies

| Dependency | Owner | Required By |
|------------|-------|-------------|
| ECPay Test Credentials | Business Team | Development start |
| ECPay Production Credentials | Business Team | Production validation |
| Odoo 18 Test Instance | IT Team | All testing |
| Code Review | Development Lead | Before release |

## Appendix

### A. ECPay Invoice Carrier Types

| Code | Name (Chinese) | Name (English) | Format |
|------|---------------|----------------|--------|
| 1 | 綠界科技電子發票載具 | ECPay Carrier | Auto-generated |
| 2 | 自然人憑證 | Natural Person Certificate | `[A-Z]{2}[0-9]{14}` |
| 3 | 手機條碼 | Mobile Barcode | `/[0-9A-Za-z+.-]{7}` |

### B. ECPay Payment Methods

| Code | Name (Chinese) | Name (English) |
|------|---------------|----------------|
| Credit | 信用卡 | Credit Card |
| Credit_3 | 信用卡 3期 | Credit Card 3 installments |
| Credit_6 | 信用卡 6期 | Credit Card 6 installments |
| Credit_12 | 信用卡 12期 | Credit Card 12 installments |
| WebATM | 網路 ATM | Web ATM |
| ATM | ATM 轉帳 | ATM Transfer |
| CVS | 超商代碼 | Convenience Store Code |
| BARCODE | 超商條碼 | Convenience Store Barcode |
| ApplePay | Apple Pay | Apple Pay |
| TWQR | 台灣 Pay | Taiwan Pay QR |
| BNPL | 先享後付 | Buy Now Pay Later |

### C. Related Documentation

- ECPay Official Documentation: `ECPay_user_manual_1.0.2.pdf`
- Taiwan E-Invoice Platform: https://www.einvoice.nat.gov.tw/
- Odoo 18 Development Guide: https://www.odoo.com/documentation/18.0/developer.html

### D. Bug Reference

| Bug ID | Module | Status | Priority | Description |
|--------|--------|--------|----------|-------------|
| BUG-001 | ecpay_invoice_tw | Open | High | carrierNum readonly field |
| BUG-002 | ecpay_invoice_tw | Open | High | Donation/print fields readonly |
| BUG-003 | ecpay_invoice_tw | Fixed | - | reverse_moves() kwargs |
| BUG-004 | ecpay_invoice_tw | Fixed | - | refund_method removed |
| BUG-005 | ecpay_invoice_website | Fixed | - | Parameter name mismatch |
| BUG-006 | All | Fixed | - | JS module loading, Boolean handling |
| BUG-007 | ecpay_invoice_tw | Open | **Critical** | Settings page crash - KeyError 'group_mrp_routings' |
| BUG-008 | payment_ecpay | Open | Medium | Missing `@api.depends` on `_compute_display_name` |
| BUG-009 | ecpay_invoice_tw | Open | Medium | Boolean comparison using `is` instead of `==` (12 locations) |
| BUG-010 | ecpay_invoice_tw | Open | High | `carrierNum` related field cannot be written to (same root as BUG-001) |
| BUG-011 | ecpay_invoice_tw | Open | High | `is_donation`/`is_print` readonly blocks UI (same root as BUG-002) |
| BUG-012 | payment_ecpay | Open | Low | SDK type comparison using `is` for types |
| BUG-013 | ecpay_invoice_tw | Open | High | Multiple readonly fields block website data flow |
| BUG-014 | ecpay_invoice_website | Open | Medium | ConfirmationDialog may fail in frontend context |
| BUG-015 | payment_ecpay | Open | Low | `any()` usage on recordset deprecated |

### E. BUG-007 Technical Details

**Error Log:**
```
Occured on woowtech-odoo.woowtech.io on model res.config.settings on 2026-01-06 03:05:07 GMT

Traceback:
  File "odoo/addons/base/models/res_config.py", line 270, in default_get
    classified = self._get_classified_fields(fields)
  File "odoo/addons/base/models/res_config.py", line 230, in _get_classified_fields
    field = self._fields[name]
KeyError: 'group_mrp_routings'
```

**Root Cause Analysis:**
- The error occurs when the Settings form tries to load fields
- `group_mrp_routings` is a field from the MRP (Manufacturing) module
- Some code in the inheritance chain references this field
- When MRP module is not installed, the field doesn't exist, causing KeyError

**Investigation Points:**
1. `ecpay_invoice_tw/models/res_config_settings.py` - Check for incorrect field references
2. `ecpay_invoice_tw/views/res_config_setting_view.xml` - Check inherited view
3. `account.res_config_settings_view_form` - Check base view for MRP references
4. Module dependencies - Verify no implicit MRP dependency

### F. BUG-008 through BUG-015 Technical Details (Architecture Review)

These bugs were identified through an architecture review comparing the modules against Odoo 18 best practices.

#### BUG-008: Missing `@api.depends` on `_compute_display_name`
- **File:** `payment_ecpay/models/payment_ecpay_model.py:21-23`
- **Issue:** `_compute_display_name` method lacks `@api.depends('name')` decorator
- **Fix:** Add `@api.depends('name')` above the method

#### BUG-009: Boolean Comparison Using `is` Instead of `==`
- **File:** `ecpay_invoice_tw/models/account_invoice.py`
- **Lines:** 62, 68, 168, 170, 172, 173, 179, 184, 241, 244, 246, 329
- **Examples:**
  - `if self.is_print is True` should be `if self.is_print`
  - `if self.carrierNum is False` should be `if not self.carrierNum`
- **Fix:** Replace `is True/False` with truthiness checks

#### BUG-010 & BUG-011: Related Fields Cannot Be Written To
- **Root cause:** Same as BUG-001/BUG-002, but identifies the ORM-level issue
- **Impact:** Code attempts to write to readonly related fields fail silently or raise errors

#### BUG-012: SDK Type Comparison Using `is`
- **File:** `payment_ecpay/sdk/ecpay_payment_sdk.py:242-248`
- **Issue:** `v.get('type') is str` should use `== str` or `isinstance()`
- **Fix:** Replace `is str` with `== str`

#### BUG-013: Multiple Readonly Fields Block Website Data Flow
- **File:** `ecpay_invoice_tw/models/account_invoice.py:40-44`
- **Fields affected:**
  - `lovecode` (line 40)
  - `ecpay_CustomerIdentifier` (line 42)
  - `ec_print_address` (line 43)
  - `ec_ident_name` (line 44)
- **Impact:** `sale_order._prepare_invoice()` cannot write these values when creating invoices
- **Fix:** Remove `readonly=True` from these fields

#### BUG-014: ConfirmationDialog May Fail in Frontend Context
- **File:** `ecpay_invoice_website/static/src/js/invoice.js:8, 336`
- **Issue:** `this.call('dialog', 'add', ConfirmationDialog, ...)` may not work in public widget context
- **Fix:** Use simpler alert mechanism or notification service

#### BUG-015: `any()` Usage on Recordset Deprecated
- **File:** `payment_ecpay/models/payment_transaction.py:224`
- **Issue:** `any(s)` on recordset is deprecated; use `bool(s)` or `if s:`
- **Fix:** Replace `any(s)` with `s` or `bool(s)`
