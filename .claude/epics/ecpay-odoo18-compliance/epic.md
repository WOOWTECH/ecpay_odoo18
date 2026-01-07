---
name: ecpay-odoo18-compliance
status: backlog
created: 2026-01-07T00:54:13Z
updated: 2026-01-07T01:25:46Z
progress: 0%
prd: .claude/prds/ecpay-odoo18-compliance.md
github: [Will be updated when synced to GitHub]
---

# Epic: ECPay Odoo 18 Full Compliance & Production Readiness

## Overview

This epic addresses the remaining Odoo 18 compliance issues and production readiness for three ECPay modules (`ecpay_invoice_tw`, `ecpay_invoice_website`, `payment_ecpay`). The work focuses on:

1. **Critical Bug Fixes** - Resolve 11 open bugs (BUG-001, BUG-002, BUG-007 through BUG-015)
2. **Website Checkout Enhancements** - Add missing input fields for carrier numbers and lovecodes
3. **Odoo 18 Compliance Audit** - Ensure all code patterns comply with Odoo 18 standards
4. **Testing & Documentation** - Comprehensive test coverage and user guide

## Bug Summary (Post-Architecture Review)

An architect review identified **8 additional bugs** beyond the 3 originally documented:

| Bug ID | Severity | Module | Description |
|--------|----------|--------|-------------|
| BUG-001 | High | ecpay_invoice_tw | carrierNum readonly field - cannot input carrier number |
| BUG-002 | High | ecpay_invoice_tw | Donation/print fields readonly |
| BUG-007 | Critical | ecpay_invoice_tw | Settings page crash - KeyError 'group_mrp_routings' |
| BUG-008 | Medium | payment_ecpay | Missing `@api.depends` on `_compute_display_name` |
| BUG-009 | Medium | ecpay_invoice_tw | Boolean comparison using `is` instead of `==` (12 locations) |
| BUG-010 | High | ecpay_invoice_tw | `carrierNum` related field cannot be written to (same root as BUG-001) |
| BUG-011 | High | ecpay_invoice_tw | `is_donation`/`is_print` readonly blocks UI (same root as BUG-002) |
| BUG-012 | Low | payment_ecpay | SDK type comparison using `is` for types |
| BUG-013 | High | ecpay_invoice_tw | Multiple readonly fields block website data flow (`lovecode`, `ecpay_CustomerIdentifier`, etc.) |
| BUG-014 | Medium | ecpay_invoice_website | ConfirmationDialog may fail in frontend context |
| BUG-015 | Low | payment_ecpay | `any()` usage on recordset deprecated |

**Note:** BUG-010/011 are the same root cause as BUG-001/002 but identified at different code locations. BUG-013 expands the scope of readonly field issues.

## Bug Resolution Process (MANDATORY)

**CRITICAL:** Every bug fix MUST strictly follow this 6-step process to ensure 100% resolution:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        BUG RESOLUTION PROCESS                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  Step 1: DEEP RESEARCH                                                      │
│  ├── Read Odoo 18 architecture reference                                    │
│  │   Path: /mnt/c/Users/Matt/Desktop/CLAUDE專案/ODOO相關/                   │
│  │         Odoo_18_Environment_Architecture                                 │
│  ├── Trace the bug to its root cause                                        │
│  ├── Identify all affected files and code paths                             │
│  └── Document findings in bug analysis                                      │
│                                                                             │
│  Step 2: CREATE FIX PLAN                                                    │
│  ├── Write detailed fix plan with specific code changes                     │
│  ├── Identify potential side effects                                        │
│  ├── List all files to modify                                               │
│  └── Define rollback strategy                                               │
│                                                                             │
│  Step 3: REVIEW FIX PLAN                                                    │
│  ├── Validate against Odoo 18 best practices                                │
│  ├── Check for conflicts with other bugs                                    │
│  ├── Ensure minimal code changes                                            │
│  └── Get confirmation before proceeding                                     │
│                                                                             │
│  Step 4: IMPLEMENT FIX                                                      │
│  ├── Apply code changes                                                     │
│  ├── Commit with descriptive message                                        │
│  ├── Reference bug ID in commit                                             │
│  └── Push to repository                                                     │
│                                                                             │
│  Step 5: DEPLOY TEST (Playwright MCP - Headed Mode)                         │
│  ├── Deploy to test Odoo instance                                           │
│  ├── Run automated UI tests with Playwright                                 │
│  ├── Verify bug is fixed                                                    │
│  ├── Check for regressions                                                  │
│  └── Document test results                                                  │
│                                                                             │
│  Step 6: ROLLBACK IF FAILED                                                 │
│  ├── If deploy test fails → immediate rollback                              │
│  ├── Revert commit(s)                                                       │
│  ├── Document failure reason                                                │
│  └── Return to Step 1 with new insights                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Process Details

