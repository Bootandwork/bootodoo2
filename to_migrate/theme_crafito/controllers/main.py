# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

import re
import math
import uuid
from werkzeug.exceptions import Forbidden, NotFound
from odoo import http, SUPERUSER_ID, fields
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers import main
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.web_editor.controllers.main import Web_Editor


class CrafitoSliderSettings(http.Controller):

    @http.route(['/theme_crafito/blog_get_options'], type='json', auth="public", website=True)
    def crafito_get_slider_options(self):
        slider_options = []
        option = request.env['blog.slider.config'].search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    @http.route(['/theme_crafito/blog_get_dynamic_slider'], type='json', auth='public', website=True)
    def crafito_get_dynamic_slider(self, slider_type=None, **post):
        if slider_type:
            slider_header = request.env['blog.slider.config'].sudo().search(
                [('id', '=', int(slider_type))])
            values = {
                'slider_header': slider_header,
                'blog_slider_details': slider_header.collections_blog_post,
            }
            return request.website.viewref("theme_crafito.theme_crafito_blog_slider_view").render(values)

    @http.route(['/theme_crafito/blog_image_effect_config'], type='json', auth='public', website=True)
    def crafito_product_image_dynamic_slider(self, **post):
        slider_data = request.env['blog.slider.config'].search(
            [('id', '=', int(post.get('slider_type')))])
        values = {
            's_id': str(slider_data.no_of_counts) + '-' + str(slider_data.id),
            'counts': slider_data.no_of_counts,
            'auto_rotate': slider_data.auto_rotate,
            'auto_play_time': slider_data.sliding_speed,
        }
        return values

    # For Client slider
    @http.route(['/theme_crafito/get_clients_dynamically_slider'], type='json', auth='public', website=True)
    def get_clients_dynamically_slider(self, **post):
        client_data = request.env['res.partner'].sudo().search(
            [('add_to_slider', '=', True)])
        values = {
            'client_slider_details': client_data,
        }
        return request.website.viewref("theme_crafito.theme_crafito_client_slider_view").render(values)

    # For multi product slider
    @http.route(['/theme_crafito/product_multi_get_options'], type='json', auth="public", website=True)
    def crafito_product_multi_get_slider_options(self):
        slider_options = []
        option = request.env['multi.slider.config'].search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    @http.route(['/theme_crafito/product_multi_get_dynamic_slider'], type='json', auth='public', website=True)
    def crafito_product_multi_get_dynamic_slider(self, slider_type=None, **post):
        context, pool = dict(request.context), request.env
        if slider_type:
            slider_header = request.env['multi.slider.config'].sudo().search(
                [('id', '=', int(slider_type))])
            if not context.get('pricelist'):
                pricelist = request.website.get_current_pricelist()
                context = dict(request.context, pricelist=int(pricelist))
            else:
                pricelist = pool.get('product.pricelist').browse(
                    context['pricelist'])

            context.update({'pricelist': pricelist.id})
            from_currency = pool['res.users'].sudo().browse(
                SUPERUSER_ID).company_id.currency_id
            to_currency = pricelist.currency_id

            def compute_currency(price): return pool[
                'res.currency']._convert(price, from_currency, to_currency, fields.Date.today())
            values = {
                'slider_details': slider_header,
                'slider_header': slider_header,
                'compute_currency': compute_currency
            }
            return request.website.viewref("theme_crafito.theme_crafito_multi_cat_slider_view").render(values)

    @http.route(['/theme_crafito/product_multi_image_effect_config'], type='json', auth='public', website=True)
    def crafito_product_multi_product_image_dynamic_slider(self, **post):
        slider_data = request.env['multi.slider.config'].search(
            [('id', '=', int(post.get('slider_type')))])
        values = {
            's_id': str(slider_data.no_of_collection) + '-' + str(slider_data.id),
            'counts': slider_data.no_of_collection,
            'auto_rotate': slider_data.auto_rotate,
            'auto_play_time': slider_data.sliding_speed,
        }
        return values

    @http.route(['/theme_crafito/newsone_get_dynamic_slider'], type='json', auth='public', website=True)
    def crafito_get_dynamic_newsone_slider(self, slider_type=None, **post):
        if slider_type:
            slider_header = request.env['blog.slider.config'].sudo().search(
                [('id', '=', int(slider_type))])
            values = {
                'slider_header': slider_header,
                'blog_slider_details': slider_header.collections_blog_post,
            }
            return request.website.viewref("theme_crafito.theme_crafito_news1_view").render(values)

    @http.route(['/theme_crafito/newstwo_get_dynamic_slider'], type='http', auth='public', website=True)
    def crafito_get_dynamic_newstwo_slider(self, slider_type=None, **post):
        if slider_type:
            slider_header = request.env['blog.slider.config'].sudo().search(
                [('id', '=', int(slider_type))])
            values = {
                'slider_header': slider_header,
                'blog_slider_details': slider_header.collections_blog_post,
            }
            return request.website.viewref("theme_crafito.theme_crafito_news2_view").render(values)

    @http.route(['/theme_crafito/theme_new_hardware_blog'], type='json', auth='public', website=True)
    def crafito_get_dynamic_hardwareblog_slider(self, slider_type=None, **post):
        if slider_type:
            slider_header = request.env['blog.slider.config'].sudo().search(
                [('id', '=', int(slider_type))])
            values = {
                'slider_header': slider_header,
                'blog_slider_details': slider_header.collections_blog_post,
            }
            return request.website.viewref("theme_crafito.theme_crafito_hardware_blog_snippet_view").render(values)

    # Coming soon snippet
    @http.route(['/biztech_comming_soon/soon_data'], type="http", auth="public", website=True)
    def get_soon_data(self, **post):
        return request.render("theme_crafito.theme_crafito_coming_soon_mode_one_view")

    @http.route(['/biztech_comming_soon_two/two_soon_data'], type="http", auth="public", website=True)
    def get_soon_data_two(self, **post):
        return request.render("theme_crafito.theme_crafito_coming_soon_mode_two_view")

    def find_snippet_employee(self):
        emp = {}
        employee = request.env['hr.employee'].sudo().search(
            [('include_inourteam', '=', 'True')])
        emp['biztech_employees'] = employee
        return emp

    # For team snippet
    @http.route(['/biztech_emp_data_one/employee_data'], type="json", auth="public", website=True)
    def get_one_employee_details_custom(self, **post):
        emp = self.find_snippet_employee()
        return request.website.viewref("theme_crafito.theme_crafito_team_one").render(emp)

    @http.route(['/biztech_emp_data/employee_data'], type="json", auth="public", website=True)
    def get_employee_detail_custom(self, **post):
        emp = self.find_snippet_employee()
        return request.website.viewref("theme_crafito.theme_crafito_team_two").render(emp)

    @http.route(['/biztech_emp_data_three/employee_data'], type="json", auth="public", website=True)
    def get_employee_detail_custom_1(self, **post):
        emp = self.find_snippet_employee()
        return request.website.viewref("theme_crafito.theme_crafito_team_three").render(emp)

    # For Category slider
    @http.route(['/theme_crafito/category_get_options'], type='json', auth="public", website=True)
    def category_get_slider_options(self):
        slider_options = []
        option = request.env['category.slider.config'].search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    @http.route(['/theme_crafito/category_get_dynamic_slider'], type='json', auth='public', website=True)
    def category_get_dynamic_slider(self, slider_id=None, **post):
        if slider_id:
            slider_header = request.env['category.slider.config'].sudo().search(
                [('id', '=', int(slider_id))])
            values = {
                'slider_header': slider_header
            }
            for category in slider_header.collections_category:
                domain = [('public_categ_ids', 'child_of', int(category))]
                search_product = request.env['product.template'].search_count(domain)
                category.linked_product_count = search_product
            values.update({
                'slider_details': slider_header.collections_category,
            })
            return request.website.viewref("theme_crafito.theme_crafito_cat_slider_view").render(values)

    @http.route(['/theme_crafito/category_image_effect_config'], type='json', auth='public', website=True)
    def category_image_dynamic_slider(self, **post):
        slider_data = request.env['category.slider.config'].search(
            [('id', '=', int(post.get('slider_id')))])
        values = {
            's_id': slider_data.name.lower().replace(' ', '-') + '-' + str(slider_data.id),
            'counts': slider_data.no_of_counts,
            'auto_rotate': slider_data.auto_rotate,
            'auto_play_time': slider_data.sliding_speed,
        }
        return values

    @http.route(['/biztech_fact_model_data/fact_data'], type="http", auth="public", website=True)
    def get_factsheet_data(self, **post):
        return request.render("theme_crafito.theme_crafito_facts_sheet_view")

    @http.route(['/biztech_skill_model_data/skill_data'], type="http", auth="public", website="True")
    def get_skill_data(self, **post):
        return request.render("theme_crafito.theme_crafito_skills_view")

    # Multi image gallery
    @http.route(['/theme_crafito/crafito_multi_image_effect_config'], type='json', auth="public", website=True)
    def get_multi_image_effect_config(self):

        cur_website = request.website
        values = {
            'no_extra_options': cur_website.no_extra_options,
            'theme_panel_position': cur_website.thumbnail_panel_position,
            'interval_play': cur_website.interval_play,
            'enable_disable_text': cur_website.enable_disable_text,
            'color_opt_thumbnail': cur_website.color_opt_thumbnail,
            'change_thumbnail_size': cur_website.change_thumbnail_size,
            'thumb_height': cur_website.thumb_height,
            'thumb_width': cur_website.thumb_width,
        }
        return values

    # For Product slider
    @http.route(['/theme_crafito/product_get_options'], type='json', auth="public", website=True)
    def product_get_slider_options(self):
        slider_options = []
        option = request.env['product.slider.config'].search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    @http.route(['/theme_crafito/product_get_dynamic_slider'], type='json', auth='public', website=True)
    def product_get_dynamic_slider(self, slider_id=None, **post):
        if slider_id:
            slider_header = request.env['product.slider.config'].sudo().search(
                [('id', '=', int(slider_id))])
            values = {
                'slider_header': slider_header
            }
            values.update({
                'slider_details': slider_header.collections_products,
            })
            return request.website.viewref("theme_crafito.theme_crafito_product_slider_view").render(values)

    @http.route(['/theme_crafito/product_image_effect_config'], type='json', auth='public', website=True)
    def product_image_dynamic_slider(self, **post):
        slider_data = request.env['product.slider.config'].search(
            [('id', '=', int(post.get('slider_id')))])
        values = {
            's_id': str(slider_data.id),
            'counts': slider_data.no_of_counts,
            'auto_rotate': slider_data.auto_rotate,
            'auto_play_time': slider_data.sliding_speed,
        }
        return values

    # For Featured Product slider
    @http.route(['/theme_crafito/featured_product_get_options'], type='json', auth="public", website=True)
    def featured_product_get_slider_options(self):
        slider_options = []
        option = request.env['feature.product.slider.config'].search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    @http.route(['/theme_crafito/featured_product_get_dynamic_slider'], type='json', auth='public', website=True)
    def featured_product_get_dynamic_slider(self, slider_id=None, **post):
        uid, context, pool = request.uid, dict(request.context), request.env
        if slider_id:
            slider_header = request.env['feature.product.slider.config'].sudo().search(
                [('id', '=', int(slider_id))])

            if not context.get('pricelist'):
                pricelist = request.website.get_current_pricelist()
                context = dict(request.context, pricelist=int(pricelist))
            else:
                pricelist = pool.get('product.pricelist').browse(
                    context['pricelist'])

            context.update({'pricelist': pricelist.id})

            from_currency = pool['res.users'].browse(
                uid).company_id.currency_id
            to_currency = pricelist.currency_id

            def compute_currency(price):
                return pool['res.currency']._convert(price, from_currency, to_currency, fields.Date.today())

            values = {
                'compute_currency': compute_currency,
                'slider_header': slider_header
            }
            return request.website.viewref("theme_crafito.theme_crafito_featured_product_slider_view").render(values)

    @http.route(['/theme_crafito/featured_product_image_effect_config'], type='json', auth='public', website=True)
    def featured_product_image_dynamic_slider(self, **post):
        slider_data = request.env['feature.product.slider.config'].search(
            [('id', '=', int(post.get('slider_id')))])
        values = {
            's_id': slider_data.name.lower().replace(' ', '-') + '-' + str(slider_data.id),
            'counts': slider_data.no_of_counts,
            'auto_rotate': slider_data.auto_rotate,
            'auto_play_time': slider_data.sliding_speed,
        }
        return values

    @http.route(['/theme_crafito/event_slider/get_data'], type="json", auth="public", website=True)
    def get_event_data(self, **post):
        events = request.env['event.type'].sudo().search([])
        values = {'main_events_category': events}
        return request.website.viewref("theme_crafito.theme_crafito_events_view").render(values)


