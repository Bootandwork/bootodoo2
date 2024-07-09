/** @odoo-module */

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { RTActivityMgmtDashboard } from "@rt_activity_mgmt/components/activity_dashboard";

export class RTActivityMgmtKanbanRenderer extends KanbanRenderer {}

RTActivityMgmtKanbanRenderer.template = "rt_activity_mgmt.RTActivityMgmtKanbanRenderer";
RTActivityMgmtKanbanRenderer.components = Object.assign({}, KanbanRenderer.components, { RTActivityMgmtDashboard });

export const RTActivityMgmtKanbanActivityDashboard = {
    ...kanbanView,
    Renderer: RTActivityMgmtKanbanRenderer,
};

registry.category("views").add("rt_activity_mgmt_kanban_activity_dashboard", RTActivityMgmtKanbanActivityDashboard);
