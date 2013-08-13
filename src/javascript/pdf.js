function toolkitVersionChangeHandler(event) {
	toggleByClass($(event.target), "v");
}

function formatterHandler(event) {
    toggleByClass($(event.target), "f");
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

$(document).ready(function() {
	// widget initialization
	$(":input.editable-list").each(function() {
		var s = $(this);
		var id = s.attr("name") != undefined ? s.attr("name") : s.attr("id");
		var l = $(":input[id='" + id + ".list']");
		var o = $(":input[id='" + id + ".other']");
		s.change(editableHandler);
		o.change(function(event){editableOtherHandler(s, l, o);});
		l.change(function(event){editableListHandler(s, l, o);});
	});
	
	// form initialization
	$(":input[name='ot.version']").change(toolkitVersionChangeHandler).change();
    $(":input[name='pdf.formatter']").change(formatterHandler).change();
    $(":input[name='transtype']").change(transtypeChangeHandler);
    $(":input[name='pdf.body-column-count']").change(columnChangeHandler).change();
  $.each(storeFields, function(f) {
    $(":input[id='pdf." + this + "']").change(styleEditorHandler);
  });
  $("#pdf-style-selector").change(styleHandler);
  readFromModel("body");// initialize style dialog
  pdfStyleSelectorCurrent = "body";
  $("#pdf-style-selector").change();
	$(":input.length-value").keydown(valueChangeHandler).change(validateLength);
});

// UI --------------------------------------------------------------------------

function validateLength(event) {
	var target = $(event.target);
	var val = toPt(getVal(target));
	if (val == undefined) {
		setError(target, $("<span>Invalid value</span>"), "Invalid XSL FO length value");
	} else {
		setOk(target);
	}
}

var pdfStyleSelectorCurrent;

// Column methods

function columnChangeHandler(event) {
	var target = $(event.target);
	if (target.val() == 1) {
		$(":input[name='pdf.column-gap']").prop("disable", true).parent().hide();
	} else {
		$(":input[name='pdf.column-gap']").prop("disable", false).parent().show();
	}
}

// Editable list methods

function editableHandler(event) {
	var target = $(event.target);
	var id = target.attr("name") != undefined ? target.attr("name") : target.attr("id");
	var list = $(":input[id='" + id + ".list" + "']");
	var other = $(":input[id='" + id + ".other" + "']");
	other.val(target.val());
	if (list.find("option[value='" + other.val() + "']").length != 0) { // same value in list
		other.hide().prop("disabled", true);
		list.val(other.val());
		other.val(undefined);
	} else {
		list.val("#other");
		other.show().prop("disabled", false).focus();
	}
}
function editableListHandler(store, list, other) {
	if (list.val() == "#other") {
		store.val(other.val()).change();
	} else {
		store.val(list.val()).change();
	}

}
function editableOtherHandler(store, list, other) {
	store.val(other.val()).change();
}

// Value increment/decrement methods

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

// Style dialog methods

/**
 * Change which style to edit
 * @param event UI change event
 */
function styleHandler(event) {
	var target = $(event.target);
	var style = target.val();
	$("#style-form [data-style]").each(function() {
	  var f = $(this); 
	  f.toggle($(this).attr("data-style").split(" ").indexOf(style) !== -1);
	});
	var type = target.find(":selected").parent("optgroup.block");
	if (type.length == 0) {
		$(".pdf-style-selector-block").hide().find(":input").attr("disabled", true);
	} else {
		$(".pdf-style-selector-block").show().find(":input").removeAttr("disabled");
	}
	pdfStyleSelectorCurrent = target.val();
	readFromModel(target.val());
}
var storeFields = ["font-family", "font-size", "font-weight", "font-style", "color", "background-color", "space-before", "space-after", "start-indent", "text-align", "text-decoration", "line-height",
				   // titles
				   "title-numbering",
                   // note
                   "icon",
                   // link
                   "link-page-number", "link-url",
                   //
                   "dl-type",
                   // table, fig
                   "caption-number"];
/**
 * Read fields from model to UI.
 * @param type
 */
function readFromModel(type) {
	for (var i = 0; i < storeFields.length; i++) {
		var model = $("#style-model :input[name='pdf." + storeFields[i] + "." + type + "']");
		// if no value, inherit from body
		if (model.data("inherit") != undefined && (model.val() == undefined || model.val() == "")) {
			model = $("#style-model :input[name='pdf." + storeFields[i] + "." + "body" + "']");
		}
		var view = $("#style-form :input[id='pdf." + storeFields[i] + "']");
		if (view.is(":checkbox")) {
			view.prop("checked", model.val() == view.val());
		} else if (view.is(".editable-list")) {
			var id = view.attr("name") != undefined ? ui.attr("name") : view.attr("id");
			var store = $("#style-model :input[id='" + id + "']");
		    store.val(model.val());
		    store.change();		    
		} else {
			view.val(model.val());
		}
	}
}
function writeToModel(type) {
	for (var i = 0; i < storeFields.length; i++) {
		writeFieldToModel(storeFields[i], type);
	}
}
function writeFieldToModel(field, type) {
	var view = $("#style-form :input[id='pdf." + field + "']");
	var model = $("#style-model :input[name='pdf." + field + "." + type + "']");
	var oldValue = model.val();
	var newValue;
	if (view.is(":checkbox")) {
		if (view.is(":checked")) {
			newValue = view.val();
		} else if (field == "text-decoration") {
			newValue = "none";
		} else {
			newValue = "normal";
		}
	} else if (view.is(".editable-list")) {
		newValue = view.val();
	} else {
		newValue = view.val();
	}
	
	// if equals body value, treat as inherit value
	if (model.data("inherit") != undefined) {
		var b = $("#style-model :input[name='pdf." + field + "." + "body" + "']");
		if (oldValue == b.val()) {
			newValue = undefined;
		}
    // update inheriting model fields
	} else if (type == "body") {
	  $("#style-model :input[data-inherit=body]").each(function() {
			var m = $(this);
			if (m.is("[name^='pdf." + field + "']")) {
				if (m.val() == undefined || m.val() == "" || m.val() == oldValue) {
					m.val(newValue);
					m.change();
				}
			}
		});
	}

	model.val(newValue);
	// fire change event
	model.change();
}
/**
 * Update store when UI changes
 * @param event UI change event
 */
function styleEditorHandler(event) {
	var ui = $(event.target);
	var field = ui.attr("id").split(".")[1];
	writeFieldToModel(field, pdfStyleSelectorCurrent);
}
