var factor = 0.12;

function toolkitVersionChangeHandler(event) {
	toggleByClass($(event.target), "v");
}

function formatterHandler(event) {
    toggleByClass($(event.target), "f");
//    var val = p.val();
//    p.find("option").each(function() {
//        var s = $(this).attr("value");
//        var c = ".v" + s.replace(/\./g, "_");
//        $(c).addClass("disabled").find(":input").attr("disabled", true);
//    });
//    p.find("option").each(function() {
//        var s = $(this).attr("value");
//        var c = ".v" + s.replace(/\./g, "_");
//        if (val == s) {
//            $(c).removeClass("disabled").find(":input").removeAttr("disabled");
//        }
//    });
}

function toggleByClass(p, prefix) {
	var val = p.val();
    p.find("option").each(function() {
        var s = $(this).attr("value");
        var c = "." + prefix + s.replace(/\./g, "_");
        $(c).addClass("disabled").find(":input").attr("disabled", true);
    });
    p.find("option").each(function() {
        var s = $(this).attr("value");
        var c = "." + prefix + s.replace(/\./g, "_");
        if (val == s) {
            $(c).removeClass("disabled").find(":input").removeAttr("disabled");
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

function otherChangeHandler(event) {
	var target = $(event.target);
	var other = $(":input[name='" + target.attr("name") + ".other']");
	if (target.val() == "#other") {
		other.show().prop("disabled", false).focus();
	} else {
		other.hide().prop("disabled", true);
	}
}

function columnChangeHandler(event) {
	var target = $(event.target);
	if (target.val() == 1) {
		$(":input[name='pdf.column-gap']").prop("disable", true).parent().hide();
	} else {
		$(":input[name='pdf.column-gap']").prop("disable", false).parent().show();
	}
}

$(document).ready(function() {
    $(":input[name='ot.version']").change(toolkitVersionChangeHandler).change();
    $(":input[name='pdf.formatter']").change(formatterHandler).change();
    $(":input[name='transtype']").change(transtypeChangeHandler);
    
    $(":input[name='pdf.force-page-count']").change(forcePageCountChangeHandler).change();
//    $(":input[name='pdf.chapter-layout']").change(forcePageCountChangeHandler).change();
    
    $("option[value='#other']").parent().change(otherChangeHandler).change();
    $(":input[name='pdf.body-column-count']").change(columnChangeHandler).change();
    $(":input[name='pdf.side-col-width']").change(sideColWidthHandler).change();
    $(":input[name='pdf.text-align']").change(textAlignHandler).change();
    $(":input[name='pdf.link-font-weight']," +
      ":input[name='pdf.link-font-style']," +
      ":input[name='pdf.link-text-decoration']," +
      ":input[name='pdf.link-color']," +
      ":input[name='pdf.link-color.other']").change(linkStyleHandler).change();
    $(":input[name='pdf.page-size']," +
      ":input[name='pdf.orientation']," +
      ":input[name='pdf.page-margin-top']," +
      ":input[name='pdf.page-margin-right']," +
      ":input[name='pdf.page-margin-bottom']," +
      ":input[name='pdf.page-margin-left']," +
      ":input[name='pdf.page-margin-inside']," +
      ":input[name='pdf.page-margin-outside']," +
      ":input[name='pdf.body-column-count']," + 
      ":input[name='pdf.column-gap']").change(pageMarginHandler).first().change();
    $(":input[name='pdf.spacing.before']," +
      ":input[name='pdf.spacing.after']").change(function (event) { spacingHandler(event, "margin-top") } ).first().change();
    $(":input.length-value").keydown(valueChangeHandler);
    $(":input[name='pdf.mirror-page-margins']").change(mirrorPageHandler).change();
    $(":input[name='pdf.dl']").change(definitionListHandler).change();
    $(":input[name='pdf.title-numbering']").change(titleNumberingHandler).change();
    $(":input[name='pdf.link-page-number']").change(linkPageNumberHandler).change();
});

// UI --------------------------------------------------------------------------

function titleNumberingHandler(event) {
	var target = $(event.target);
	var preview = $("*[id='pdf.title-numbering.example']");
	preview.children().hide();
	$("*[id='pdf.title-numbering.example." + target.val() + "']").show();
}

function valueChangeHandler(event) {
	switch (event.keyCode) {
	case 38:
		var t = $(event.target);
		addToValue(t, 1);
		event.preventDefault();
		event.stopPropagation();
		t.change();
		return false;
	case 40:
		var t = $(event.target);
		addToValue(t, -1);
		event.preventDefault();
		event.stopPropagation();
		t.change();
		return false;
	}
}

function addToValue(target, add) {
	var val = target.val();
	if (val == "") {
		val = target.attr("placeholder");
	}
	var num = new Number(val.substring(0, val.length - 2));
	var unit = val.substring(val.length - 2);
	target.val((num + add).toString() + unit);
}

// Preview ---------------------------------------------------------------------

function linkPageNumberHandler(event) {
	var target = $(event.target);
	var e = $("*[id='pdf.link-page-number.example']");
	if (target.is(":checked")) {
		e.show();
	} else {
		e.hide();
	}
}

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
	$(".example-page-content-para, .example-page-content-title").css(cls, v);
}

function mirrorPageHandler(event) {
	var target = $(event.target);
	var evenPage = $("*[id='pdf.margin.example'] .even");
	if (target.prop("checked")) {
		evenPage.show();
	} else {
		evenPage.hide();
	}
	pageMarginHandler(event);
}

//function pageHandler(event) {
//	//*[id='pdf.page.example'] .example-page, 
//	$("*[id='pdf.margin.example'] .example-page").each(function() { updatePageExample($(this)); });
//}

function pageMarginHandler(event) {
	//*[id='pdf.margin.example'] .example-page, *[id='pdf.margin.example']  
	$(".example-page").each(function() { updatePageExample($(this)); });
}

/** Get page factor. */
//function getFactor(page, pageWidth) {
//	var example = page.parents(".example:first");
//	return (Number(example.width()) / example.find(".example-page").size() - 10) / pageWidth;
//}

function updatePageExample(page) {
	var isOdd = page.is(".odd");
	var pageSize = $(":input[name='pdf.page-size']").val().split(' ');
	var pageWidth, pageHeight;
	if ($(":input[name='pdf.orientation']").val() == "landscape") {
		pageWidth = toPt(pageSize[1]);
		pageHeight = toPt(pageSize[0]);
	} else {
		pageWidth = toPt(pageSize[0]);
		pageHeight = toPt(pageSize[1]);	
	}
	
	var marginTopTarget = $(":input[name='pdf.page-margin-top']");
	var marginOutsideTarget = $(":input[name='pdf.page-margin-outside']");
	var marginBottomTarget = $(":input[name='pdf.page-margin-bottom']");
	var marginInsideTarget = $(":input[name='pdf.page-margin-inside']");
	
	var marginTop = toPt(getVal(marginTopTarget));
	if (marginTop == undefined) {
		setError(marginTopTarget, $("<span>Invalid value</span>"), "Invalid XSL FO length value");
	} else {
		setOk(marginTopTarget);
	}
	var marginOutside = toPt(getVal(marginOutsideTarget));
	if (marginOutside == undefined) {
		setError(marginOutsideTarget, $("<span>Invalid value</span>"), "Invalid XSL FO length value");
	} else {
		setOk(marginOutsideTarget);
	}
	var marginBottom = toPt(getVal(marginBottomTarget));
	if (marginBottom == undefined) {
		setError(marginBottomTarget, $("<span>Invalid value</span>"), "Invalid XSL FO length value");
	} else {
		setOk(marginBottomTarget);
	}
	var marginInside = toPt(getVal(marginInsideTarget));
	if (marginInside == undefined) {
		setError(marginInsideTarget, $("<span>Invalid value</span>"), "Invalid XSL FO length value");
	} else {
		setOk(marginInsideTarget);
	}
	
	//var factor = getFactor(page, pageWidth);
	
	page.height(pageHeight * factor);
	page.width(pageWidth * factor);
	
	var content = page.find(".example-page-body");
	content.css("margin-top", (marginTop * factor) + "px");
	content.css(isOdd ? "margin-right" : "margin-left", (marginOutside * factor) + "px");
	content.css("margin-bottom", (marginBottom * factor) + "px");
	content.css(isOdd ? "margin-left" : "margin-right", (marginInside * factor) + "px");
	content.height((pageHeight - marginTop - marginBottom) * factor);
	content.width((pageWidth - marginInside - marginOutside) * factor);
	
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

function definitionListHandler(event) {
	var target = $(event.target);
	$("*[id='pdf.dl.example.html'], *[id='pdf.dl.example.list'], *[id='pdf.dl.example.table']").hide();
	$("*[id='pdf.dl.example." + target.val() + "']").show();
}

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

function sideColWidthHandler(event) {
	var page = $("*[id='pdf.side-col-width.example']");
	var pageSize = $(":input[name='pdf.page-size']").val().split(' ');
	var pageWidth, pageHeight;
	if ($(":input[name='pdf.orientation']").val() == "landscape") {
		pageWidth = toPt(pageSize[1]);
		pageHeight = toPt(pageSize[0]);
	} else {
		pageWidth = toPt(pageSize[0]);
		pageHeight = toPt(pageSize[1]);	
	}
	var marginOutside = toPt(getVal($(":input[name='pdf.page-margin-outside']")));
	var marginInside = toPt(getVal($(":input[name='pdf.page-margin-inside']")));
	
	var f = 0.3;
	
	page.width(pageWidth * f);
	
	var content = page.find(".example-page-wrapper");
	content.css("margin-left", (marginOutside * f) + "px");
    content.css("margin-right", (marginInside * f) + "px");
	content.width((pageWidth - marginInside - marginOutside) * f);

	var indent = toPt(getVal($(event.target)));
	if (indent == undefined) {
		setError($(event.target), $("<span>Invalid value</span>"), "Invalid XSL FO length value");
	} else {
		setOk($(event.target));
	}
	$(".example-page-content-para").css("margin-left", (indent * f) + "px");
//	var columns = new Number($(":input[name='pdf.body-column-count']").val());
//	var columnWidth = toPt(getVal($(":input[name='pdf.column-gap']")))
//	var tr = page.find(".example-page-body tr");
//	var buf = $("<tr></tr>");
//	for (var i = 0; i < columns; i++) {
//		if (i != 0) {
//			buf.append($("<td class='gap'></td>").width(columnWidth * factor));
//		}
//		buf.append($("<td></td>"));
//	}
//	tr.html(buf.find("td"));
}

function textAlignHandler(event) {
	var target = $(event.target);
	var align = target.val();
	switch (align) {
	case "start":
		align = "left";
		break;
	case "end":
		align = "right";
		break;
	}
	$("*[id='pdf.text-align.example']").css("text-align", align);
}

// Utilities -------------------------------------------------------------------

function validateDistance(event) {
	var target = $(event.target);
}

function getVal(input) {
	return input.val() != "" ? input.val() : input.attr("placeholder");
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
    } else if (unit == "mm") {
        return value;
    } else {
    	return undefined;
    }
}

function toPt(val) {
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
    	var val = $(":input[name='pdf.default-font-size']").val();
    	return val.substring(0, val.length - 2) * value;  
    } else if (unit == "pt") {
        return value;
    } else {
    	return undefined;
    }
}

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