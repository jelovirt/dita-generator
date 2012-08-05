var factor = 0.12;

function linkStyleHandler(event) {
	var target = $(event.target);
	var link = $("*[id='pdf.link-style.example']");
	switch (target.attr("name")) {
	case "pdf.link-font-weight":
		link.css("font-weight", target.attr("checked") ? "bold" : "normal");
		break;
	case "pdf.link-font-style":
		link.css("font-style", target.attr("checked") ? "italic" : "normal");
		break;
	case "pdf.link-text-decoration":
		link.css("text-decoration", target.attr("checked") ? "underline" : "none");
		break;
	case "pdf.link-color":
	case "pdf.link-color.other":
		if ($(":input[name='pdf.link-color']").val() == "#other") {
			link.css("color", $(":input[name='pdf.link-color.other']").val());
		} else {
			link.css("color", $(":input[name='pdf.link-color']").val());
		}
		break;
	}
}

function previewSpaceHandler(event) {
	var model = $(event.target);
	var id = model.attr("name");
	var first = id.indexOf(".");
	var second = id.indexOf(".", first + 1);
	var field = id.substring(first + 1, second)
	var type = id.substring(second + 1);
	
	var v = getVal(model);
	if (v == undefined && model.hasClass("inherit-from-body")) {
		v = getVal($(":input[name='pdf." + field + ".body']"));
	}
	
	var isLength = false;
	var cls;
	switch (field) {
	case "space-before":
		cls = "margin-top";
		isLength = true;
		break;
	case "space-after":
		cls = "margin-bottom";
		isLength = true;
		break;
	case "start-indent":
		cls = "margin-left";
		isLength = true;
		break;
	case "font-weight":
		cls = "font-weight";
		break;
	case "font-family":
		cls = "font-family";
		break;
	case "font-style":
		cls = "font-style";
		break;
	case "text-decoration":
		cls = "text-decoration";
		break;
	case "color":
		cls = "color";
		break;
	case "font-size":
		cls = "font-size";
		isLength = true;
		break;
	case "text-align":
		cls = "text-align";
		switch (v) {
		case "start":
			v = "left";
			break;
		case "end":
			v = "right";
			break;
		}
		break;
	default:
		cls = field;
		break;
	}
	//$("#pdf-style-selector option").each(function() {
	//	var type = $(this).attr("value");
//		var model = $(":input[name='" + id + "." + type + "']");
		if (isLength) {
			if (v == undefined) { // support undefined values
				return true;
			}
			v= toPt(v);
			var f = 0.9;
			v = String(v * f) + "px";
		}
		//console.info("css " + type + " = " + cls + ":" + v);
		$("*[class~='example-page-content-" + type + "']").css(cls, v);
	//});
}

function pageMarginHandler(event) {
	$(".example-page").each(function() { updatePageExample($(this)); });
	$(".example-block-page").each(function() { updateFixedPageExample($(this)); });
}

/**
 * For pages with fixed factor
 */
