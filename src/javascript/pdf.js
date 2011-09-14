var factor;

function toolkitVersionChangeHandler(event) {
    var p = $(event.target);
    var val = p.val();
    p.find("option").each(function() {
        var s = $(this).attr("value");
        var c = ".v" + s.replace(/\./g, "_");
        if (val == s) {
            $(c).removeClass("disabled").find(":input").removeAttr("disabled");
        } else {
            $(c).addClass("disabled").find(":input").attr("disabled", true);
        }
    });
}

function transtypeChangeHandler(event) {
    var id = $(event.target);
    var val = id.attr("value");
    if (!pluginPatter.test(val)) { //!namePattern.test(val)
        setError(id, $("<span>Not a valid XML name</span>"),
                 "Type ID must be a valid XML name.");
    } else {
        setOk(id);
    }
}

function pageSizeChangeHandler(event) {
    var p = $(event.target);
    var val = p.val();
//    // preview
//    if (val == undefined || val == "") {
//      val = "8.5in 11in";
//    }
//    var tokens = val.split(" ");
//    tokens = $.map(tokens, toMm);
//    var ratio = tokens[1] / tokens[0];
//    factor = page.width() / tokens[0];
//    var page = $(".preview-page");
//    page.innerHeight(page.width() * ratio);
}

function pageMarginChangeHandler(event, side) {
    var p = $(event.target);
    var val = p.val();
//    // preview
//    if (val == undefined || val == "") {
//      val = p.attr("placeholder");
//    }
//    var page = $(".preview-content");
//    page.css("padding-" + side, (toMm(val) * factor) + "px");
}

function forcePageCountChangeHandler(event) {
	drawSequencePreview();
}

function toMm(val) {
  var unit = val.substring(val.length - 2);
  var value = val.substring(0, val.length - 2);
  if (unit == "cm") {
    return value * 10;
  } else if (unit == "in") {
    return value * 25.4;
  } else if (unit == "pt" || unit == "px") {
    return value * 25.4 / 72;
  } else if (unit == "pc") {
    return value * 25.4 / 72 * 12;
  } else {
    return value;
  }
}

function colorChangeHandler(event) {
	var target = $(event.target);
	var other = $(":input[name='" + target.attr("name") + ".other']");
	if (target.val() == "#other") {
		other.show().prop("disabled", false);
	} else {
		other.hide().prop("disabled", true);
	}
}

function linkColorChangeHandler(event) {
	colorChangeHandler(event);
}


$(document).ready(function() {
    $(":input[name='ot.version']").change(toolkitVersionChangeHandler).change();
    $(":input[name='transtype']").change(transtypeChangeHandler);
    
//    $(":input[name='pdf.page-size']").change(pageSizeChangeHandler).change();
//    $(":input[name='pdf.page-margin-top']").change(function(event) { pageMarginChangeHandler(event, "top") }).change();
//    $(":input[name='pdf.page-margin-right']").change(function(event) { pageMarginChangeHandler(event, "right") }).change();
//    $(":input[name='pdf.page-margin-bottom']").change(function(event) { pageMarginChangeHandler(event, "bottom") }).change();
//    $(":input[name='pdf.page-margin-left']").change(function(event) { pageMarginChangeHandler(event, "left") }).change();
//    $(":input[name='pdf.force-page-count']").change(forcePageCountChangeHandler).change();
//    $(":input[name='pdf.chapter-layout']").change(forcePageCountChangeHandler).change();
    
    $(":input[name='pdf.color']").change(colorChangeHandler).change();
    $(":input[name='pdf.link-color']").change(linkColorChangeHandler).change();
});

// preview page drawing

var margins = [5, 5, 5, 5];

function drawSequencePreview() {
	var canvas = document.getElementById("preview.sequence");
    if (canvas != null && canvas.getContext) {
    	var ctx = canvas.getContext("2d");
    	ctx.clearRect(0, 0, canvas.width, canvas.height);
    	var p1 = drawPage(ctx, 2, 1);
    	p1[3] = p1[3] / 2;
    	drawContents(ctx, p1, false);
    	if ($(":input[name='pdf.force-page-count']").val() == "auto") {
        	var p2 = drawPage(ctx, 1, 2);
        	if ($(":input[name='pdf.chapter-layout']").val() == "BASIC") {
            	drawContents(ctx, p2, false);	
        	} else {
            	drawMinitoc(ctx, p2, false);
        	}
        	var p3 = drawPage(ctx, 2, 2);
        	drawContents(ctx, p3, true);
    	} else {
        	var p2 = drawPage(ctx, 1, 2);
        	var p3 = drawPage(ctx, 2, 2);
        	if ($(":input[name='pdf.chapter-layout']").val() == "BASIC") {
            	drawContents(ctx, p3, true);	
        	} else {
            	drawMinitoc(ctx, p3, true);
        	}
    	}
    }
}

function drawPage(ctx, col, row, content) {
	ctx.lineWidth = "1px";
	var height = 297 / 4;
	var width = 210 / 4;
	var x = ((col - 1) * 5) + (width * col) - width;
	var y = ((row - 1) * 5) + (height * row) - height;
	
	ctx.strokeStyle = "black";
	ctx.strokeRect(x, y, width, height);
	
	return {
		x: x + margins[0],
		y: y + margins[1],
	    width: width - margins[0] - margins[2],
	    height: height - margins[1] - margins[3]
	};
}

function drawContents(ctx, c, cont) {
	ctx.lineWidth = "2px";
	var start = cont;
	var offset = 0;
	var lines = 0;
	while (offset < c.height) {
		if (start || Math.random() < 0.1) {
			ctx.strokeStyle = "black";
			offset = offset + 3;
			lines = 0;
			start = false;
		} else {
			ctx.strokeStyle = "silver";
		}
		ctx.beginPath();
		ctx.moveTo(c.x,
				   c.y + offset);
		ctx.lineTo(c.width + c.x - Math.random() * 20,
				   c.y + offset);
		ctx.closePath();
		ctx.stroke();
		offset = offset + 3;
		if (Math.random() > 0.75 && lines > 2) {
			offset = offset + 3;
			lines = 0;
		} else {
			lines++;
		}
	}
}

function drawMinitoc(ctx, c, cont) {
	ctx.lineWidth = "2px";
	ctx.strokeStyle = "black";
	ctx.beginPath();
	ctx.moveTo(c.x,
			   c.y);
	ctx.lineTo(c.x + c.width / 1.5,
			   c.y);
	ctx.closePath();
	ctx.stroke();
	var start = cont;
	var offset = 3;
	var lines = 0;
	while (offset < c.height / 2) {
//		if (start || Math.random() < 0.1) {
//			ctx.strokeStyle = "black";
//			offset = offset + 3;
//			lines = 0;
//			start = false;
//		} else {
			ctx.strokeStyle = "silver";
//		}
		ctx.beginPath();
		ctx.moveTo(c.x,
				   c.y + offset);
		ctx.lineTo(c.width + c.x / 1.5 - Math.random() * 5,
				   c.y + offset);
		ctx.closePath();
		ctx.stroke();
		offset = offset + 3;
		if (Math.random() > 0.75 && lines > 2) {
			offset = offset + 3;
			lines = 0;
		} else {
			lines++;
		}
	}
	ctx.beginPath();
	ctx.moveTo(c.width + c.x / 1.5 + 2,
			   c.y + 3);
	ctx.lineTo(c.width + c.x / 1.5 + 2,
			   c.y + c.height / 2 + 3);
	ctx.closePath();
	ctx.stroke();
}