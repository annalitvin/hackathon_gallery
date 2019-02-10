$(document).ready(function(){

    var emotion_variable = [
        '&#128528;',
        '&#128530;',
        '&#128522;',
        '&#128544;',
        '&#128549;',
        '&#128555;',
        '&#128560;',
    ];
    

	request_page_update ();
	
	function request_page_update () {
		$.ajax({
			url: "/photo_lists/update_main_page",
			type: "get",
			success: renderPhotosList
		});		
	}
	
	function renderPhotosList (data) {
		insert_block(data);
		setTimeout(request_page_update, 5000);
		
	}

    function insert_block(data) {
		if (Object.keys(data).length > 0) {
			out_code = "";
			menu = "<nav class='menu-nav'>" +
			       "<div class='menu-nav__item'>" +
			       "<a href='' class='nav-menu__link'>#INT20H</a></div>";

            count = 0
			for (var emotion in data) {

				out_code += "<div class='list-news__blocks' > ";
				out_code += "<h2 class='emotion__title' id='" + emotion + "'>" + emotion + "</h2>";
				for (var photo in data[emotion]) {
				    out_code += "<div class='news-blok'>";
				    out_code += "<div class='news-blok-main-image__row'>";
				    out_code += " <img src='" + data[emotion][photo] + "' class='news-blok-main-image-news'></div>";
				    out_code += "  <div class='list-news-category__links'>";
				    out_code += "<a href='" + data[emotion][photo] +
				                "' class='list-news-category__link' target='_blank'>View Photo</a></div>";
				    out_code += "</div>";
				}
				out_code += "</div> ";

                smile = emotion_variable[count];
                count++;

				 menu += "<div class='menu-nav__item'>";
				 menu += "<a href='#" +  emotion + "' class='nav-menu__link'>" + smile + emotion + "</a>";
				 menu += "</div>";
			}
            menu += "</nav>";
			
			$("#photo_list_block").empty();
	        $(out_code).appendTo("#photo_list_block");

	        $(".menu-header").empty();
	        $(menu).appendTo(".menu-header");
			
		} else {
			$("<div class='list-news__blocks'><h2>No Photos...</h2></div>").appendTo("#photo_list_block");
		}
	}	

});