function updatePageExample(page) {
	var isOdd = page.is(".odd");
	var dim = readPageDimensions();
	
//	var pageSize = $(":input[name='pdf.page-size']").val().split(' ');
//	var pageWidth, pageHeight;
//	if ($(":input[name='pdf.orientation']").val() == "landscape") {
//		pageWidth = toPt(pageSize[1]);
//		pageHeight = toPt(pageSize[0]);
//	} else {
//		pageWidth = toPt(pageSize[0]);
//		pageHeight = toPt(pageSize[1]);	
//	}
//	
//	var marginTopTarget = $(":input[name='pdf.page-margin-top']");
//	var marginOutsideTarget = $(":input[name='pdf.page-margin-outside']");
//	var marginBottomTarget = $(":input[name='pdf.page-margin-bottom']");
//	var marginInsideTarget = $(":input[name='pdf.page-margin-inside']");
//	
//	var marginTop = toPt(getVal(marginTopTarget));
//	var marginOutside = toPt(getVal(marginOutsideTarget));
//	var marginBottom = toPt(getVal(marginBottomTarget));
//	var marginInside = toPt(getVal(marginInsideTarget));
	
	page.height(dim.pageHeight * factor);
	page.width(dim.pageWidth * factor);
	
	var content = page.find(".example-page-body");
	content.css("margin-top", (dim.marginTop * factor) + "px");
	content.css(isOdd ? "margin-right" : "margin-left", (dim.marginOutside * factor) + "px");
	content.css("margin-bottom", (dim.marginBottom * factor) + "px");
	content.css(isOdd ? "margin-left" : "margin-right", (dim.marginInside * factor) + "px");
	content.height((dim.pageHeight - dim.marginTop - dim.marginBottom) * factor);
	content.width((dim.pageWidth - dim.marginInside - dim.marginOutside) * factor);
	
	var columns = new Number($(":input[name='pdf.body-column-count']").val());
	var columnWidth = toPt(getVal($(":input[name='pdf.column-gap']")))
	var tr = page.find(".example-page-body tr");
	var buf = $("<tr></tr>");
	for (var i = 0; i < columns; i++) {
		if (i != 0) {
			buf.append($("<td class='gap'><span/></td>").width(columnWidth * factor));
		}
		buf.append($("<td><div/></td>"));
	}
	tr.replaceWith(buf);
}
/**
 * For pages with fixed width
 */
function updateFixedPageExample(page) {
	var dim = readPageDimensions();
	
	var blockWidth = 700; //page.parents(".example-block:first").outerWidth();
	var factor = blockWidth / dim.pageWidth;

	//page.height(dim.pageHeight * factor);
	//page.width(dim.pageWidth * factor);
	
	var content = page.find(".example-page-content");
	//content.css("margin-top", (dim.marginTop * factor) + "px");
	content.css("margin-right", (dim.marginOutside * factor) + "px");
	//content.css("margin-bottom", (dim.marginBottom * factor) + "px");
	content.css("margin-left", (dim.marginInside * factor) + "px");
	//content.height((dim.pageHeight - dim.marginTop - dim.marginBottom) * factor);
	//content.width((dim.pageWidth - dim.marginInside - dim.marginOutside) * factor);
}

/**
 * Return page dimensions in points.
 * 
 * @returns {___anonymous8727_8728}
 */
function readPageDimensions() {
	var res = {};
	
	var pageSize = $(":input[name='pdf.page-size']").val().split(' ');
	if ($(":input[name='pdf.orientation']").val() == "landscape") {
		res.pageWidth = toPt(pageSize[1]);
		res.pageHeight = toPt(pageSize[0]);
	} else {
		res.pageWidth = toPt(pageSize[0]);
		res.pageHeight = toPt(pageSize[1]);	
	}
	res.marginTop = toPt(getVal($(":input[name='pdf.page-margin-top']")));
	res.marginOutside = toPt(getVal($(":input[name='pdf.page-margin-outside']")));
	res.marginBottom = toPt(getVal($(":input[name='pdf.page-margin-bottom']")));
	res.marginInside = toPt(getVal($(":input[name='pdf.page-margin-inside']")));
	
	return res;
}

function forcePageCountChangeHandler(event) {
	var target = $(event.target);
	$(".pdf_force-page-count_example_auto, .pdf_force-page-count_example_odd, .pdf_force-page-count_example_even").each(function () {
		var t = $(this);
		if (t.is(".pdf_force-page-count_example_" + target.val())) {
			t.show();
		} else {
			t.hide();
		}
	});
}

function taskLabelHandler(event) {
	var target = $(event.target);
	var e = $(".example-task-label");
	if (target.is(":checked")) {
		e.show();
	} else {
		e.hide();
	}
}

/** @deprecated */
function spacingHandler(event, cls) {
	var target = $(event.target);
	var val = toPt(getVal(target));
	if (val == undefined) {
		setError(target, $("<span>Invalid value</span>"), "Invalid XSL FO length value");
	} else {
		setOk(target);
	}
	var f = 0.3;
	var v = String(val * f) + "px";
	$(".example-page-content-body, .example-page-content-topic, .example-page-content-topic.topic").css(cls, v);
}

