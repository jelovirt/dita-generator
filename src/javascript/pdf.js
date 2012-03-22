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
		editableListHandler(s, l, o);
	});
	
	// form initialization
	$(":input[name='ot.version']").change(toolkitVersionChangeHandler).change();
    $(":input[name='pdf.formatter']").change(formatterHandler).change();
    $(":input[name='transtype']").change(transtypeChangeHandler);
    $(":input[name='pdf.body-column-count']").change(columnChangeHandler).change();
    $("#pdf-style-selector").change(styleHandler);
    readFromStore("body");// initialize style dialog
	$("#pdf-style-selector-current").val("body");
	$(":input[id='pdf.font-family']," +
      ":input[id='pdf.font-size']," +
      ":input[id='pdf.font-weight']," +
      ":input[id='pdf.font-style']," +
      ":input[id='pdf.text-decoration']," +
      ":input[id='pdf.space-before']," +
      ":input[id='pdf.space-after']," +
      ":input[id='pdf.color']").change(styleEditorHandler).change();
    $(":input.length-value").keydown(valueChangeHandler);
});

// UI --------------------------------------------------------------------------

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
}
function editableListHandler(store, list, other) {
	if (list.val() == "#other") {
		other.show().prop("disabled", false).focus();
		store.val(other.val());
	} else {
		other.hide().prop("disabled", true);
		store.val(list.val());
	}
}
function editableOtherHandler(store, list, other) {
	if (list.find("option[value='" + other.val() + "']").length != 0) {
		other.hide().prop("disabled", true);
		list.val(other.val());
		store.val(list.val());
	} else {
		other.show().prop("disabled", false).focus();
		store.val(other.val());
	}
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
	var current = $("#pdf-style-selector-current");
	writeToStore(current.val());
	readFromStore(target.val());
	current.val(target.val());
}
var storeFields = ["font-family", "font-size", "color", "font-weight", "font-style", "color", "space-before", "space-after"];
function readFromStore(type) {
	for (var i = 0; i < storeFields.length; i++) {
		var model = $(":input[name='pdf." + storeFields[i] + "." + type + "']");
		// if no value, inherit from body
//		if (model.is(".inherit-from-body") && (s.val() == undefined || s.val() == "")) {
//			model = $(":input[name='pdf." + storeFields[i] + "." + "body" + "']");
//		}
		var view = $(":input[id='pdf." + storeFields[i] + "']");
		if (view.is(":checkbox")) {
			if (model.val() == view.val()) {
				view.attr("checked", true);
			} else {
				view.removeAttr("checked");
			}
		} else if (view.is(".editable-list")) {
			var id = view.attr("name") != undefined ? ui.attr("name") : view.attr("id");
			var other = $(":input[id='" + id + ".other']");
			other.val(model.val()).change();
		} else {
			view.val(model.val());
		}
	}
}
function writeToStore(type) {
	for (var i = 0; i < storeFields.length; i++) {
		writeFieldToStore(storeFields[i], type);
	}
}
function writeFieldToStore(field, type) {
	var view = $(":input[id='pdf." + field + "']");
	var model = $(":input[name='pdf." + field + "." + type + "']");
	// if equals body value, treat as inherit value
//	var b = $(":input[name='pdf." + field + "." + "body" + "']");
//	if (model.is(".inherit-from-body") && view.val() == b.val()) {
//		model.val(undefined);
//		return;
//	}
	if (view.is(":checkbox")) {
		if (view.is(":checked")) {
			//s.removeAttr("disabled");
			model.val(view.val());
		} else {
			model.val("normal");
			//s.attr("disabled", true);
		}
	} else if (view.is(".editable-list")) {
		model.val(view.val());
	} else {
		model.val(view.val());
	}		
}
/**
 * Update store when UI changes
 * @param event UI change event
 */
function styleEditorHandler(event) {
	var ui = $(event.target);
	var type = $("#pdf-style-selector-current").val();
	var field = ui.attr("id");
	field = field.substring(field.indexOf(".") + 1);
	writeFieldToStore(field, type);
}
