var factor = 0.12;

function previewSpaceHandler(event) {
  var model = $(event.target);
  var id = model.attr("name");
  var first = id.indexOf(".");
  var second = id.indexOf(".", first + 1);
  var field = id.substring(first + 1, second)
  var type = id.substring(second + 1);
  
  var v = getVal(model);
  if (v == undefined && model.data("inherit") != undefined) {
    v = getVal($(":input[name='pdf." + field + "." + model.data("inherit") + "']"));
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
  case "font-size":
    cls = field;
    isLength = true;
    break;
  case "line-height":
    cls = field;
    isLength = true;
    break;
  case "text-align":
    cls = field;
    switch (v) {
    case "start":
      v = "left";
      break;
    case "end":
      v = "right";
      break;
    }
    break;
  case "icon":
//    type = "icon";
    cls = "display";
    v = (v == "icon") ? "table-cell" : "none";
    break;
  case "link-page-number":
//    type = "link-page-number";
    cls = "display";
    v = (v == "true") ? "inline" : "none";
    break;
  case "link-url":
//    type = "link-url";
    cls = "display";
    v = (v == "true") ? "inline" : "none";
    break;
  default:
    var all = $("[data-field='" + field + "'][data-style='" + type + "']");
    if (all.length) {
      var all = $("[data-field='" + field + "'][data-style='" + type + "']");
      all.hide();
      all.filter("[data-value='" + v + "']").show();
    } else {
      cls = field;
    }
    break;
  }
  if (cls != undefined) {
    if (isLength) {
      if (v == undefined) { // support undefined values
        return true;
      }
      v= toPt(v);
      var f = 0.9;
      v = String(v * f) + "px";
    }
    $("*[class~='example-page-content-" + type + "']").css(cls, v);
  }
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
  
  var blockWidth = 700;
  var factor = blockWidth / dim.pageWidth;

  var content = page.find(".example-page-content");
  content.css("margin-right", (dim.marginOutside * factor) + "px");
  content.css("margin-left", (dim.marginInside * factor) + "px");
}

/**
 * Page dimensions in points.
 */
function Dimensions() {
    var pageWidth;
    var pageHeight;
    var marginTop;
    var marginOutside;
    var marginBottom;
    var marginInside
}

/**
 * Return page dimensions in points.
 */
function readPageDimensions() {
  var res = new Dimensions();
  
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

function titleNumberingHandler(event) {
  var target = $(event.target);
  var preview = $("*[id='pdf.title-numbering.example']");
  preview.children().hide();
  $("*[id='pdf.title-numbering.example." + target.val() + "']").show();
}

function tableAndFigureNumberingHandler(event) {
    var target = $(event.target);
    var preview = $("*[id='" + target.attr("name") + ".example']");
    if (target.val() == "none") {
        preview.hide();
    } else {
        preview.show();
    }
}

$(document).ready(function() {
    $(":input[name='pdf.title-numbering']").change(titleNumberingHandler).change();
    $(":input[name='pdf.table-numbering']," +
      ":input[name='pdf.figure-numbering']").change(tableAndFigureNumberingHandler).change();
    $(":input[name='pdf.dl']").change(definitionListHandler).change();
    $(":input[name='pdf.mirror-page-margins']").change(mirrorPageHandler).change();
  $(":input[name='pdf.task-label']").change(taskLabelHandler).change();
    $(":input[name='pdf.force-page-count']").change(forcePageCountChangeHandler).change();
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

/**
 * Convert length value to millimetres.
 * 
 * @param val length with CSS unit
 * @return Number
 */
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

/**
 * Convert length value to points.
 * 
 * @param val length with CSS unit
 * @return Number
 */
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