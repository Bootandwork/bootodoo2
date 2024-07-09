# -*- coding: utf-8 -*-

{
    "name": "Activity Management | Activity Dashboard | Activity Monitoring | Activity Views",
    "version": "16.0.4",
    "license": "OPL-1",
    "support": "relief.4technologies@gmail.com",
    "author": "Relief Technologies",
    "live_test_url": "https://youtu.be/p93lhTYTMOI",
    "category": "Activity Management/Activity",
    "summary": "schedule activity management Mail Activity Board daily to do management to do list crm activity management sale activity management",
    "description": """

    """,
    "depends": ["base", "mail"],
    "data": [
        "security/activity_security.xml",
        "security/ir.model.access.csv",
        "views/activity_tag.xml",
        "views/mail_activity.xml",
        "views/mail_message_views.xml",

    ],
    'assets': {
        'web.assets_backend': [
            # ACTIVITY DASHBOARD
            'rt_activity_mgmt/static/src/components/activity_dashboard.js',
            'rt_activity_mgmt/static/src/components/activity_dashboard.xml',
            'rt_activity_mgmt/static/src/components/activity_dashboard.scss',

            # ACTIVITY LIST VIEW
            'rt_activity_mgmt/static/src/views/list.js',
            'rt_activity_mgmt/static/src/views/list.xml',

            # ACTIVITY KANBAN VIEW
            'rt_activity_mgmt/static/src/views/kanban.js',
            'rt_activity_mgmt/static/src/views/kanban.xml',

        ],
    },


    "images": ["static/description/background.png",],
    "installable": True,
    "application": True,
    "auto_install": False,
    "price": 35,
    "currency": "EUR"
}
