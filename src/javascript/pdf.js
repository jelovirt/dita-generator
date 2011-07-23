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

$(document).ready(function() {
    $(":input[name='ot.version']").change(toolkitVersionChangeHandler).change();
    $(":input[name='transtype']").change(transtypeChangeHandler);
    $(":input[name='pdf.page-size']").change(pageSizeChangeHandler).change();
    $(":input[name='pdf.page-margin-top']").change(function(event) { pageMarginChangeHandler(event, "top") }).change();
    $(":input[name='pdf.page-margin-right']").change(function(event) { pageMarginChangeHandler(event, "right") }).change();
    $(":input[name='pdf.page-margin-bottom']").change(function(event) { pageMarginChangeHandler(event, "bottom") }).change();
    $(":input[name='pdf.page-margin-left']").change(function(event) { pageMarginChangeHandler(event, "left") }).change();
});