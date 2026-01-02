# BUG-006 Fix Plan: JavaScript Migration to Odoo 18

## Bug Summary

| Field | Value |
|-------|-------|
| Bug ID | BUG-006 |
| Severity | Critical |
| Module | `ecpay_invoice_website` |
| File | `static/src/js/invoice.js` |
| Symptom | E-invoice options selected during checkout are NOT saved to sale order |
| Root Cause | JavaScript uses Odoo 16 module syntax, causing entire file to fail loading in Odoo 18 |

## Root Cause Analysis

### Console Errors Observed
```
[ERROR] The following modules are needed by other modules but have not been defined...
[ERROR] The following modules could not be loaded because they have unmet dependencies...
```

### Technical Analysis

The JavaScript file uses deprecated Odoo 16 module loading syntax that is incompatible with Odoo 18:

| Component | Odoo 16 (Current) | Odoo 18 (Required) |
|-----------|-------------------|---------------------|
| Module declaration | `odoo.define('name', function(require){...})` | `/** @odoo-module **/` |
| RPC import | `require('web.rpc')` | `import { rpc } from '@web/core/network/rpc'` |
| Public widget | `require('web.public.widget')` | `import publicWidget from '@web/legacy/js/public/public_widget'` |
| Payment form | `require('payment.checkout_form')` | `import PaymentForm from '@payment/js/payment_form'` |
| RPC calls | `rpc.query({route, params})` | `await rpc(route, params)` |
| Extension pattern | `PaymentCheckoutForm.include({...})` | `PaymentForm.include({...})` |

### Reference Implementation

Official Odoo 18 ECPay module found at:
```
odoo/addons/l10n_tw_edi_ecpay_website_sale/static/src/js/website_sale.js
```

## Changes Required

### 1. Module Header Replacement

**Current (Odoo 16):**
```javascript
odoo.define('ecpay_invoice_tw.checkout', function (require) {
    "use strict";

    const rpc = require('web.rpc');
    const publicWidget = require('web.public.widget');
    const PaymentCheckoutForm = require('payment.checkout_form');
```

**New (Odoo 18):**
```javascript
/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';
import PaymentForm from '@payment/js/payment_form';
import { rpc } from '@web/core/network/rpc';
```

### 2. Widget Registration Update

**Current:**
```javascript
let ECPayInvoiceHandler = publicWidget.Widget.extend({...});
publicWidget.registry.ECPayInvoiceHandler = ECPayInvoiceHandler;
```

**New:**
```javascript
publicWidget.registry.ECPayInvoiceHandler = publicWidget.Widget.extend({...});
```

### 3. RPC Model Calls (check_carrier_num, check_lovecode)

**Current:**
```javascript
rpc.query({
    model: 'account.move',
    method: 'check_carrier_num',
    args: [value],
}).then(result => {
    // handle result
});
```

**New:**
```javascript
try {
    const result = await rpc('/web/dataset/call_kw/account.move/check_carrier_num', {
        model: 'account.move',
        method: 'check_carrier_num',
        args: [value],
        kwargs: {},
    });
    // handle result
} catch (error) {
    console.error('RPC error:', error);
}
```

### 4. RPC Route Calls (save_invoice_type)

**Current:**
```javascript
prom = rpc.query({
    route,
    params: {
        invoiceType,
        invoice_type: sharedDataset.eType,
        CarrierNum: sharedDataset.carrierNum,
    }
});
```

**New:**
```javascript
const result = await rpc(route, {
    invoiceType,
    invoice_type: sharedDataset.eType,
    CarrierNum: sharedDataset.carrierNum,
});
```

### 5. PaymentForm Extension

