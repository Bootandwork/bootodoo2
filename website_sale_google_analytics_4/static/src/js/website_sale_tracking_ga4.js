odoo.define('website_sale_google_analytics_4.tracking', function (require) {
"use strict";

var websiteSaleTrackingAlternative = require('website_sale_tracking_base.tracking');

websiteSaleTrackingAlternative.include({

    _trackingGoogleAnalytics4: function () {
        const websiteGA4 = window.gtag || function () {};
        if (this.trackingIsLogged()) {
            console.log('DO _trackGA');
        }
        websiteGA4.apply(this, arguments);
    },

    trackingSendEventData: function(eventType, eventData) {
        if (this.trackingIsLogged()) {
            console.log('-- RUN GA4 --');
        }
        if (eventData['ga4'] !== undefined && Array.isArray(eventData['ga4'])) {
            for(var i = 0; i < eventData['ga4'].length; i++) {
                if (this.trackingIsLogged()) {
                    console.log(eventData['ga4'][i]);
                }
                var run_script = eventData['ga4'][i]['run_script']
                var event_name = eventData['ga4'][i]['event_name']
                var event_data = eventData['ga4'][i]['data']
                if (event_data !== undefined && run_script !== undefined && run_script) {
                    this._trackingGoogleAnalytics4('event', event_name, event_data);
                }
            }
        }
        return this._super.apply(this, arguments);
    },
});
});