#### Step 1: Deep Research
```bash
# Reference architecture documentation
ODOO_ARCH_REF="/mnt/c/Users/Matt/Desktop/CLAUDE專案/ODOO相關/Odoo_18_Environment_Architecture"

# Required research for each bug:
# 1. Read relevant architecture docs
# 2. Grep for related patterns in codebase
# 3. Check Odoo 18 source if needed
# 4. Document root cause analysis
```

#### Step 2: Create Fix Plan
Each fix plan must include:
- **Root Cause**: Exact reason for the bug
- **Solution**: Specific code changes
- **Files Modified**: List of all files
- **Side Effects**: Potential impacts
- **Rollback Plan**: How to revert if needed

#### Step 3: Review Fix Plan
Checklist before implementation:
- [ ] Follows Odoo 18 patterns from architecture reference
- [ ] No conflicts with other bug fixes
- [ ] Minimal invasive changes
- [ ] Backward compatible (if applicable)

#### Step 4: Implement Fix
```bash
# Commit format
git commit -m "Fix BUG-XXX: [Brief description]

- Root cause: [explanation]
- Solution: [what was changed]
- Files: [list of modified files]

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```

#### Step 5: Deploy Test with Playwright MCP
```javascript
// Use Playwright MCP in HEADED mode for visual verification
// Test Instance: https://matt-test-254-odoo.woowtech.io/
// Login: admin / admin

// Required test scenarios per bug:
// 1. Direct bug reproduction test
// 2. Related functionality regression test
// 3. Screenshot capture for documentation
```

#### Step 6: Rollback Protocol
```bash
# If test fails:
git revert HEAD  # Revert last commit
git push origin main

# Document failure:
# - What test failed
# - Why the fix didn't work
# - New insights for next attempt
```

### Odoo 18 Architecture Reference

**Location:** `/mnt/c/Users/Matt/Desktop/CLAUDE專案/ODOO相關/Odoo_18_Environment_Architecture`

Use this reference for:
- Correct field definitions and decorators
- View inheritance patterns
- JavaScript module syntax
- Controller patterns
- Security model patterns

## Architecture Decisions

### AD-1: Carrier Number Input Strategy
- **Decision**: Add new editable field `input_carrier_num` on `account.move` rather than modifying the existing readonly related field
- **Rationale**: Preserves the readonly `carrierNum` field that shows the ECPay-assigned value, while allowing user input before invoice issuance
- **Pattern**: Use `@api.onchange` for validation, copy to API params on `create_ecpay_invoice()`

### AD-2: Settings Page Fix Approach
- **Decision**: Investigate the inheritance chain to find MRP field reference, then either remove it or add proper conditional handling
- **Rationale**: The error is caused by referencing a field from an uninstalled module; proper Odoo 18 pattern is to check field existence or use conditional views
- **Pattern**: Use `hasattr()` or try/except in Python, `invisible` conditions in XML

### AD-3: Website Checkout UI Enhancement
- **Decision**: Extend existing JavaScript widget (`ECPayInvoiceHandler`) with new input fields rather than creating new components
- **Rationale**: Leverages existing validation logic and RPC patterns already implemented
- **Pattern**: Add conditional input fields in QWeb template, extend JS handlers

### AD-4: Test Strategy
- **Decision**: Focus on unit tests for model methods + manual integration testing on live Odoo instance
- **Rationale**: ECPay API testing requires sandbox environment; UI tests are fragile; manual protocol ensures real-world validation
- **Pattern**: Use Odoo's `TransactionCase` for unit tests, documented manual test protocol

## Technical Approach

### Backend Changes (ecpay_invoice_tw)

**Models to Modify:**
| File | Changes |
|------|---------|
| `models/account_invoice.py` | Add `input_carrier_num`, `input_lovecode` fields; add onchange handlers; remove readonly from `is_donation`, `is_print`, `lovecode`, `ecpay_CustomerIdentifier`, `ec_print_address`, `ec_ident_name`; fix `is` vs `==` comparisons (BUG-009) |
| `models/res_config_settings.py` | Fix MRP field reference causing KeyError |
| `views/account_invoice_form.xml` | Update form to show new input fields conditionally |
| `views/res_config_setting_view.xml` | Ensure view doesn't reference missing fields |

