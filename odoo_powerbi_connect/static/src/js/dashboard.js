/** @odoo-module */
/* Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */


import { FormController } from "@web/views/form/form_controller";
import { formView } from '@web/views/form/form_view';
import { registry } from '@web/core/registry';

var ajax = require("web.ajax");

export class PowerbiDashboardController extends FormController {
    setup() {
        super.setup();
        this.render_powerbi_dashboard();        
    }

    render_powerbi_dashboard() {
        var resId = this.props.resId
        
        // jsonRpc call for getting Embed Token and Embed Url
        ajax.jsonRpc('/get/dashboardparameter', 'call', {
            'res_id': resId,
        })
        .then( function(data){
            var container = document.getElementById('powerbi_dashboard_container');

            var dashboardContainer = container;
    
            // Initializing iframe for embedding dashboard
            powerbi.bootstrap(dashboardContainer, { type: "dashboard" });
                    
            var models = window["powerbi-client"].models;
            var dashboardData = {
                type: "dashboard",
                tokenType: models.TokenType.Embed,
    
                // Enable this setting to remove gray shoulders from embedded dashboard
                settings: {
                    background: models.BackgroundType.Transparent
                }
            };
            dashboardData.accessToken = data.embed_token;
            dashboardData.embedUrl = data.embed_url;

            // Embedding Power BI dashboard using Access token and Embed URL
            var dashboard = powerbi.embed(dashboardContainer, dashboardData);

            // This will be triggered when a dashboard schema is successfully loaded
            dashboard.on("loaded", function () {
                console.log("Dashboard load successful")
            });
                
            // This will be triggered when a dashboard is successfully embedded in UI
            dashboard.on("rendered", function () {
                console.log("Dashboard render successful")
            });
                
            // Clear any other error handler event
            // dashboard.off("error");
                
            // Printing errors that occur during embedding
            dashboard.on("error", function (event) {
                var errorMsg = event.detail;
                console.error(errorMsg);
                return;
            });
        });
    }
};

registry.category('views').add('powerbi_dashboard_form', {
    ...formView,
    Controller: PowerbiDashboardController,
}); 
