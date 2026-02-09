---
name: ecpay-odoo18-modules-review-test
description: Code review and comprehensive live testing for ECPay Odoo 18 invoice and payment modules
status: backlog
created: 2025-12-30T10:35:41Z
---

# PRD: ECPay Odoo 18 Modules Code Review & Live Testing

## Executive Summary

This project involves comprehensive code review and live instance testing of three ECPay integration modules for Odoo 18:
1. **ecpay_invoice_tw** - Taiwan Electronic Invoice (電子發票) integration
2. **ecpay_invoice_website** - Website/eCommerce frontend for invoice options
3. **payment_ecpay** - ECPay Payment Gateway integration

The goal is to ensure 100% functionality of all features in a live Odoo 18 environment, identify and fix any compatibility issues from the Odoo 16→18 migration, and validate compliance with Odoo 18 architecture standards.

## Problem Statement

### What problem are we solving?
These three modules were migrated from Odoo 16 to Odoo 18 and require thorough validation to ensure:
- No compile errors or import issues
- Compliance with Odoo 18 architecture (deprecated APIs, field changes)
- All business functions work correctly end-to-end
- ECPay API integrations function properly in both test and production modes

### Why is this important now?
- The modules are already deployed to a live Odoo 18 instance
- Business continuity depends on correct invoice generation and payment processing
- Taiwan legal requirements mandate proper electronic invoice (電子發票) handling
- Any bugs could result in financial discrepancies or compliance issues

## Module Analysis

### Module 1: ecpay_invoice_tw (Taiwan Electronic Invoice)

**Purpose**: Backend integration with ECPay for Taiwan electronic invoices (電子發票)

**Key Features**:
- B2B and B2C invoice generation via ECPay API
- Invoice void (作廢) functionality
- Invoice allowance/discount (折讓) functionality
- Carrier type support:
  - Type 1: ECPay electronic carrier (綠界科技電子發票載具)
  - Type 2: Certificate barcode (自然人憑證)
  - Type 3: Mobile barcode (手機條碼)
- Donation (捐贈) support with love code (愛心碼)
- Print invoice option
- Tax handling (含稅/未稅)
- Automatic invoice on post OR manual invoice creation
- Invoice status tracking (to invoice → invoiced → invalid → discounted)

**Dependencies**: account, sale, stock, pycryptodomex

**Key Files**:
- `models/account_invoice.py` - AccountMove inheritance, invoice creation logic
- `models/uniform_invoice.py` - UniformInvoice model for invoice records
- `models/res_config_settings.py` - Company settings for ECPay credentials
- `sdk/ecpay_main.py` - ECPay SDK integration
- `wizard/` - Invoice void and allowance wizards

### Module 2: ecpay_invoice_website (Website Frontend)

**Purpose**: Frontend extension for eCommerce checkout invoice options

**Key Features**:
- Customer invoice type selection during checkout
- Mobile barcode input validation
- Love code (donation) input
- Business identifier (統一編號) input for B2B
- Print invoice address input

**Dependencies**: ecpay_invoice_tw, website_sale

**Key Files**:
- `views/website_sale.xml` - Checkout page modifications
- `static/src/js/invoice.js` - Frontend validation logic

### Module 3: payment_ecpay (Payment Gateway)

**Purpose**: ECPay payment provider integration for Odoo

**Key Features**:
- Payment Methods:
  - Credit card (信用卡一次付清)
  - Credit card installment (分期: 3, 6, 12, 18, 24 periods)
  - WebATM (網路ATM)
  - ATM virtual account (自動櫃員機ATM)
  - CVS convenience store code (超商代碼)
  - Barcode convenience store (超商條碼)
  - Apple Pay
  - BNPL - Buy Now Pay Later (無卡分期)
  - TWQR mobile payment (行動支付)
- Configurable expiration dates for ATM/CVS/Barcode
- Transaction status handling (done/pending/error)
- CheckMacValue verification for security
- Callback URL handling

**Dependencies**: payment, sale_management, website_sale

**Key Files**:
- `models/payment_ecpay_model.py` - PaymentProvider extension
- `models/payment_transaction.py` - PaymentTransaction handling
- `controllers/main.py` - Callback endpoints
- `sdk/ecpay_payment_sdk.py` - Payment SDK

## User Stories

### Invoice Module User Stories

#### US-INV-001: Admin Creates Manual Invoice
**As a** sales admin
**I want to** manually create an electronic invoice from an Odoo invoice
**So that** I can generate e-invoices for completed sales

**Acceptance Criteria**:
- [ ] "Create E-Invoice" button visible on customer invoice
- [ ] Invoice generated successfully on ECPay
- [ ] Invoice number stored in Odoo
- [ ] Invoice status updated to "invoiced"
- [ ] QR codes and barcode data retrieved