function mirrorPageHandler(event) {
	var target = $(event.target);
	var evenPage = $(".even");
	if (target.prop("checked")) {
		evenPage.show();
	} else {
		evenPage.hide();
	}
	pageMarginHandler(event);
}


function definitionListHandler(event) {
	var target = $(event.target);
	$("*[id='pdf.dl.example.html'], *[id='pdf.dl.example.list'], *[id='pdf.dl.example.table']").hide();
	$("*[id='pdf.dl.example." + target.val() + "']").show();
}

function linkPageNumberHandler(event) {
	var target = $(event.target);
	var view = $(".link-page-number-example");
	if (target.is(":checked")) {
		view.show();
	} else {
		view.hide();
	}
}

function titleNumberingHandler(event) {
	var target = $(event.target);
	var preview = $("*[id='pdf.title-numbering.example']");
	preview.children().hide();
	$("*[id='pdf.title-numbering.example." + target.val() + "']").show();
}

$(document).ready(function() {
    $(":input[name='pdf.link-page-number']").change(linkPageNumberHandler).change();
    $(":input[name='pdf.title-numbering']").change(titleNumberingHandler).change();
    $(":input[name='pdf.dl']").change(definitionListHandler).change();
    $(":input[name='pdf.mirror-page-margins']").change(mirrorPageHandler).change();
	$(":input[name='pdf.task-label']").change(taskLabelHandler).change();
    $(":input[name='pdf.force-page-count']").change(forcePageCountChangeHandler).change();
    $(":input[name='pdf.link-font-weight']," +
      ":input[name='pdf.link-font-style']," +
      ":input[name='pdf.link-text-decoration']," +
      ":input[name='pdf.link-color']").change(linkStyleHandler).change();
	$("#style-model :input").change(previewSpaceHandler).change();
	$(":input[name='pdf.page-size']," +
      ":input[name='pdf.orientation']," +
      ":input[name='pdf.page-margin-top']," +
      ":input[name='pdf.page-margin-bottom']," +
      ":input[name='pdf.page-margin-inside']," +
      ":input[name='pdf.page-margin-outside']," +
      ":input[name='pdf.body-column-count']," + 
      ":input[name='pdf.column-gap']").change(pageMarginHandler).first().change();
});

// Utilities -------------------------------------------------------------------

function validateDistance(event) {
	var target = $(event.target);
}

function getVal(input) {
	return input.val() != "" ? input.val() : input.attr("placeholder");
}

function stripUnit(val) {
	return new Number(val.substring(0, val.length - 2));
}

function toMm(val) {
	if (val == undefined) {
		return undefined;
	}
    var unit = val.substring(val.length - 2);
    var value = stripUnit(val);
    if (unit == "cm") {
        return value * 10;
    } else if (unit == "in") {
        return value * 25.4;
    } else if (unit == "pt" || unit == "px") {
        return value * 25.4 / 72;
    } else if (unit == "pc") {
        return value * 25.4 / 72 * 12;
    } else if (unit == "mm") {
        return value;
    } else {
    	return undefined;
    }
}

function toPt(val) {
	if (val == undefined) {
		return undefined;
	}
    var unit = val.substring(val.length - 2);
    var value = val.substring(0, val.length - 2);
    if (unit == "cm") {
        return value / 2.54 * 72;
    } else if (unit == "mm") {
        return value / 25.4 * 72;
    } else if (unit == "in") {
        return value * 72;
    } else if (unit == "pc") {
        return value * 12;
    } else if (unit == "em") {
    	var val = $(":input[name='pdf.font-size.body']").val();
    	return val.substring(0, val.length - 2) * value;  
    } else if (unit == "pt") {
        return value;
    } else {
    	return undefined;
    }
}

// preview page drawing
/*
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
*/