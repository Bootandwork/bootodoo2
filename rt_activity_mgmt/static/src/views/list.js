/** @odoo-module */

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";

import { RTActivityMgmtDashboard } from "@rt_activity_mgmt/components/activity_dashboard";


export class RTActivityMgmtListRenderer extends ListRenderer {}

RTActivityMgmtListRenderer.template = "rt_activity_mgmt.RTActivityMgmtListRenderer";
RTActivityMgmtListRenderer.components = Object.assign({}, ListRenderer.components, { RTActivityMgmtDashboard });

export const RTActivityMgmtListActivityDashboard = {
    ...listView,
    Renderer: RTActivityMgmtListRenderer,
};

registry.category("views").add("rt_activity_mgmt_list_activity_dashboard", RTActivityMgmtListActivityDashboard);
