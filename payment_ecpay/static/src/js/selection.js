/** @odoo-module **/
// ECPay Payment Selection - Odoo 18 Compatible
// Migrated from Odoo 16 module syntax to ES6 modules

import PaymentForm from '@payment/js/payment_form';
import { rpc } from '@web/core/network/rpc';

PaymentForm.include({
    events: Object.assign({}, PaymentForm.prototype.events || {}, {
        'click .card-body.o_payment_option_card': '_payment_acquirer_select',
    }),

    start: async function () {
        await this._super(...arguments);
        // Deselect all payment options if more than one exists
        const radioButtons = this.el.querySelectorAll('input[name="o_payment_radio"]');
        if (radioButtons.length > 1) {
            radioButtons.forEach(radio => radio.checked = false);
        }
        this._payment_acquirer_select();
    },

    _payment_acquirer_select: function (ev) {
        // Show/hide ECPay payment method dropdown based on selected provider
        const form = this.el.querySelector('form[name="o_payment_checkout"]');
        if (!form) return;

        const acquirerInputs = form.querySelectorAll('input[name="o_payment_radio"]');
        const selector = form.querySelector('div.ecpay_payment_method');

        if (!selector) return;

        let showSelector = false;
        acquirerInputs.forEach(input => {
            if (input.dataset.provider === 'ecpay' && input.checked) {
                showSelector = true;
            }
        });

        if (showSelector) {
            selector.classList.remove('d-none');
        } else {
            selector.classList.add('d-none');
        }
    },

    async _submitForm(ev) {
        // Capture _super before async operation
        const _super = this._super.bind(this);

        // Save ECPay payment type to session before payment
        await this._saveEcpayPaymentType();

        return _super(...arguments);
    },

    async _saveEcpayPaymentType() {
        let payment_type = 'Credit'; // Default value
        const ecpayPaymentTypeElement = document.getElementById('ecpay_payment_type');

        if (ecpayPaymentTypeElement) {
            const selectedOption = ecpayPaymentTypeElement.querySelector(':checked') ||
                                   ecpayPaymentTypeElement.options?.[ecpayPaymentTypeElement.selectedIndex];
            if (selectedOption) {
                payment_type = selectedOption.value.trim();
            }
        }

        try {
            await rpc('/payment/ecpay/save_payment_type', { payment_type: payment_type });
            console.log('ECPay: Saved payment type to session:', payment_type);
        } catch (error) {
            console.error('ECPay: Failed to save payment type:', error);
            // Continue anyway, will use default 'Credit'
        }
    },
});
