---
name: ecpay-odoo18-modules-review-test
status: backlog
created: 2025-12-30T10:50:39Z
updated: 2025-12-30T11:14:29Z
progress: 0%
prd: .claude/prds/ecpay-odoo18-modules-review-test.md
github: [Will be updated when synced to GitHub]
---

# Epic: ECPay Odoo 18 Modules Code Review & Live Testing

## Overview

Technical implementation for validating three ECPay modules (ecpay_invoice_tw, ecpay_invoice_website, payment_ecpay) on Odoo 18. This involves static code analysis, Odoo 18 compatibility verification, and comprehensive live testing using Playwright MCP against a production instance.

## Architecture Decisions

### Testing Strategy
- **Playwright MCP** for UI automation - leverages existing MCP integration for browser control
- **Screenshot capture** - take screenshots during all Playwright tests for documentation and final report
- **Sequential testing** - test invoice module first (dependency for website module), then payment, then website
- **Live instance testing** - no local environment setup needed, tests run against https://matt-test-254-odoo.woowtech.io/

### Code Review Approach
- **Static analysis** using Python AST and grep patterns to detect deprecated Odoo 16 APIs
- **Focus areas**: `states=` attribute removal, `name_get()` deprecation, field definition changes
- **No extensive refactoring** - only fix blocking issues, document non-critical findings

### Test Data Strategy
- **Create fresh test data** for each test run (new sales orders, invoices)
- **Use ECPay sandbox** environment (test mode enabled in company settings)
- **No cleanup required** - test environment is disposable

## Technical Approach

### Phase 1: Static Code Review
- Python syntax validation (compileall)
- Odoo 18 API compliance check (deprecated patterns)
- XML view validation
- Security audit (credential exposure)

### Phase 2: Module Installation Verification
- Upgrade/reinstall modules via Odoo UI
- Verify menu items and views load correctly
- Check for server errors in logs

### Phase 3: Invoice Module Testing (ecpay_invoice_tw)
- Configure company ECPay settings (test mode)
- Create sales order → invoice → post
- Test manual and automatic e-invoice creation
- Test carrier types (mobile barcode, certificate)
- Test donation flow
- Test B2B invoice with tax ID
- Test void and allowance operations

### Phase 4: Payment Module Testing (payment_ecpay)
- Configure payment provider settings
- Test credit card payment flow (redirect to ECPay)
- Test ATM/CVS/Barcode code generation
- Verify callback handling (pending → done states)

### Phase 5: Website Module Testing (ecpay_invoice_website)
- Test checkout page invoice options
- Test input validation (mobile barcode, love code)
- End-to-end purchase with invoice options

## Implementation Strategy

### Git Workflow
- **Commit on file changes** - commit immediately when any file is modified (including `.claude/` directory)
- **Branch management** - work on feature branch `epic/ecpay-odoo18-modules-review-test`
- **Commit message format**: `Issue #{task_number}: {description}`
- **Include all changes** - `.claude/` files (PRD, epic, tasks) are part of the project and should be committed

### Risk Mitigation
- Start with code review to catch compile errors before live testing
- Test invoice module before payment (invoice is a dependency)
- Document any skipped tests with clear reasons

### Testing Priorities
1. **Critical**: Invoice creation, payment processing
2. **High**: Void/allowance, callback handling
3. **Medium**: All carrier types, all payment methods
4. **Low**: Edge cases, error scenarios

## Task Breakdown Preview

- [ ] Task 1: Static Code Review & Odoo 18 Compatibility Audit
- [ ] Task 2: Module Installation & Configuration Verification
- [ ] Task 3: Invoice Module - Basic Invoice Creation Tests
- [ ] Task 4: Invoice Module - Carrier Types & Donation Tests
- [ ] Task 5: Invoice Module - Void & Allowance Tests
- [ ] Task 6: Payment Module - Payment Flow Tests
- [ ] Task 7: Payment Module - Callback & Status Tests
- [ ] Task 8: Website Module - Checkout Invoice Options Tests
- [ ] Task 9: Integration Test - Full Purchase Flow
- [ ] Task 10: Final Report & Documentation

## Dependencies

### External
- ECPay Test API availability
- Live Odoo 18 instance uptime
- Playwright MCP operational

### Internal
- Company ECPay credentials configured
- Test products with correct pricing
- Payment provider enabled

## Success Criteria (Technical)

### Code Review
- Zero Python syntax errors
- Zero blocking Odoo 18 compatibility issues
- No hardcoded credentials found

### Invoice Testing
- ≥90% of invoice test cases pass
- All critical flows (create, void, allowance) working
- ECPay API calls successful

### Payment Testing
- ≥90% of payment test cases pass
- Callback handling verified
- Transaction states updated correctly

### Website Testing
- Invoice options visible and functional
- Validation working for all input types

## Estimated Effort

| Task Category | Estimated Time |
|--------------|----------------|
| Code Review | 1-2 hours |
| Installation Test | 30 min |
| Invoice Tests | 2-3 hours |
| Payment Tests | 2-3 hours |
| Website Tests | 1-2 hours |
| Documentation | 1 hour |
| **Total** | **8-12 hours** |

## Test Environment

- **URL**: https://matt-test-254-odoo.woowtech.io/
- **Admin**: admin / admin
- **Test User**: woow_ngrok_002@protonmail.com / admin
- **SSH**: `ssh ha-192-168-2-254` (read-only log access)

## Tasks Created

- [ ] 001.md - Static Code Review & Odoo 18 Compatibility Audit (parallel: true)
- [ ] 002.md - Module Installation & Configuration Verification (parallel: false, depends: 001)
- [ ] 003.md - Invoice Module - Basic Invoice Creation Tests (parallel: true, depends: 002)
- [ ] 004.md - Invoice Module - Carrier Types & Donation Tests (parallel: false, depends: 003)
- [ ] 005.md - Invoice Module - Void & Allowance Tests (parallel: false, depends: 003)
- [ ] 006.md - Payment Module - Payment Flow Tests (parallel: true, depends: 002)
- [ ] 007.md - Payment Module - Callback & Status Tests (parallel: false, depends: 006)
- [ ] 008.md - Website Module - Checkout Invoice Options Tests (parallel: false, depends: 003, 004)
- [ ] 009.md - Integration Test - Full Purchase Flow (parallel: false, depends: 003-008)
- [ ] 010.md - Final Report & Documentation (parallel: false, depends: all)

**Total tasks:** 10
**Parallel tasks:** 3 (001, 003, 006)
**Sequential tasks:** 7
**Estimated total effort:** 19 hours

## Deliverables

1. MASTER_TASK.md with task summaries
2. Git commits for any bug fixes
3. Test results documented per task
4. Screenshots captured during Playwright testing (stored in `screenshots/` directory)
5. Final summary report with embedded screenshots