**Current:**
```javascript
PaymentCheckoutForm.include({
    _onClickPay: function (ev) {
        const self = this;
        const originSuper = this._super;
        ev.stopPropagation();
        ev.preventDefault();
        let target = ev.currentTarget;

        let prom = this._ensureEcpayInvoiceAlright();
        if (prom) {
            target.disabled = true;
            prom.then(result => {
                target.disabled = false;
                if (!result) {
                    self._displayError('更新電子發票資訊失敗', '更新電子發票資訊失敗，請稍後重試');
                } else {
                    originSuper.apply(self, arguments);
                }
            });
        }
    },
    // ...
});
```

**New:**
```javascript
PaymentForm.include({
    async _submitForm(ev) {
        // Validate ECPay invoice data before submitting
        const isValid = await this._ensureEcpayInvoiceAlright();
        if (!isValid) {
            return; // Don't proceed with payment
        }
        return this._super(...arguments);
    },

    async _ensureEcpayInvoiceAlright() {
        // Check if ECPay invoice form exists on page
        if (!document.querySelector('.ecpay-invoice-info-form')) {
            return true; // No ECPay form, proceed normally
        }

        const route = '/payment/ecpay/save_invoice_type';
        const { invoiceType, eType, carrierNum, address, vatNeeded, name, identifier, loveCode } = sharedDataset;

        try {
            let params = {};

            if (invoiceType === 0) {
                // Electronic invoice with carrier
                if (eType > 1 && !carrierNum) {
                    this._displayErrorDialog('載具號碼錯誤', '請輸入正確的載具號碼');
                    return false;
                }
                params = {
                    invoice_type: eType,
                    CarrierNum: carrierNum,
                };
            } else if (invoiceType === 1) {
                // Paper invoice
                if (!address) {
                    this._displayErrorDialog('電子發票有必填欄位尚未填寫', '請填寫發票寄送地址！');
                    return false;
                }
                params = {
                    print_flag: true,
                    invoice_address: address,
                };
                if (vatNeeded) {
                    if (!name || !identifier) {
                        this._displayErrorDialog('電子發票有必填欄位尚未填寫', '請確認「受買人姓名」，「統一編號」是否有填寫');
                        return false;
                    }
                    params.ident_flag = true;
                    params.identifier_name = name;
                    params.identifier = identifier;
                }
            } else if (invoiceType === 2) {
                // Donation
                if (!loveCode) {
                    this._displayErrorDialog('電子發票有必填欄位尚未填寫', '請確認「捐贈碼」是否有填寫正確');
                    return false;
                }
                params = {
                    donate_flag: true,
                    LoveCode: loveCode,
                };
            } else {
                this._displayErrorDialog('錯誤的類型', '不支援的電子發票類型');
                return false;
            }

            const result = await rpc(route, params);
            return result === '200';
        } catch (error) {
            console.error('ECPay invoice save error:', error);
            this._displayErrorDialog('更新電子發票資訊失敗', '更新電子發票資訊失敗，請稍後重試');
            return false;
        }
    },

    _displayErrorDialog(title, message) {
        // Use Odoo 18 dialog system or fallback to alert
        if (this.call && this.call.bind) {
            this.call('dialog', 'add', {
                title: title,
                body: message,
            });
        } else {
            alert(`${title}\n${message}`);
        }
    },
});
```

### 6. Remove Module Wrapper

**Current (end of file):**
```javascript
    return {
        sharedDataset,
        ECPayInvoiceHandler,
    };
});
```

**New:**
```javascript
// No wrapper needed - ES6 modules don't need return
// Export if needed for external access:
// export { sharedDataset, ECPayInvoiceHandler };
```

## Implementation Steps

1. **Backup current file**
   ```bash
   cp invoice.js invoice.js.bak
   ```

2. **Create new Odoo 18 compatible invoice.js**
   - Apply all changes listed above
   - Convert event handlers to async/await where RPC is used

3. **Update manifest if needed**
   - Verify `web.assets_frontend` bundle is correct (already done)

4. **Deploy to server**
   ```bash
   ssh ha-192-168-2-254
   docker exec -i addon_local_odoo tee /addon_config/odoo_custom_addons/ecpay_invoice_website/static/src/js/invoice.js < invoice.js
   docker restart addon_local_odoo
   ```

