# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

import re
import math
from odoo import http, SUPERUSER_ID
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_sale.controllers import main
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute


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

    @http.route(['/theme_crafito/blog_get_dynamic_slider'], type='http', auth='public', website=True)
    def crafito_get_dynamic_slider(self, **post):
        if post.get('slider-type'):
            slider_header = request.env['blog.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            values = {
                'slider_header': slider_header,
                'blog_slider_details': slider_header.collections_blog_post,
            }
            return request.render("theme_crafito.theme_crafito_blog_slider_view", values)

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
    @http.route(['/theme_crafito/get_clients_dynamically_slider'], type='http', auth='public', website=True)
    def get_clients_dynamically_slider(self, **post):
        client_data = request.env['res.partner'].sudo().search(
            [('add_to_slider', '=', True)])
        values = {
            'client_slider_details': client_data,
        }
        return request.render("theme_crafito.theme_crafito_client_slider_view", values)

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

    @http.route(['/theme_crafito/product_multi_get_dynamic_slider'], type='http', auth='public', website=True)
    def crafito_product_multi_get_dynamic_slider(self, **post):
        context, pool = dict(request.context), request.env
        if post.get('slider-type'):
            slider_header = request.env['multi.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            if not context.get('pricelist'):
                pricelist = request.website.get_current_pricelist()
                context = dict(request.context, pricelist=int(pricelist))
            else:
                pricelist = pool.get('product.pricelist').browse(context['pricelist'])

            context.update({'pricelist': pricelist.id})
            from_currency = pool['res.users'].sudo().browse(SUPERUSER_ID).company_id.currency_id
            to_currency = pricelist.currency_id
            compute_currency = lambda price: pool[
                'res.currency']._compute(from_currency, to_currency, price)
            values = {
                'slider_details': slider_header,
                'slider_header': slider_header,
                'compute_currency': compute_currency
            }
            return request.render("theme_crafito.theme_crafito_multi_cat_slider_view", values)

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

    @http.route(['/theme_crafito/newsone_get_dynamic_slider'], type='http', auth='public', website=True)
    def crafito_get_dynamic_newsone_slider(self, **post):
        if post.get('slider-type'):
            slider_header = request.env['blog.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            values = {
                'slider_header': slider_header,
                'blog_slider_details': slider_header.collections_blog_post,
            }
            return request.render("theme_crafito.theme_crafito_news1_view", values)

    @http.route(['/theme_crafito/newstwo_get_dynamic_slider'], type='http', auth='public', website=True)
    def crafito_get_dynamic_newstwo_slider(self, **post):
        if post.get('slider-type'):
            slider_header = request.env['blog.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            values = {
                'slider_header': slider_header,
                'blog_slider_details': slider_header.collections_blog_post,
            }
            return request.render("theme_crafito.theme_crafito_news2_view", values)

    @http.route(['/theme_crafito/theme_new_hardware_blog'], type='http', auth='public', website=True)
    def crafito_get_dynamic_hardwareblog_slider(self, **post):
        if post.get('slider-type'):
            slider_header = request.env['blog.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            values = {
                'slider_header': slider_header,
                'blog_slider_details': slider_header.collections_blog_post,
            }
            return request.render("theme_crafito.theme_crafito_hardware_blog_snippet_view", values)

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
    @http.route(['/biztech_emp_data_one/employee_data'], type="http", auth="public", website=True)
    def get_one_employee_details_custom(self, **post):
        emp = self.find_snippet_employee()
        return request.render("theme_crafito.theme_crafito_team_one", emp)

    @http.route(['/biztech_emp_data/employee_data'], type="http", auth="public", website=True)
    def get_employee_detail_custom(self, **post):
        emp = self.find_snippet_employee()
        return request.render("theme_crafito.theme_crafito_team_two", emp)

    @http.route(['/biztech_emp_data_three/employee_data'], type="http", auth="public", website=True)
    def get_employee_detail_custom_1(self, **post):
        emp = self.find_snippet_employee()
        return request.render("theme_crafito.theme_crafito_team_three", emp)

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

    @http.route(['/theme_crafito/category_get_dynamic_slider'], type='http', auth='public', website=True)
    def category_get_dynamic_slider(self, **post):
        if post.get('slider-id'):
            slider_header = request.env['category.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-id')))])
            values = {
                'slider_header': slider_header
            }
            for category in slider_header.collections_category:
                query = """
                    SELECT
                        count(product_template_id)
                    FROM
                        product_public_category_product_template_rel
                    WHERE
                        product_public_category_id in %s
                """
                request.env.cr.execute(query, (tuple([category.id]),))
                product_details = request.env.cr.fetchone()
                category.linked_product_count = product_details[0]
            values.update({
                'slider_details': slider_header.collections_category,
            })
            return request.render("theme_crafito.theme_crafito_cat_slider_view", values)

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

    @http.route(['/theme_crafito/product_get_dynamic_slider'], type='http', auth='public', website=True)
    def product_get_dynamic_slider(self, **post):
        if post.get('slider-id'):
            slider_header = request.env['product.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-id')))])
            values = {
                'slider_header': slider_header
            }
            values.update({
                'slider_details': slider_header.collections_products,
            })
            return request.render("theme_crafito.theme_crafito_product_slider_view", values)

    @http.route(['/theme_crafito/product_image_effect_config'], type='json', auth='public', website=True)
    def product_image_dynamic_slider(self, **post):
        slider_data = request.env['product.slider.config'].search(
            [('id', '=', int(post.get('slider_id')))])
        values = {
            's_id': slider_data.name.lower().replace(' ', '-') + '-' + str(slider_data.id),
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

    @http.route(['/theme_crafito/featured_product_get_dynamic_slider'], type='http', auth='public', website=True)
    def featured_product_get_dynamic_slider(self, **post):
        uid, context, pool = request.uid, dict(request.context), request.env
        if post.get('slider-id'):
            slider_header = request.env['feature.product.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-id')))])

            if not context.get('pricelist'):
                pricelist = request.website.get_current_pricelist()
                context = dict(request.context, pricelist=int(pricelist))
            else:
                pricelist = pool.get('product.pricelist').browse(context['pricelist'])

            context.update({'pricelist': pricelist.id})

            from_currency = pool['res.users'].browse(uid).company_id.currency_id
            to_currency = pricelist.currency_id
            compute_currency = lambda price: pool[
                'res.currency']._compute(from_currency, to_currency, price)

            values = {
                'compute_currency': compute_currency,
                'slider_header': slider_header
            }
            return request.render("theme_crafito.theme_crafito_featured_product_slider_view", values)

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

    @http.route(['/theme_crafito/event_slider/get_data'], type="http", auth="public", website=True)
    def get_event_data(self, **post):
        events = request.env['event.type'].sudo().search([])
        values = {'main_events_category': events}
        return request.render("theme_crafito.theme_crafito_events_view", values)


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

    @http.route([],
                type='http',
                auth='public',
                website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        result = super(CrafitoEcommerceShop, self).shop(
            page=page, category=category, search=search, **post)

        # odoo11
        # for displaying after whishlist or add to cart button n product_detail page
        if request.env.get('product.attribute.category') != None:
            compare_tmpl_obj = request.env.ref('website_sale_comparison.product_add_to_compare')
            if compare_tmpl_obj and compare_tmpl_obj.priority != 20:
                compare_tmpl_obj.sudo().write({'priority': 20})

        sort_order = ""
        cat_id = []
        ppg = 18
        product_temp = []
        newproduct = []
        # product template object
        product_obj = request.env['product.template']

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [list(map(int, v.split("-"))) for v in attrib_list if v]
        attributes_ids = set([v[0] for v in attrib_values])
        attrib_set = set([v[1] for v in attrib_values])
        domain = request.website.sale_product_domain()
        domain += self._get_search_domain(search, category, attrib_values)
        url = "/shop"

        if post:
            request.session.update(post)

        prevurl = request.httprequest.referrer
        if prevurl:
            if not re.search('/shop', prevurl, re.IGNORECASE):
                request.session['sortid'] = ""
                request.session['sort_id'] = ""
                request.session['pricerange'] = ""
                request.session['min1'] = ""
                request.session['max1'] = ""
                request.session['curr_category'] = ""

        session = request.session
        cate_for_price = None
        # for category filter
        if category:
            cate_for_price = int(category)

            category = request.env['product.public.category'].browse(int(category))
            url = "/shop/category/%s" % slug(category)

        if category != None:
            for ids in category:
                cat_id.append(ids.id)
            domain += ['|', ('public_categ_ids.id', 'in', cat_id),
                       ('public_categ_ids.parent_id', 'in', cat_id)]

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

        is_price_slider = request.env.ref('theme_crafito.product_price_slider')
        if is_price_slider and is_price_slider.active:
            # For Price slider

            is_discount_hide = True if request.website.get_current_pricelist(
            ).discount_policy == 'with_discount' else False

            product_slider_ids = []
            asc_product_slider_ids = product_obj.search(domain, limit=1, order='list_price')
            desc_product_slider_ids = product_obj.search(domain, limit=1, order='list_price desc')
            if asc_product_slider_ids:
                # product_slider_ids.append(asc_product_slider_ids.website_price)
                product_slider_ids.append(
                    asc_product_slider_ids.website_price if is_discount_hide else asc_product_slider_ids.list_price)
            if desc_product_slider_ids:
                # product_slider_ids.append(desc_product_slider_ids.website_price)
                product_slider_ids.append(
                    desc_product_slider_ids.website_price if is_discount_hide else desc_product_slider_ids.list_price)

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
                                product_withprice = product_obj.search(domain)
                                for prod_id in product_withprice:
                                    if prod_id.website_price >= float(request.session['min1']) and prod_id.website_price <= float(request.session['max1']):
                                        price_product_list.append(prod_id.id)

                                if price_product_list:
                                    domain += [('id', 'in', price_product_list)]
                                else:
                                    domain += [('id', 'in', [])]
                            else:
                                domain += [('list_price', '>=', request.session.get('min1')),
                                           ('list_price', '<=', request.session.get('max1'))]
# ==============================
                            request.session["pricerange"] = str(
                                request.session['min1'])+"-To-"+str(request.session['max1'])

                if session.get('min1') and session['min1']:
                    result.qcontext['min1'] = session["min1"]
                    result.qcontext['max1'] = session["max1"]

        if cate_for_price:
            request.session['curr_category'] = int(cate_for_price)

        product_count = product_obj.search_count(domain)
        pager = request.website.pager(
            url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = product_obj.search(domain, limit=ppg, offset=pager['offset'], order=sort_order)

        result.qcontext.update({'search_count': product_count,
                                'products': products,
                                'category': category,
                                'pager': pager,
                                'bins': TableCompute().process(products, ppg)})
        result.qcontext['domain'] = domain

        return result

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
