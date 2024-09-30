odoo.define('website_sale_tracking_base.stop_default_tracking', function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');
    require('website_sale.tracking');

    publicWidget.registry.websiteSaleTracking.include({
        /**
         * Skip default GA tracking.
         * @override
        */
        _trackGA: function () {}
    })
});
