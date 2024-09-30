odoo.define('website_sale_tracking_base.login_tracking', function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');
    const websiteSaleTrackingAlternative = require('website_sale_tracking_base.tracking');

    publicWidget.registry.websiteAuthTracking = websiteSaleTrackingAlternative.extend({
        selector: '.oe_website_login_container',
        events: {
            'click form.oe_login_form div.oe_login_buttons button.btn-primary': '_onClickLoginButton',
            'click form.oe_signup_form div.oe_login_buttons button.btn-primary': '_onClickSignupButton',
        },
        _onClickLoginButton: function () {
            this.trigger_up('tracking_login');
        },
        _onClickSignupButton: function () {
            this.trigger_up('tracking_sign_up');
        },
    });
    return publicWidget.registry.websiteAuthTracking;
});
