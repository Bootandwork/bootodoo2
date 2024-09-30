//
// This file is meant to regroup your javascript code. You can either copy/past
// any code that should be executed on each page loading or write your own
// taking advantage of the Odoo framework to create new behaviors or modify
// existing ones. For example, doing this will greet any visitor with a 'Hello,
// world !' message in a popup:
//
/*
odoo.define('website.user_custom_code', function (require) {
'use strict';

var Dialog = require('web.Dialog');
var publicWidget = require('web.public.widget');

publicWidget.registry.HelloWorldPopup = publicWidget.Widget.extend({
    selector: '#wrapwrap',

    start: function () {
        Dialog.alert(this, "Hello, world!");
        return this._super.apply(this, arguments);
    },
})
});
*/

$(".tab-content").each(function() {
  $(this).children(".tab-pane").first().addClass("show");
});

// per treure la fila de delivery amb DHL a la taula de other information de la fitxa de producte
$('#myMeas').find('tr:last-child').remove();

// per treure la directiva mèdica
//$('#mySec tr td').eq(1).remove();

/*
$( "#footer" ).remove();
$( ".o_footer_copyright" ).remove();
*/
/* per treure els links de les tags*/
$('a[href*="/tag/"]').removeAttr('href');


// per la geolocalitzacio a la pagina Distributors
// obtenim codi pais i iterem per fer visible
 /*$.get("https://ipinfo.io", function(response) {
    var c = response.country;
    console.log(c);
    var elements = document.getElementsByClassName(response.country);
    Array.prototype.forEach.call(elements, function(el) {
        el.style.display = "block";
    });
}, "jsonp");
       
*/

function miraIp () {
    if (window.location.href.indexOf("world-wide-distributors") != -1) {
    var requestOptions = {
      method: 'GET',
    };
    
    fetch("https://api.geoapify.com/v1/ipinfo?&apiKey=0fe53ab6d0f34a2680cff25d728de166", requestOptions)
      .then(response => response.json())
      .then(result => {console.log(result.country.iso_code);
          var elements = document.getElementsByClassName(result.country.iso_code);
        Array.prototype.forEach.call(elements, function(el) {
            el.style.display = "block";
        });
      })
      .catch(error => console.log('error', error));
        }
}
miraIp();

/*
function dLayer () {
    if (window.location.href.indexOf("/shop/product/") != -1) {
        var name = document.querySelector('[itemprop="name"]').textContent;
        var price = document.querySelector('[itemprop="price"]').textContent;
        var sku = document.querySelector('[itemprop="sku"]').textContent;
        var brand = "Industrial Shields ®";
        
        console.log(name+price+sku+brand);
        
        dataLayer.push({ ecommerce: null });
        dataLayer.push({
          'ecommerce': {
            'currencyCode': 'EUR',
            'impressions': [
             {
               'name': name, 
               'id': sku,
               'price': price,
               'brand': brand
             }]
          }
        });
    }
    
    if (window.location.href.indexOf("/shop/category/") != -1) {
        var brand = "Industrial Shields ®";
        let impressions = [];
        var category = document.querySelector('.right-title').textContent;
        category = category.trim();
        category = category.replace(/\n/g, '');
        var divs = document.querySelectorAll('.pwp-info');
        
        for (var i = 0; i < divs.length; i++) {
             var name = divs[i].querySelector('[itemprop="name"]').textContent;
             var price = divs[i].querySelector('[itemprop="price"]').textContent;
             var position = i+1;
             obj = {'name':name, 'price':price, 'brand':brand, 'category':category, 'position':position};
             impressions.push(obj); 
        }
        
        console.log(impressions);
        
        dataLayer.push({ ecommerce: null });
        dataLayer.push({
          'ecommerce': {
            'currencyCode': 'EUR',
            'impressions':impressions
          }
        });
    }
}
dLayer();
*/