**Key Implementation Details:**
```python
# New fields on account.move
input_carrier_num = fields.Char(string='Carrier Number Input')
input_lovecode = fields.Char(string='Donation Code Input')

# Onchange validation
@api.onchange('carrierType', 'input_carrier_num')
def _onchange_carrier_num(self):
    if self.carrierType in ['2', '3'] and self.input_carrier_num:
        # Validate format based on carrier type
        pass
```

### Frontend Changes (ecpay_invoice_website)

**Files to Modify:**
| File | Changes |
|------|---------|
| `static/src/js/invoice.js` | Add input field handlers for carrier num and lovecode |
| `views/website_sale.xml` | Add conditional input fields in QWeb template |
| `controllers/main.py` | Handle new input parameters in `save_invoice_type` route |

**Key Implementation Details:**
```javascript
// Add input field visibility logic
_updateCarrierInput() {
    const carrierType = this.$('select[name="eCarrierType"]').val();
    const showInput = ['2', '3'].includes(carrierType);
    this.$('.carrier_num_input').toggleClass('d-none', !showInput);
}
```

### Compliance Audit Scope

**Python Files (18 files across 3 modules):**
- Check for deprecated decorators, methods, field attributes
- Verify `_description` on all models
- Fix string comparisons using `is` (BUG-009, BUG-012)
- Add missing `@api.depends` decorators (BUG-008)
- Fix deprecated `any()` on recordsets (BUG-015)

**JavaScript Files (3 files):**
- Verify `/** @odoo-module **/` headers
- Check import paths
- Verify `_super` binding patterns
- Fix ConfirmationDialog usage in frontend (BUG-014)

**XML Files (15 files):**
- Verify view inheritance patterns
- Check for deprecated attributes

## Implementation Strategy

### Phase 1: Critical Bug Fixes (Priority: Immediate)
1. Fix BUG-007 (Settings page crash) - **Blocking issue**
2. Fix BUG-001 (Carrier number input)
3. Fix BUG-002 (Donation/print fields)

### Phase 2: Website Enhancements
4. Add carrier number input to checkout
5. Add lovecode input to checkout

### Phase 3: Quality Assurance
6. Odoo 18 compliance audit
7. Unit tests for new functionality
8. Manual integration testing

### Phase 4: Documentation
9. Update user guide
10. Update README

### Risk Mitigation
- **Settings page crash**: Investigate before other changes to avoid blocking development
- **ECPay API changes**: Use sandbox for all development; document any API quirks
- **Browser compatibility**: Test checkout flow in Chrome, Firefox, Safari

## Task Breakdown

Each task follows the **6-Step Bug Resolution Process** defined above.

| # | Task | Priority | Scope | Bugs Addressed | Process Steps |
|---|------|----------|-------|----------------|---------------|
| 1 | Fix BUG-007: Settings Page KeyError | Critical | ecpay_invoice_tw | BUG-007 | Research → Plan → Review → Implement → Test → Verify |
| 2 | Fix Readonly Fields (Invoice Form) | High | ecpay_invoice_tw | BUG-001, BUG-002, BUG-010, BUG-011, BUG-013 | Research → Plan → Review → Implement → Test → Verify |
| 3 | Add Checkout Input Fields (Carrier + Lovecode) | High | ecpay_invoice_website | BUG-014 (partial) | Research → Plan → Review → Implement → Test → Verify |
| 4 | Python Code Compliance Fixes | Medium | All modules | BUG-008, BUG-009, BUG-012, BUG-015 | Research → Plan → Review → Implement → Test → Verify |
| 5 | JavaScript Compliance Fixes | Medium | ecpay_invoice_website | BUG-014 | Research → Plan → Review → Implement → Test → Verify |
| 6 | Unit Tests for New Functionality | High | ecpay_invoice_tw | - | Implement → Test |
| 7 | Full Integration Testing (Playwright) | High | All modules | All bugs verification | Deploy Test → Document |
| 8 | Update User Guide Documentation | Medium | Documentation | - | Document |

### Task Execution Template

For each bug fix task (Tasks 1-5), execute:

```markdown
## Task X: [Bug Description]

### Step 1: Deep Research
- [ ] Read Odoo 18 architecture reference
- [ ] Trace root cause
- [ ] Document affected files
- [ ] Findings: [document here]

### Step 2: Fix Plan
- **Root Cause:** [explanation]
- **Solution:** [specific changes]
- **Files to Modify:** [list]
- **Side Effects:** [potential impacts]
- **Rollback:** `git revert [commit]`

### Step 3: Review
- [ ] Follows Odoo 18 patterns
- [ ] No conflicts with other fixes
- [ ] Minimal changes
- [ ] Ready to implement

### Step 4: Implementation
- [ ] Code changes applied
- [ ] Committed with message
- [ ] Pushed to repository

### Step 5: Deploy Test (Playwright MCP - Headed)
- [ ] Navigate to https://matt-test-254-odoo.woowtech.io/
- [ ] Login with admin / admin
- [ ] Reproduce original bug scenario
- [ ] Verify bug is fixed
- [ ] Check for regressions
- [ ] Screenshots captured

### Step 6: Result
- [ ] ✅ PASS - Bug resolved, move to next task
- [ ] ❌ FAIL - Rollback and retry from Step 1
```