#### US-INV-002: Automatic Invoice on Post
**As a** system
**When** a customer invoice is posted and company is set to "automatic"
**Then** electronic invoice should be created automatically

**Acceptance Criteria**:
- [ ] Invoice created on post action
- [ ] No user intervention required
- [ ] Error handling if ECPay API fails

#### US-INV-003: Invoice with Mobile Barcode
**As a** customer
**I want to** store my invoice on my mobile barcode carrier
**So that** I don't need paper invoices

**Acceptance Criteria**:
- [ ] Mobile barcode validation via ECPay API
- [ ] Carrier type set correctly
- [ ] No print flag set

#### US-INV-004: Invoice Donation
**As a** customer
**I want to** donate my invoice to a charity
**So that** I can support charitable organizations

**Acceptance Criteria**:
- [ ] Love code validation via ECPay API
- [ ] Donation flag set correctly
- [ ] Invoice not printed

#### US-INV-005: B2B Invoice with Business ID
**As a** business customer
**I want to** receive an invoice with my company's tax ID (統一編號)
**So that** I can claim business expenses

**Acceptance Criteria**:
- [ ] Business identifier included in invoice
- [ ] Invoice category set to B2B
- [ ] Print flag set to true

#### US-INV-006: Invoice Void
**As a** sales admin
**I want to** void an electronic invoice
**So that** I can cancel incorrect invoices

**Acceptance Criteria**:
- [ ] Void wizard opens correctly
- [ ] Void API called successfully
- [ ] Invoice status updated to "invalid"

#### US-INV-007: Invoice Allowance (Discount)
**As a** sales admin
**I want to** create an allowance for a partial refund
**So that** the invoice amount is adjusted correctly

**Acceptance Criteria**:
- [ ] Allowance created from credit note
- [ ] Allowance number received from ECPay
- [ ] Remaining allowance amount updated

### Payment Module User Stories

#### US-PAY-001: Credit Card Payment
**As a** customer
**I want to** pay with my credit card
**So that** I can complete my purchase immediately

**Acceptance Criteria**:
- [ ] Redirect to ECPay payment page
- [ ] Successful payment returns to shop
- [ ] Transaction marked as done
- [ ] Order confirmed

#### US-PAY-002: Credit Card Installment
**As a** customer
**I want to** pay with credit card installments
**So that** I can spread my payment over time

**Acceptance Criteria**:
- [ ] Installment options displayed
- [ ] Selected period sent to ECPay
- [ ] Payment processed correctly

#### US-PAY-003: ATM Virtual Account
**As a** customer
**I want to** receive an ATM virtual account
**So that** I can pay via bank transfer

**Acceptance Criteria**:
- [ ] Virtual account number generated
- [ ] Transaction set to pending
- [ ] Account expiration date correct
- [ ] Payment confirmation on callback

#### US-PAY-004: CVS Convenience Store Code
**As a** customer
**I want to** receive a convenience store payment code
**So that** I can pay at 7-11/FamilyMart

**Acceptance Criteria**:
- [ ] Payment code generated
- [ ] Transaction set to pending
- [ ] Store expiration date correct
- [ ] Payment confirmation on callback

#### US-PAY-005: Barcode Payment
**As a** customer
**I want to** receive a barcode for convenience store payment
**So that** I can pay at convenience stores

**Acceptance Criteria**:
- [ ] Barcode generated
- [ ] Transaction set to pending
- [ ] Correct expiration
- [ ] Payment confirmation on callback

#### US-PAY-006: Payment Callback Handling
**As a** system
**When** ECPay sends payment notification
**Then** the transaction should be updated correctly

**Acceptance Criteria**:
- [ ] CheckMacValue validation
- [ ] Transaction status updated
- [ ] Order status updated
- [ ] Invoice auto-generated (if enabled)

### Website Module User Stories

#### US-WEB-001: Checkout Invoice Options
**As a** website customer
**I want to** choose my invoice options during checkout
**So that** I receive my invoice in my preferred way

**Acceptance Criteria**:
- [ ] Invoice options visible on checkout
- [ ] Can select carrier type
- [ ] Can enter mobile barcode
- [ ] Can enter love code for donation
- [ ] Can enter business ID

## Requirements

### Functional Requirements

#### FR-001: Code Compilation
- All Python files must import without errors
- All XML views must load without errors
- All JavaScript files must execute without console errors

#### FR-002: Odoo 18 Compatibility
- No usage of deprecated Odoo 16 APIs
- Correct use of Odoo 18 field definitions
- Proper inheritance patterns

#### FR-003: ECPay API Integration
- Valid API calls to ECPay test environment
- Proper error handling for API failures
- CheckMacValue validation for all callbacks

#### FR-004: Invoice Functionality
- Create B2B and B2C invoices
- Void invoices
- Create allowances
- Support all carrier types
- Support donation

#### FR-005: Payment Functionality
- Support all enabled payment methods
- Handle payment callbacks correctly
- Update transaction and order status

