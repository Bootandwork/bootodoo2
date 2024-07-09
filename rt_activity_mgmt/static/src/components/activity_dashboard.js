/** @odoo-module */

import {  useService } from "@web/core/utils/hooks";

const { Component, useState, onWillUpdateProps ,onWillStart} = owl;

export class RTActivityMgmtDashboard extends Component {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.state = useState({
            infos: {},
        });
        onWillStart(async () => {
            await this._fetch_rt_activity_mgmt_dashboard_data([this.props.domain])
        });
        onWillUpdateProps(this.willUpdate);
    }

    async willUpdate(nextProps) {
        await this._fetch_rt_activity_mgmt_dashboard_data([nextProps.domain])
    }

    async _fetch_rt_activity_mgmt_dashboard_data(domain = []) {
        this.state.infos= await this.orm.call(
            "mail.activity",
            "rt_activity_mgmt_retrieve_dashboard",
            domain
        );
    }
}

RTActivityMgmtDashboard.props = ["domain"];
RTActivityMgmtDashboard.template = 'rt_activity_mgmt.RTActivityMgmtDashboard';