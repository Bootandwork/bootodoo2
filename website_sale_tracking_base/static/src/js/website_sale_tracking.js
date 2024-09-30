odoo.define('website_sale_tracking_base.tracking', function (require) {
    "use strict";

    const trackingDataRoute = '/shop/tracking_data';
    const publicWidget = require('web.public.widget');

    publicWidget.registry.websiteSaleTrackingAlternative = publicWidget.Widget.extend({
        selector: '.oe_website_sale',
        events: {
            'click button.o_add_wishlist_dyn': 'trackingEventAddToWishlist',
            'click button.o_add_wishlist': 'trackingEventAddToWishlistFromList',
            'click button.o_wish_add': 'trackingEventAddToCartFromList',
            'click #add_to_cart': 'trackingEventAddToCart',
            'click div.o_wsale_product_grid_wrapper form[action="/shop/cart/update"] a.a-submit': 'trackingEventAddToCartFromList',
            'click div.flex-column a.btn-primary.float-end, div.js_cart_summary a.btn-secondary.float-end': 'trackingEventBeginCheckout',
            'click a[href="#"].a-submit-loading': 'trackingEventAddShippingInfo',
        },
        custom_events: {
            tracking_lead: 'trackingEventLead',
            tracking_login: 'trackingEventLogin',
            tracking_sign_up: 'trackingEventSignUp',
            tracking_payment_info: 'trackingEventAddPaymentInfo',
        },

        trackingIsLogged: function() {
            var logTrackingEvents = document.querySelector('body').getAttribute('data-log-tracking-events');
            return (typeof logTrackingEvents !== 'undefined' && logTrackingEvents)
        },

        start: function (ev) {
            var self = this;
            this.trackingLogPrefix = '[Tracking] ';
            // view_item
            const $productView = this.$('div#product_details')
            if ($productView.length) {
                if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'View Product') }
                var params = this.trackingGetProductParams();
                params['event_type'] = 'view_product';
                this.trackingExecuteEvent(params);
            }
            // view_item_list or search
            const $productsGrid = this.$('div#products_grid')
            if ($productsGrid.length) {
                var productTemplateIds = $productsGrid.attr('data-tracking_product_tmpl_ids');
                var productCategory = $productsGrid.attr('data-tracking_category')
                if (productTemplateIds) {
                    if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'View Product List') }
                    this.trackingExecuteEvent({
                        event_type: 'view_product_list',
                        product_ids: productTemplateIds && JSON.parse(productTemplateIds) || [],
                        product_category: parseInt(productCategory, 10),
                    });
                }
                if (productCategory) {
                    if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'View Product Category') }
                    this.trackingExecuteEvent({
                        event_type: 'view_product_category',
                        product_ids: productTemplateIds && JSON.parse(productTemplateIds) || [],
                        product_category: parseInt(productCategory, 10),
                    });
                }
                var searchTerm = $productsGrid.attr('data-tracking_search_term')
                if (searchTerm) {
                    if (self.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'Search') }
                    this.trackingExecuteEvent({
                        event_type: 'search_product',
                        search_term: searchTerm,
                        product_ids: productTemplateIds && JSON.parse(productTemplateIds) || [],
                    });
                }
            }
            // purchase
            const $confirmation = this.$('div.oe_website_sale_tx_status');
            if ($confirmation.length) {
                if (self.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'Purchase') }
                this.trackingExecuteEvent({
                    event_type: 'purchase',
                    order_id: parseInt($confirmation.data('order-id'), 10),
                });
            }
            return this._super.apply(this, arguments);
        },

        trackingEventLead: function (ev) {
            if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'Lead (Contact Us - Thank You!)') }
            this.trackingExecuteEvent({ event_type: 'lead' });
        },

        trackingEventLogin: function (ev) {
            if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'User Login') }
            this.trackingExecuteEvent({ event_type: 'login' });
        },

        trackingEventSignUp: function (ev) {
            if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'Sign Up') }
            this.trackingExecuteEvent({ event_type: 'sign_up' });
        },

        trackingEventAddToWishlist: function (ev) {
            if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'Add To Wishlist (Product)') }
            var params = this.trackingGetProductParams();
            params['event_type'] = 'add_to_wishlist';
            this.trackingExecuteEvent(params);
        },

       trackingEventAddToWishlistFromList: function (ev) {
            //if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'Add To Wishlist (Product List)') }
            /*var params = this.trackingGetProductParams(ev.currentTarget.parentNode);
            params['event_type'] = 'add_to_wishlist';
            this.trackingExecuteEvent(params);*/
            if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'Add To Wishlist (Product List)') }
            var params = {};
            params['event_type'] = 'add_to_wishlist';
            console.log(params);
            this.trackingExecuteEvent(params);
        },

        trackingEventAddToCart: function (ev) {
            if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'Add To Cart (Product)') }
            var params = this.trackingGetProductParams();
            params['event_type'] = 'add_to_cart';
            this.trackingExecuteEvent(params);
        },

        trackingEventAddToCartFromList: function (ev) {
            if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'Add To Cart (Product List)') }
            var params = this.trackingGetProductParams(ev.currentTarget.parentNode);
            params['event_type'] = 'add_to_cart';
            this.trackingExecuteEvent(params);
        },

        trackingEventBeginCheckout: function (ev) {
            if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'Begin Checkout') }
            this.trackingExecuteEvent({ event_type: 'begin_checkout' });
        },

        trackingEventAddShippingInfo: function(ev) {
            if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'Add Shipping Info') }
            this.trackingExecuteEvent({ event_type: 'add_shipping_info' });
        },

        trackingEventAddPaymentInfo: async function(ev) {
            if (this.trackingIsLogged()) { console.log(this.trackingLogPrefix + 'Add Payment Info') }
            this.trackingExecuteEvent({ event_type: 'add_payment_info' });
        },

        trackingGetProductParams: function(el) {
        var my_elem = document;
        if (el) { my_elem = el}
            var params = {};

            var product_template_id = my_elem.querySelector('input[name="product_template_id"]');
            var product_id = my_elem.querySelector('input[name="product_id"]');
            var add_qty = my_elem.querySelector('input[name="add_qty"]');

            // The select "product_id" on prior way
            if (product_id) {
                params['item_type'] = 'product.product';
                params['product_ids'] = [parseInt(product_id.value, 10)];
            } else {
                params['item_type'] = 'product.template';
                params['product_ids'] = [parseInt(product_template_id.value, 10)];
            }
            if (add_qty) {
                params['product_qty'] = parseInt(add_qty.value, 10);
            }

            if (this.trackingIsLogged()) {
                console.log(this.trackingLogPrefix + 'Item Parameters:');
                console.log(params);
            }
            return params;
        },

        trackingExecuteEvent: function(params) {
            var self = this
            this._rpc({
                route: trackingDataRoute,
                params: params,
                kwargs: {},
            }).then(function (trackingResponse) {
                if (self.trackingIsLogged()) {
                    if (trackingResponse['error']) {
                        console.log(self.trackingLogPrefix + 'ERROR: ' + trackingResponse['error']);
                    }
                    console.log('>>> trackingResponse:');
                    console.log(trackingResponse);
                }
                if (trackingResponse['services'] !== undefined && trackingResponse['services']) {
                    self.trackingSendEventData(params['event_type'], trackingResponse['services']);
                }
            }).catch(error => console.log(error))
        },

        trackingSendEventData: function(eventType, eventData) {
            if (this.trackingIsLogged()) {
                console.log('-- SEND DATA --');
            }
        },

    });
    return publicWidget.registry.websiteSaleTrackingAlternative;
});