#### FR-006: Website Functionality
- Display invoice options on checkout
- Validate user input
- Pass invoice data to backend

### Non-Functional Requirements

#### NFR-001: Performance
- Invoice creation < 5 seconds
- Payment redirect < 3 seconds
- No timeout errors during normal operation

#### NFR-002: Security
- No sensitive credentials in logs
- CheckMacValue validation on all callbacks
- Proper HTTPS enforcement

#### NFR-003: Reliability
- Graceful error handling
- Clear error messages for users
- Transaction rollback on failure

#### NFR-004: Maintainability
- Code follows Odoo conventions
- Clear documentation in Chinese/English
- Proper logging for debugging

## Success Criteria

### Code Review Success
- [ ] All Python files pass syntax check
- [ ] No deprecated API usage found
- [ ] All imports resolve correctly
- [ ] Security review passed (no credential leaks)

### Live Testing Success
- [ ] Module installation without errors
- [ ] All menu items accessible
- [ ] All views render correctly
- [ ] All buttons/actions functional

### Invoice Testing Success (100% of test cases pass)
- [ ] Create B2C invoice - manual
- [ ] Create B2C invoice - automatic
- [ ] Create B2B invoice with tax ID
- [ ] Create invoice with mobile barcode
- [ ] Create invoice with certificate barcode
- [ ] Create invoice with donation
- [ ] Create print invoice
- [ ] Void invoice
- [ ] Create allowance
- [ ] Query invoice details

### Payment Testing Success (100% of test cases pass)
- [ ] Credit card - full payment
- [ ] Credit card - installment
- [ ] WebATM (if desktop)
- [ ] ATM virtual account
- [ ] CVS code generation
- [ ] Barcode generation
- [ ] Apple Pay (if available)
- [ ] BNPL (if available)
- [ ] TWQR (if available)
- [ ] Payment callback handling
- [ ] Failed payment handling

### Website Testing Success
- [ ] Invoice options visible on checkout
- [ ] Mobile barcode validation
- [ ] Love code validation
- [ ] Business ID acceptance
- [ ] End-to-end checkout with invoice

## Constraints & Assumptions

### Constraints
- Testing uses ECPay test environment (sandbox)
- Real credit card payments cannot be tested without production credentials
- Some payment methods may require specific device types (mobile/desktop)

### Assumptions
- ECPay test credentials are configured correctly
- Live Odoo 18 instance is accessible
- Playwright MCP is available for automated UI testing
- Test transactions will be in TWD currency

## Out of Scope

- Production ECPay credential setup
- Performance load testing
- Multi-currency support testing
- Migration of historical invoice data
- Integration with other payment providers
- Tax calculation logic changes
- Custom report modifications

## Dependencies

### External Dependencies
- ECPay Test Environment API availability
- Live Odoo 18 instance (https://matt-test-254-odoo.woowtech.io/)
- Playwright MCP for UI automation

### Internal Dependencies
- Base Odoo modules: account, sale, stock, website_sale, payment
- Python package: pycryptodomex

## Test Environment Information

### Odoo Instance
- **URL**: https://matt-test-254-odoo.woowtech.io/
- **Admin**: admin / admin
- **Test User**: woow_ngrok_002@protonmail.com / admin

### ECPay Test Credentials
- Located in company settings
- Test mode must be enabled for sandbox testing

### SSH Access
- Command: `ssh ha-192-168-2-254`
- Purpose: Log inspection, database queries (read-only)

## Testing Approach

### Phase 1: Static Code Review
1. Check all Python imports
2. Verify Odoo 18 API compliance
3. Review security (no hardcoded credentials)
4. Check XML view syntax

### Phase 2: Installation Test
1. Install/upgrade modules
2. Verify no installation errors
3. Check all menu items load

### Phase 3: Functional Testing (Playwright)
1. Backend admin tests
2. Website customer tests
3. Payment flow tests
4. Callback simulation

### Phase 4: Integration Testing
1. Full purchase flow with invoice
2. Full purchase flow with payment
3. Void and allowance flows

## Deliverables

1. **MASTER_TASK.md** - Progress tracking document
2. **Code review findings** - List of issues found and fixed
3. **Test results** - Pass/fail for each test case
4. **Bug fixes** - Git commits for any issues found
5. **Final report** - Summary of all testing activities

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| ECPay API changes | High | Low | Check API documentation |
| Odoo 18 breaking changes | Medium | Medium | Follow migration guide |
| Test environment instability | Medium | Medium | Document reproduction steps |
| Payment callback issues | High | Medium | Extensive callback testing |

## Next Steps

After PRD approval:
1. Run `/pm:prd-parse ecpay-odoo18-modules-review-test` to create implementation epic
2. Begin code review phase
3. Set up Playwright test scripts
4. Execute testing phases
