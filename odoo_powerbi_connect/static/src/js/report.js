/** @odoo-module */
/* Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */


import { FormController } from "@web/views/form/form_controller";
import { formView } from '@web/views/form/form_view';
import { registry } from '@web/core/registry';

var ajax = require("web.ajax");

export class PowerbiReportController extends FormController {
    setup() {
        super.setup();
        this.render_powerbi_report();        
    }

    render_powerbi_report() {
        var resId = this.props.resId
        
        // jsonRpc call for getting Embed Token and Embed Url
        ajax.jsonRpc('/get/reportparameter', 'call', {
            'res_id': resId,
        })
        .then( function(data){
            var container = document.getElementById('powerbi_report_container');

            var reportContainer = container;

            // Initializing iframe for embedding report
            powerbi.bootstrap(reportContainer, { type: "report" });

            var models = window["powerbi-client"].models;
            var reportData = {
                type: "report",
                tokenType: models.TokenType.Embed,
    
                // Enable this setting to remove gray shoulders from embedded report
                settings: {
                        background: models.BackgroundType.Transparent
                    }
            };
            reportData.accessToken = data.embed_token;
            reportData.embedUrl = data.embed_url;

            // Embedding Power BI report using Access token and Embed Url
            var report = powerbi.embed(reportContainer, reportData);

            // This will be triggered when a report schema is successfully loaded
            report.on("loaded", function () {
                console.log("Report successfully loaded.")
            });

            // This will be triggered when a report is successfully embedded in UI
            report.on("rendered", function () {
                console.log("Report successfully rendered.")
            });

            // Clear any other error handler event
            // report.off("error");

            // Printing errors that occur during embedding
            report.on("error", function (event) {
                var errorMsg = event.detail;
                console.error(errorMsg);
                return;
            });
        });
    }
};

registry.category('views').add('powerbi_report_form', {
    ...formView,
    Controller: PowerbiReportController,
}); 
