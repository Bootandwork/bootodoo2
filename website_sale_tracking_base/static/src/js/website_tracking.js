odoo.define('website_sale_tracking_base.website_tracking', function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');
    const websiteSaleTrackingAlternative = require('website_sale_tracking_base.tracking');

    publicWidget.registry.websiteTrackingAlternative = websiteSaleTrackingAlternative.extend({
        selector: 'span.fa.fa-4x.fa-thumbs-up.mx-auto.rounded-circle.bg-primary',

        start: function (ev) {
            this.trigger_up('tracking_lead');
            return this._super.apply(this, arguments);
        },
    });
    return publicWidget.registry.websiteTrackingAlternative;
});



