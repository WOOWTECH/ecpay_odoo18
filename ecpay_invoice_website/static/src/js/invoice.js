/** @odoo-module **/
// ECPay Invoice Website - Odoo 18 Compatible
// Migrated from Odoo 16 module syntax to ES6 modules

import publicWidget from '@web/legacy/js/public/public_widget';
import PaymentForm from '@payment/js/payment_form';
import { rpc } from '@web/core/network/rpc';
import { ConfirmationDialog } from '@web/core/confirmation_dialog/confirmation_dialog';

// Shared state for invoice form data
const sharedDataset = {
    invoiceType: 0,

    eType: 0,
    carrierNum: '',
    name: '',
    identifier: '',

    address: '',
    vatNeeded: false,

    loveCode: '',
};

// ECPay Invoice Handler Widget
publicWidget.registry.ECPayInvoiceHandler = publicWidget.Widget.extend({
    selector: '.ecpay-invoice-info-form',
    events: {
        'click #ecpay_invoice_print .form-check': '_changeType',

        // Electronic invoice
        'change #invoice_e_type': '_changeEType',
        'change #CarrierNum': '_changeCarrierNum',

        // Paper invoice
        'change #invoice_address': '_changeAddress',
        'change input[name="identifier_group"]': '_changePaperIdenti',
        'change #identifier_name': '_changeBuyerName',
        'change #identifier': '_changeBuyerIdentifier',

        // Donation
        'change #LoveCode': '_changeLoveCode',
    },

    init: function () {
        let def = this._super(...arguments);
        this.state = sharedDataset;

        this.default_msg = {
            carrierNum: '載具格式為1碼斜線「/」加上7碼由數字及大寫英文字母及+-.符號組成的字串',
            natureNum: '總長度為16碼字元,前兩碼為大寫英文【A-Z】,後14碼為數字【0-9】',
            wait: '判斷中，請稍候...',
        };
        return def;
    },

    start: function () {
        this.$page = this.$el.find('.invoice-page');
        this.changeTypePage();

        this.state.address = this.$el.find('#invoice_address').val();

        return this._super(...arguments);
    },

    // --------------------
    //  Handler
    // --------------------
    changeTypePage: function () {
        this.$page.hide()
            .eq(this.state.invoiceType).show();
    },

    updateBuyerAlert: function () {
        let $alert = this.$el.find('#warning-identifier');

        let msg = [];
        if (!this.state.name) {
            msg.push('- 請輸入受買人名稱(不可有特殊符號)');
        }

        if (!this.state.identifier) {
            msg.push('- 請輸入正確的統編');
        }

        $alert.html(msg.join('<br/>'))[msg.length ? 'removeClass' : 'addClass']('d-none');
    },

    // --------------------
    //  Events
    // --------------------
    _changeType: function (ev) {
        let input = ev.currentTarget.querySelector('input');
        if (!input) {
            return false;
        }

        if (input.checked === false) {
            input.checked = true;
        }

        this.state.invoiceType = parseInt(input.value) || 0;
        this.changeTypePage();
    },

    _changeEType: function (ev) {
        this.state.eType = parseInt(ev.currentTarget.value) || 0;

        if (this.state.eType < 0 || this.state.eType > 3) {
            this.state.eType = 0;
        }

        this.$el.find('#ecpay_invoice_CarrierNum')
            .toggleClass('d-none', this.state.eType < 2);

        let $msg = this.$el.find('#warning-CarrierNum');
        console.log('ECPay: carrier type changed to', this.state.eType);
        if (this.state.eType === 2) {
            $msg.text(this.default_msg.natureNum);
        } else if (this.state.eType === 3) {
            $msg.text(this.default_msg.carrierNum);
        }
    },

    async _changeCarrierNum(ev) {
        let target = ev.currentTarget;
        let $msg = this.$el.find('#warning-CarrierNum');
        let value = target.value || '';
        let msg = this.default_msg.carrierNum;
        let pass = true;

        if (this.state.eType > 1) {
            if (this.state.eType === 2) {
                // Natural person certificate
                if (!/^[A-Za-z]{2}[0-9]{14}$/.test(value)) {
                    msg = `自然人憑證格式不正確！${this.default_msg.natureNum}`;
                    pass = false;
                } else {
                    msg = this.default_msg.natureNum;
                }
            } else {
                // Mobile carrier barcode
                if (/^\/[0-9a-zA-Z+-.]{7}$/.test(value)) {
                    target.disabled = true;
                    msg = this.default_msg.wait;
                    $msg.text(msg);

                    try {
                        const result = await rpc('/web/dataset/call_kw/account.move/check_carrier_num', {
                            model: 'account.move',
                            method: 'check_carrier_num',
                            args: [value],
                            kwargs: {},
                        });

                        target.disabled = false;
                        if (!result) {
                            $msg.text(`載具內容不存在！${this.default_msg.carrierNum}`);
                        }
                        this.state.carrierNum = result ? value : '';
                        return;
                    } catch (error) {
                        console.error('ECPay: carrier check RPC error:', error);
                        target.disabled = false;
                        $msg.text(`驗證失敗，請稍後重試`);
                        this.state.carrierNum = '';
                        return;
                    }
                } else {
                    msg = `格式錯誤！${this.default_msg.carrierNum}`;
                    pass = false;
                }
            }
        }

        $msg.text(msg);
        this.state.carrierNum = pass ? value : '';
    },

    _changeAddress: function (ev) {
        let value = ev.currentTarget.value || '';
        let $alert = this.$el.find('#div-invoice_address .alert');
        if (value.length < 5 || value.length > 300) {
            $alert.removeClass('d-none');
            this.state.address = '';
            return false;
        }

        $alert.addClass('d-none');
        this.state.address = value;
    },

    _changePaperIdenti: function (ev) {
        this.state.vatNeeded = ev.currentTarget.value === '1';

        this.$el.find('#ecpay_invoice_identifier_name')
            .toggleClass('d-none', !this.state.vatNeeded);
    },

    _changeBuyerName: function (ev) {
        let value = ev.currentTarget.value || '';
        let reTest = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(value);
        this.state.name = (value.length && !reTest) ? value : '';
        this.updateBuyerAlert();
    },

    _changeBuyerIdentifier: function (ev) {
        let value = ev.currentTarget.value || '';
        let reTest = /^[0-9]{8}$/.test(value);
        this.state.identifier = reTest ? value : '';
        this.updateBuyerAlert();
    },

    async _changeLoveCode(ev) {
        let $alert = this.$el.find('#warning-LoveCode');
        let target = ev.currentTarget;
        let value = target.value;

        if (!/^([xX][0-9]{2,6}|[0-9]{3,7})$/.test(value)) {
            $alert.text('愛心碼格式應為3~7碼的數字').removeClass('d-none');
            sharedDataset.loveCode = '';
            return true;
        }

        target.disabled = true;
        $alert.text(this.default_msg.wait).removeClass('d-none alert-danger').addClass('alert-warning');

        try {
            const result = await rpc('/web/dataset/call_kw/account.move/check_lovecode', {
                model: 'account.move',
                method: 'check_lovecode',
                args: [value],
                kwargs: {},
            });

            target.disabled = false;
            if (result) {
                $alert.addClass('d-none');
            } else {
                $alert.text('愛心碼不存在').removeClass('alert-warning').addClass('alert-danger');
                target.focus();
            }
            sharedDataset.loveCode = result ? value : '';
        } catch (error) {
            console.error('ECPay: lovecode check RPC error:', error);
            target.disabled = false;
            $alert.text('驗證失敗，請稍後重試').removeClass('alert-warning').addClass('alert-danger');
            sharedDataset.loveCode = '';
        }
    },
});

// Extend PaymentForm to validate ECPay invoice before payment
PaymentForm.include({
    async _submitForm(ev) {
        // Capture _super before async operation (required for Odoo 18 include pattern)
        const _super = this._super.bind(this);

        // Validate ECPay invoice data before submitting payment
        const isValid = await this._ensureEcpayInvoiceAlright();
        if (!isValid) {
            return; // Don't proceed with payment
        }
        return _super(...arguments);
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

            console.log('ECPay: saving invoice data', params);
            const result = await rpc(route, params);
            console.log('ECPay: save result', result);
            return result === '200';
        } catch (error) {
            console.error('ECPay invoice save error:', error);
            this._displayErrorDialog('更新電子發票資訊失敗', '更新電子發票資訊失敗，請稍後重試');
            return false;
        }
    },

    _displayErrorDialog(title, message) {
        // Use Odoo 18 ConfirmationDialog
        this.call('dialog', 'add', ConfirmationDialog, { title: title, body: message || "" });
    },
});
