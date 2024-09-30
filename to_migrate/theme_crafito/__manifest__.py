# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    'name': 'Theme Crafito',
    'summary': 'Advanced Responsive Theme with A Range of Custom Snippets',
    'description': '''Theme Crafito
Business theme
Hardware theme
Hardware and tools theme
Single Page theme
Digital security theme
Event theme
Medical equipments theme
multipurpose template for industry
multipurpose template for all industries
odoo custom theme
customizable odoo theme
multi industry odoo theme
multi purpose responsive odoo theme
multipurpose website template for odoo
odoo multipurpose theme for industry
multipurpose templates for odoo
odoo ecommerce templates
odoo ecommerce theme
odoo ecommerce themes
odoo responsive themes
odoo website themes
odoo ecommerce website theme
odoo theme for ecommerce store
odoo bootstrap themes
customize odoo theme
odoo ecommerce store theme for business
odoo theme for business
odoo responsive website theme
Crafito Theme
Odoo Crafito Theme
Crafito theme for Odoo
odoo 11 theme
multipurpose theme
odoo multipurpose theme
odoo responsive theme
responsive theme
odoo theme
odoo themes
ecommerce theme
odoo ecommerce themes
odoo website themes
odoo bootstrap themes
bootstrap themes
bootstrap theme
customize odoo theme
ecommerce store theme
theme for business
theme for ecommerce store
    ''',
    'category': 'Theme/Ecommerce',
    'version': '13.0.1.0.5',
    'license': 'OPL-1',
    'author': 'AppJetty',
    'website': 'https://www.appjetty.com/',
    'depends': [
        # 'website_theme_install',
        'mass_mailing',
        'hr',
        'website_sale',
        'website_blog',
        'website_event_sale',
        'website_sale_comparison',
        'website_sale_wishlist',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/website_data.xml',
        # 'views/assets.xml',
        'views/views.xml',
        'views/website_view.xml',
        'views/slider_views.xml',
        'views/snippets.xml',
        'views/theme_customize.xml',
        'views/theme.xml',
    ],
    'support': 'support@appjetty.com',
    'live_test_url': 'https://theme-crafito-v12.appjetty.com/',
    'images': [
        'static/description/splash-screen.png',
        'static/description/splash-screen_screenshot.png',
    ],
    'application': True,
    'price': 79.00,
    'currency': 'EUR',
    'installable': True,
    "assets": {
        "web.assets_backend": ["theme_crafito/static/src/css/plugins/owl.carousel.css",
                               "theme_crafito/static/src/css/plugins/unite-gallery.css",
                               "theme_crafito/static/src/css/plugins/ion.rangeSlider.css",
                               "theme_crafito/static/src/css/plugins/ion.rangeSlider.skinHTML5.css",
                               "theme_crafito/static/src/skins/alexis/alexis.css",
                               "theme_crafito/static/src/scss/variable.scss",
                               "theme_crafito/static/src/scss/colors/color_picker.scss",
                               "theme_crafito/static/src/scss/colors/color_picker_sec.scss",
                               "theme_crafito/static/src/scss/mixins.scss",
                               "theme_crafito/static/src/scss/custom.scss",
                               "theme_crafito/static/src/scss/header.scss",
                               "theme_crafito/static/src/scss/footer.scss",
                               "theme_crafito/static/src/scss/skills.scss",
                               "theme_crafito/static/src/scss/testimonial.scss",
                               "theme_crafito/static/src/scss/product-detail-page.scss",
                               "theme_crafito/static/src/scss/theme_common.scss",
                               "theme_crafito/static/src/js/plugins/jquery.waypoints.min.js",
                               "theme_crafito/static/src/js/plugins/jquery.counterup.js",
                               "theme_crafito/static/src/js/plugins/owl.carousel.min.js",
                               "theme_crafito/static/src/js/plugins/ion.rangeSlider.min.js",
                               "theme_crafito/static/src/js/plugins/carousel-swipe.js",
                               "theme_crafito/static/src/js/plugins/jquery.circleGraphic.js",
                               "theme_crafito/static/src/js/plugins/unitegallery.min.js",
                               "theme_crafito/static/src/js/plugins/ug-theme-compact.js",
                               "theme_crafito/static/src/js/crafito_frontend.js",
                               "theme_crafito/static/src/js/plugins/jquery.easing.1.3.js",
                               "theme_crafito/static/src/js/plugins/jquery.quicksand.js",
                               "theme_crafito/static/src/js/crafito_custom.js",
                               "theme_crafito/static/src/js/rating_state.js",
                               "theme_crafito/static/src/js/crafito_common_custom.js"],
        'website.assets_editor': ["theme_crafito/static/src/js/crafito_editor.js",
                                  "theme_crafito/static/src/js/widget/theme.js"],
    },
}