**Total Estimated Effort: 24-36 hours**

### Bug-to-Task Mapping

| Bug | Task | Notes |
|-----|------|-------|
| BUG-001 | Task 2 | Add input field for carrier number |
| BUG-002 | Task 2 | Remove readonly from donation/print fields |
| BUG-007 | Task 1 | Fix Settings page crash |
| BUG-008 | Task 4 | Add @api.depends to _compute_display_name |
| BUG-009 | Task 4 | Fix `is` vs `==` comparisons in account_invoice.py |
| BUG-010 | Task 2 | Same root cause as BUG-001 |
| BUG-011 | Task 2 | Same root cause as BUG-002 |
| BUG-012 | Task 4 | Fix `is` comparisons in SDK |
| BUG-013 | Task 2 | Remove readonly from lovecode, CustomerIdentifier, etc. |
| BUG-014 | Task 5 | Fix ConfirmationDialog in frontend |
| BUG-015 | Task 4 | Replace any() with bool() on recordset |

## Dependencies

### Prerequisites
- Access to live Odoo 18 test instance
  - **URL:** https://matt-test-254-odoo.woowtech.io/
  - **Username:** admin
  - **Password:** admin
- ECPay sandbox credentials (already configured)
- Browser for testing (Chrome recommended)

### Blocking Dependencies
| Dependency | Blocks | Owner |
|------------|--------|-------|
| BUG-007 fix | All Settings-related testing | Task 1 |
| BUG-001/002 fixes | Invoice form testing | Task 2 |
| Checkout fixes | Website flow testing | Task 3 |

### External Dependencies
- ECPay sandbox API availability
- Odoo 18 stable (no breaking changes expected)

## Success Criteria (Technical)

### Bug Fix Verification
- [ ] Settings page loads without error (BUG-007)
- [ ] Carrier number can be entered on invoice form (BUG-001, BUG-010)
- [ ] Donation/print options can be toggled on invoice form (BUG-002, BUG-011)
- [ ] Lovecode, CustomerIdentifier, address fields editable (BUG-013)
- [ ] Carrier number input appears in checkout for carrier types 2 and 3
- [ ] Lovecode input appears in checkout for donation option
- [ ] Error dialogs work in website frontend (BUG-014)

### Compliance Verification
- [ ] `rg "@api.multi|@api.one" --type py` returns 0 results
- [ ] `rg "name_get" --type py` returns 0 results (except comments)
- [ ] `rg "odoo.define" --type js` returns 0 results
- [ ] All 3 manifests have `license` field
- [ ] No `is True` or `is False` comparisons (BUG-009)
- [ ] All `_compute_display_name` have `@api.depends` (BUG-008)
- [ ] No `any()` on recordsets (BUG-015)

### Test Coverage
- [ ] Unit tests pass: `odoo-bin -i ecpay_invoice_tw --test-enable`
- [ ] Manual test protocol: 100% pass rate
- [ ] Invoice issuance with mobile barcode carrier: Success
- [ ] Invoice issuance with donation: Success

### Documentation
- [ ] User guide covers all e-invoice options
- [ ] README reflects current functionality
- [ ] Troubleshooting section includes BUG-007 symptoms

## Estimated Effort

| Phase | Tasks | Hours |
|-------|-------|-------|
| Critical Bug Fixes | 1-2 | 6-10 |
| Website Enhancements | 3 | 4-6 |
| Compliance | 4-5 | 5-8 |
| Testing | 6-7 | 7-10 |
| Documentation | 8 | 2-3 |
| **Total** | **8 tasks** | **24-37 hours** |

**Timeline**: Can be completed in 4-5 focused work days.

## Notes

### Simplifications Applied
1. Combined BUG-001 and BUG-002 fixes into single task (both modify same files)
2. Combined carrier input and lovecode input into single checkout enhancement task
3. Combined compliance audit and fix application (audit informs fixes immediately)
4. Deferred technical documentation (README update covers essentials)

### Leveraging Existing Work
- Previous migration (BUG-003 through BUG-006) established patterns for:
  - JavaScript ES6 module syntax
  - Odoo 18 RPC patterns
  - Boolean field handling
  - Proper `super()` binding
- Use these patterns as reference for new code
