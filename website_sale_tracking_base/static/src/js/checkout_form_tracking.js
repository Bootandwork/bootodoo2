odoo.define('website_sale_tracking_base.checkout_form', function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');
    const websiteSaleTrackingAlternative = require('website_sale_tracking_base.tracking');

    publicWidget.registry.PaymentCheckoutFormTracking = websiteSaleTrackingAlternative.extend({
        selector: 'form[name="o_payment_checkout"]',
        events: {
            'click button[name="o_payment_submit_button"]': '_onClickPayButton',
        },

        _onClickPayButton: function () {
            this.trigger_up('tracking_payment_info');
        },
    });
    return publicWidget.registry.PaymentCheckoutFormTracking;
});