class CrafitoEcommerceShop(WebsiteSale):

    @http.route()
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
        result = super(CrafitoEcommerceShop, self).cart_update_json(
            product_id, line_id, add_qty, set_qty, display)
        order = request.website.sale_get_order()
        result.update({'theme_crafito.hover_total': request.env['ir.ui.view'].render_template("theme_crafito.hover_total", {
            'website_sale_order': order})
        })
        return result

    @http.route('/shop/products/recently_viewed', type='json', auth='public', website=True)
    def products_recently_viewed(self, **kwargs):
        return self._get_crafito_products_recently_viewed()

    def _get_crafito_products_recently_viewed(self):
        max_number_of_product_for_carousel = 12
        visitor = request.env['website.visitor']._get_visitor_from_request()
        if visitor:
            excluded_products = request.website.sale_get_order().mapped(
                'order_line.product_id.id')
            products = request.env['website.track'].sudo().read_group(
                [('visitor_id', '=', visitor.id), ('product_id', '!=', False),
                 ('product_id', 'not in', excluded_products)],
                ['product_id', 'visit_datetime:max'], ['product_id'], limit=max_number_of_product_for_carousel, orderby='visit_datetime DESC')
            products_ids = [product['product_id'][0] for product in products]
            if products_ids:
                viewed_products = request.env['product.product'].browse(
                    products_ids)

                FieldMonetary = request.env['ir.qweb.field.monetary']
                monetary_options = {
                    'display_currency': request.website.get_current_pricelist().currency_id,
                }
                rating = request.website.viewref(
                    'theme_crafito.theme_crafito_rating').active
                res = {'products': []}
                for product in viewed_products:
                    combination_info = product._get_combination_info_variant()
                    res_product = product.read(
                        ['id', 'name', 'website_url'])[0]
                    res_product.update(combination_info)
                    res_product['price'] = FieldMonetary.value_to_html(
                        res_product['price'], monetary_options)
                    if rating:
                        res_product['rating'] = request.env["ir.ui.view"].render_template('website_rating.rating_widget_stars_static', values={
                            'rating_avg': product.rating_avg,
                            'rating_count': product.rating_count,
                        })
                    res['products'].append(res_product)

                return res
        return {}

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        if request.env['website'].sudo().get_current_website().theme_id.name == 'theme_crafito':
            result = super(CrafitoEcommerceShop, self).shop(
                page=page, category=category, search=search, ppg=ppg, ** post)
            add_qty = int(post.get('add_qty', 1))
            Category = request.env['product.public.category']
            if category:
                category = Category.search(
                    [('id', '=', int(category))], limit=1)
                if not category or not category.can_access_from_current_website():
                    raise NotFound()
            else:
                category = Category

            if ppg:
                try:
                    ppg = int(ppg)
                    post['ppg'] = ppg
                except ValueError:
                    ppg = False
            if not ppg:
                ppg = request.env['website'].get_current_website(
                ).shop_ppg or 20

            ppr = request.env['website'].get_current_website().shop_ppr or 4

            attrib_list = request.httprequest.args.getlist('attrib')
            attrib_values = [[int(x) for x in v.split("-")]
                             for v in attrib_list if v]
            attributes_ids = {v[0] for v in attrib_values}
            attrib_set = {v[1] for v in attrib_values}

            domain = self._get_search_domain(search, category, attrib_values)

            keep = QueryURL('/shop', category=category and int(category),
                            search=search, attrib=attrib_list, order=post.get('order'))

            pricelist_context, pricelist = self._get_pricelist_context()

            request.context = dict(
                request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

            url = "/shop"
            if search:
                post["search"] = search
            if attrib_list:
                post['attrib'] = attrib_list
            if post:
                request.session.update(post)
            sort_order = self._get_search_order(post)
            Product = request.env['product.template'].with_context(
                bin_size=True)
            session = request.session
            cate_for_price = None
            # For Product Sorting
            if session.get('sort_id'):
                session_sort = session.get('sort_id')
                sort = session_sort
                sort_field = request.env['biztech.product.sortby'].sudo().search([
                    ('id', '=', int(sort))])
                request.session['product_sort_name'] = sort_field.name
                order_field = sort_field.sort_on.name
                order_type = sort_field.sort_type
                sort_order = '%s %s' % (order_field, order_type)
                if post.get("sort_id"):
                    request.session["sortid"] = [
                        sort, sort_order, sort_field.name, order_type]

            is_price_slider = request.website.viewref(
                'theme_crafito.product_price_slider')
            # if is_price_slider and is_price_slider.active:
            if is_price_slider:
                # For Price slider

                is_discount_hide = True if request.website.get_current_pricelist(
                ).discount_policy == 'with_discount' else False

                product_slider_ids = []
                asc_product_slider_ids = Product.search(
                    domain, limit=1, order='list_price')
                desc_product_slider_ids = Product.search(
                    domain, limit=1, order='list_price desc')
                if asc_product_slider_ids:
                    # product_slider_ids.append(asc_product_slider_ids.website_price)
                    product_slider_ids.append(
                        asc_product_slider_ids.price if is_discount_hide else asc_product_slider_ids.list_price)
                if desc_product_slider_ids:
                    # product_slider_ids.append(desc_product_slider_ids.website_price)
                    product_slider_ids.append(
                        desc_product_slider_ids.price if is_discount_hide else desc_product_slider_ids.list_price)

                if product_slider_ids:
                    if post.get("range1") or post.get("range2") or not post.get("range1") or not post.get("range2"):
                        range1 = min(product_slider_ids)
                        range2 = max(product_slider_ids)
                        result.qcontext['range1'] = math.floor(range1)
                        result.qcontext['range2'] = math.ceil(range2)

                    if request.session.get('pricerange'):
                        if cate_for_price and request.session.get('curr_category') and request.session.get('curr_category') != int(cate_for_price):
                            request.session["min1"] = math.floor(range1)
                            request.session["max1"] = math.ceil(range2)

                    if session.get("min1") and session["min1"]:
                        post["min1"] = session["min1"]
                    if session.get("max1") and session["max1"]:
                        post["max1"] = session["max1"]
                    if range1:
                        post["range1"] = range1
                    if range2:
                        post["range2"] = range2
                    if range1 == range2:
                        post['range1'] = 0.0

                    if request.session.get('min1') or request.session.get('max1'):
                        if request.session.get('min1'):
                            if request.session['min1'] != None:
                                # ========== for hide list-website price diffrence ====================
                                if is_discount_hide:
                                    price_product_list = []
                                    product_withprice = Product.search(
                                        domain)
                                    for prod_id in product_withprice:
                                        if prod_id.price >= float(request.session['min1']) and prod_id.price <= float(request.session['max1']):
                                            price_product_list.append(
                                                prod_id.id)

                                    if price_product_list:
                                        domain += [('id', 'in',
                                                    price_product_list)]
                                    else:
                                        domain += [('id', 'in', [])]
                                else:
                                    domain += [('list_price', '>=', request.session.get('min1')),
                                               ('list_price', '<=', request.session.get('max1'))]
                                request.session["pricerange"] = str(
                                    request.session['min1'])+"-To-"+str(request.session['max1'])

                    if session.get('min1') and session['min1']:
                        result.qcontext['min1'] = session["min1"]
                        result.qcontext['max1'] = session["max1"]

            if cate_for_price:
                request.session['curr_category'] = int(cate_for_price)
            Product = request.env['product.template'].with_context(
                bin_size=True)

            search_product = Product.search(domain)
            website_domain = request.website.website_domain()
            categs_domain = [('parent_id', '=', False)] + website_domain
            if search:
                search_categories = Category.search(
                    [('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
                categs_domain.append(('id', 'in', search_categories.ids))
            else:
                search_categories = Category
            categs = Category.search(categs_domain)

            if category:
                url = "/shop/category/%s" % slug(category)

            product_count = len(search_product)
            pager = request.website.pager(
                url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
            products = Product.search(
                domain, limit=ppg, offset=pager['offset'], order=sort_order)

            ProductAttribute = request.env['product.attribute']
            if products:
                # get all products without limit
                attributes = ProductAttribute.search(
                    [('product_tmpl_ids', 'in', search_product.ids)])
            else:
                attributes = ProductAttribute.browse(attributes_ids)

            layout_mode = request.session.get('website_sale_shop_layout_mode')
            if not layout_mode:
                if request.website.viewref('website_sale.products_list_view').active:
                    layout_mode = 'list'
                else:
                    layout_mode = 'grid'

            result.qcontext.update({
                'search': search,
                'category': category,
                'attrib_values': attrib_values,
                'attrib_set': attrib_set,
                'pager': pager,
                'pricelist': pricelist,
                'add_qty': add_qty,
                'products': products,
                'search_count': product_count,  # common for all searchbox
                'bins': TableCompute().process(products, ppg, ppr),
                'ppg': ppg,
                'ppr': ppr,
                'categories': categs,
                'attributes': attributes,
                'keep': keep,
                'search_categories_ids': search_categories.ids,
                'layout_mode': layout_mode,
            })
            return result
        else:
            return super(CrafitoEcommerceShop, self).shop(page=page, category=category, search=search, ppg=ppg, **post)

    @http.route(['/theme_carfito/removeattribute'], type='json', auth='public', website=True)
    def remove_selected_attribute(self, **post):
        if post.get("attr_remove"):
            remove = post.get("attr_remove")
            if remove == "pricerange":
                if request.session.get('min1'):
                    del request.session['min1']
                if request.session.get('max1'):
                    del request.session['max1']
                request.session[remove] = ''
                return True
            elif remove == "sortid":
                request.session[remove] = ''
                request.session["sort_id"] = ''
                return True
                request.session[remove] = ''
                return True
            elif remove == "sortid":
                request.session[remove] = ''
                request.session["sort_id"] = ''
                return True
                request.session[remove] = ''
                return True
            elif remove == "sortid":
                request.session[remove] = ''
                request.session["sort_id"] = ''
                return True
                request.session[remove] = ''
                return True
            elif remove == "sortid":
                request.session[remove] = ''
                request.session["sort_id"] = ''
                return True
                request.session[remove] = ''
                return True
            elif remove == "sortid":
                request.session[remove] = ''
                request.session["sort_id"] = ''
                return True
