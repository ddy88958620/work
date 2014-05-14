(function($){
	$.extend({
		picShow:function(picBox,actives){      
			var auto = false;
			var str = '';
			var speed = 500;
			var width = 800;
			var number = $(picBox+' li').length;
			var numWidth = number * 18;
			var _left = (width - numWidth) / 2;
			active = actives ? actives : 0;
			$(picBox+' ul').width(width * number);
			$(picBox+' li').each(function(i) {
				str += '<span></span>'
			});
			$(picBox+' .number').width(numWidth).html(str);
			$(picBox+' .number').css('left', _left);
			$(picBox+' .number span:first').addClass('on');
			function cur(ele, currentClass) {
				ele = $(ele) ? $(ele) : ele;
				ele.addClass(currentClass).siblings().removeClass(currentClass)
			}
			$(picBox+' .next').click(function() {
				slide(1)
			});
			$(picBox+' .prev').click(function() {
				slide( - 1)
			});
			function slide(j) {
				if ($(picBox+' ul').is(':animated') == false) {
					active += j;
					if (active != -1 && active != number) {
						$(picBox+' ul').animate({
							'marginLeft': -active * width + 'px'
						},
						speed)
					} else if (active == -1) {
						active = number - 1;
						$(picBox+' ul').css({
							"marginLeft": -(width * (active - 1)) + "px"
						});
						$(picBox+' ul').animate({
							"marginLeft": -(width * active) + "px"
						},
						speed)
					} else if (active == number) {
						active = 0;
						$(picBox+' ul').css({
							"marginLeft": -width + "px"
						});
						$(picBox+' ul').animate({
							"marginLeft": 0 + "px"
						},
						speed)
					}
					cur($(picBox+' .number span').eq(active), 'on')
				}
			};
			$(picBox+' .number span').click(function() {
				active = $(this).index();
				fade(active);
				cur($(picBox+' .number span').eq(active), 'on')
			});
			function fade(i) {
				if ($(picBox+' ul').css('marginLeft') != -i * width + 'px') {
					$(picBox+' ul').animate({'marginLeft': -i * width + 'px'},speed);
					/*$(picBox+' ul').fadeOut(0,
					function() {
						$(picBox+' ul').fadeIn(500)
					})*/
				}
			}
			fade(active);
			cur($(picBox+' .number span').eq(active), 'on');
			function start() {
				auto = setInterval(function() {
					fade(1)
				},
				5000)
			}
			function stopt() {
				if (auto) clearInterval(auto)
			}
			$(picBox).hover(function() {
				stopt()
			},
			function() {
				start()
			});
			//start()
		}
	});
	//////////tab切换
	$.extend({
		msclick:function(box,header,content,visited){                         
			$(box).find(header).each(function(index){
				$(this).attr("headerindex",index+"h")

				$(box).find(header).click(function(){
				var headers  = parseInt($(this).attr("headerindex"))
				$(this).addClass(visited).siblings(header).removeClass(visited)					
				$(box).find(content).eq(headers).stop(true,true).slideDown(0).siblings(content).slideUp(0)
				})
			});
		}
	})
})(jQuery);