5. **Clear browser cache**
   - Hard refresh (Ctrl+Shift+R)
   - Or clear cache from browser settings

6. **Test the fix**
   - Go to shop, add product, checkout
   - Select "綠界科技電子發票載具" carrier type
   - Click "Pay now"
   - Verify order in Odoo has carrier type saved

## Verification Checklist

- [ ] No console errors about undefined modules
- [ ] ECPay invoice form displays correctly
- [ ] Carrier type dropdown works
- [ ] Carrier number validation works (for types 2 and 3)
- [ ] Love code validation works
- [ ] "Pay now" button saves invoice options to order
- [ ] Order shows correct carrier type in "綠界電商資料" tab

## Rollback Plan

If the fix fails:
```bash
ssh ha-192-168-2-254
docker exec -i addon_local_odoo tee /addon_config/odoo_custom_addons/ecpay_invoice_website/static/src/js/invoice.js < invoice.js.bak
docker restart addon_local_odoo
```

## Related Issues

- BUG-005: Parameter mismatch (fixed in code but couldn't take effect due to BUG-006)
  - Changed `e_type` to `invoice_type` in JS
  - Added `donate_flag: true` for donation case
  - These fixes are included in this migration

## Review Findings

### Review Date: 2026-01-02

### Items Verified

1. **PaymentForm method name**: Confirmed `_submitForm` is the correct method to override (not `_onClickPay`)
   - Source: `odoo/addons/payment/static/src/js/payment_form.js:124`

2. **RPC pattern for routes**: Confirmed `await rpc(route, params)` format
   - Source: `odoo/addons/payment/static/src/js/payment_form.js:376`

3. **RPC pattern for model methods**: Confirmed `/web/dataset/call_kw/model.name/method_name` format
   - Required for `check_carrier_num` and `check_lovecode` calls

4. **Error dialog method**: Confirmed `_displayErrorDialog(title, message)` uses `ConfirmationDialog`
   - Source: `odoo/addons/payment/static/src/js/payment_form.js:289`
   - Requires import: `import { ConfirmationDialog } from '@web/core/confirmation_dialog/confirmation_dialog'`

5. **Import paths verified**:
   - `import { rpc } from '@web/core/network/rpc'` ✓
   - `import publicWidget from '@web/legacy/js/public/public_widget'` ✓
   - `import PaymentForm from '@payment/js/payment_form'` ✓

### Corrections to Plan

1. **Add ConfirmationDialog import** (was missing):
   ```javascript
   import { ConfirmationDialog } from '@web/core/confirmation_dialog/confirmation_dialog';
   ```

2. **Update _displayErrorDialog implementation** to use proper Odoo 18 dialog:
   ```javascript
   _displayErrorDialog(title, message) {
       this.call('dialog', 'add', ConfirmationDialog, { title: title, body: message || "" });
   },
   ```

3. **Event handler methods with RPC calls** need to be converted to async:
   - `_changeCarrierNum` → `async _changeCarrierNum`
   - `_changeLoveCode` → `async _changeLoveCode`

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Module still fails to load | Low | High | Verify all imports and syntax before deploy |
| PaymentForm extension breaks payment flow | Medium | High | Test with multiple payment scenarios |
| RPC calls fail | Low | Medium | Add proper error handling with try/catch |
| Browser cache shows old JS | Medium | Low | Clear cache, use private browsing for test |

### Approval

- [x] Plan reviewed and approved for implementation
- [x] All code patterns verified against Odoo 18 source
- [x] Rollback plan in place

## References

- Official Odoo 18 ECPay module: `odoo/addons/l10n_tw_edi_ecpay_website_sale/`
- Odoo 18 PaymentForm: `odoo/addons/payment/static/src/js/payment_form.js`
- Odoo 18 website_sale PaymentForm extension: `odoo/addons/website_sale/static/src/js/payment_form.js`
