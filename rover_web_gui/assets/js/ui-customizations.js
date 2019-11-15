;(function($){
    $.AdminLTE.expandableInfoBox = {
        selector: '[data-widget="collapse-detail"]',
        icons: $.AdminLTE.options.boxWidgetOptions.boxWidgetIcons,
        animationSpeed: $.AdminLTE.options.animationSpeed,
        activate: function(_box) {
            var _this = this;
            if (!_box) {
              _box = document; // activate all boxes per default
            }
            //Listen for collapse event triggers
            $(_box).on('click', _this.selector, function (e) {
              e.preventDefault();
              _this.collapse($(this));
            });
        },
        collapse: function (element) {
          var _this = this;
          //Find the box parent
          var box = element.parents(".info-box").first();
          //Find the body and the footer
          var box_content = box.find(".info-box-detail:first");
          if (!box.hasClass("collapsed-box")) {
            //Convert minus into plus
            element.children(":first")
              .removeClass(_this.icons.collapse)
              .addClass(_this.icons.open);
            //Hide the content
            box_content.slideUp(_this.animationSpeed, function () {
              box.addClass("collapsed-box");
            });
          } else {
            //Convert plus into minus
            element.children(":first")
              .removeClass(_this.icons.open)
              .addClass(_this.icons.collapse);
            //Show the content
            box_content.slideDown(_this.animationSpeed, function () {
              box.removeClass("collapsed-box");
            });
          }
        }
    }
    
}(jQuery));

$.AdminLTE.expandableInfoBox.activate();

$.fn.extend({
    animateCss: function (animationName) {
        var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
        $(this).addClass('animated ' + animationName).one(animationEnd, function() {
            $(this).removeClass('animated ' + animationName);
        });
    }
});

jQuery(".toggle-btn").click(function () { 
    $(this).toggleClass("disabled");
    
});  

