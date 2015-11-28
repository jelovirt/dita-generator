var attributePattern = new RegExp(nmtokens);

var rootTest = new RegExp("^\\s*(topic|concept|task|reference)\\s*$");

/** Current location fragment. */
var hash = location.hash;
/** Attribute domain counter. */
var attributeCounter = 0;

function validateForm(event) {
  var target = event.target;
  for (var i = 0; i < target.elements.length; i++) {
    var elem = target.elements[i]
    if (elem.className === "required" && !elem.disabled) {
      var value;
      switch (elem.nodeName.toLowerCase()) {
      case "select":
        for (var k = 0; k < elem.options.length; k++) {
          if (elem.options[k].selected) {
            value = elem.options[k].value;
            break;
          }
        }
        break;
      default:
        value = elem.value;
      }
      if (value === "") {
        var label = getLabel(elem);
        alert("Required field " + label.toLowerCase() + " has no value");
        return cancelEvent(event);
      } else if (elem.name === "root" && rootTest.test(value)) {
        var label = getLabel(elem);
        alert("Field " + label.toLowerCase() + " may not use the value '"+ value + "' because specializations may not redefine DITA elements");
        return cancelEvent(event);
      }
    }
  }
  return true;
}

function versionChangeHandler(event) {
    var value = $(":input[name=version]").attr("value");
    if (value == 1.2) {
        $(".v1_2").removeClass("disabled").find("input").removeAttr("disabled");
        $("select[name=file] option[value=ent]").removeClass("disabled");
    } else {
        $(".v1_2").addClass("disabled").find("input").attr("disabled", true);
        $("select[name=file] option[value=ent]").addClass("disabled");
    }
    topicChangeHandler();
    return true;
}

/**
 * Output type handler.
 */
function typeChangeHandler(event) {
    var value = $(":input[name=output]").attr("value")
    if (value == "specialization") {
        $("#stylesheet").show().find(":input").removeAttr("disabled");
        $("input[name=root]").removeAttr("disabled").parents("tr").show();
        $("select[name=file] option[value=mod], select[name=file] option[value=ent]").show(); // advanced
    } else {
        $("#stylesheet").hide().find(":input").attr("disabled", true);
        $("input[name=root]").attr("disabled", true).parents("tr").hide();
        $("select[name=file] option[value=mod], select[name=file] option[value=ent], #stylesheet").hide(); // advanced
    }
    return true;
}

/**
 * Topic or map type handler.
 */
function topicChangeHandler(event) {
    var version = $(":input[name=version]").val();
    var type = $(":input[name=type]:checked").val();
    var cls = (type != "" && type != undefined) ? domains[version][type].domainClass : [];
    // filter domains
    var ds = $(".domain");
    ds.each(function(i) {
        var cur = $(this);
        var enabled = false;
        if (type == "") {
            enabled = true;
        } else {
            $.each(cls, function() {
               if (cur.hasClass(this)) {
                   enabled = true;
                   return false;
               }
            });
       }
       var row = cur.parents("tr:first");
       if (enabled) {
           row.show();
           cur.not("*:input").show();
           cur.filter("*:input").removeAttr("disabled");
       } else {
           row.hide();
           cur.not("*:input").hide();
           cur.filter("*:input").attr("disabled", true);
       }
    });
    // filter nested topics
    if ($.inArray("topic", cls) == -1) {
        $("input[name='nested']").attr("disabled", true);
    } else {
        $("input[name='nested']").removeAttr("disabled");
    }
    return true;
}

function domainEnabled(cur, version, type) {
    if (type == "") {
        enabled = true;
    } else {
        $.each(cls, function() {
            if (cur.hasClass(this)) {
                enabled = true;
                return false;
            }
        });
    }
}

/**
 * Check default domains.
 */
function selectDefaultDomains(event) {
    var version = $(":input[name='version']").val();
    var type = $(":input[name='type']:checked").val();
    if (type != undefined && type != "") {
        var ds = domains[version][type].defaultDomains;
        $("input[name='domain']").val(ds);
    }
}
/**
 * Check all domains.
 */
function selectAllDomains(event) {
    $("input[name='domain']").attr("checked", true);
}
/**
 * Uncheck all domain
 */
function selectNoneDomains(event) {
    $("input[name='domain']").removeAttr("checked");
}

function attributeAddHandler(event) {
    $("#noAttributesRow").hide();
    $("#attributes thead,#generate-subject-scheme").show();
    
    var tr = $("<tr></tr>");
    tr.append("<td><input name='name' size='15'></td>");
    tr.append("<td><select name='type'><option value='props'>props</option><option value='base'>base</option></select></td>");
    tr.append("<td><select name='datatype'><option value='CDATA'>Any</option><option value='NMTOKENS'>Enum</option></select> "
              + "<input name='values' style='display:none' disabled title='Space-separated list of possible values'></td>");
    // Add change handlers
    tr.find("select").change(function(event) {
            var t = $(event.target);
            var values = t.nextAll("input:first");
            if (t.val() == "NMTOKENS") {
                values.show().removeAttr("disabled");
            } else {
                values.hide().attr("disabled", true);
            }
        });
    tr.find("input[name=values]").change(function(event) {
        var t = $(event.target);
        var val = $.trim(t.attr("value"));
        if (!attributePattern.test(val)) {
            setError(t, $("<span>Values must be space separated XML names</span>"),
                     "Values must be space separated XML names");
        } else {
            setOk(t);
        }
    });
    // Add counter
    attributeCounter++;
    tr.find(":input").each(function() {
        var t = $(this);
        t.attr("name", "att." + attributeCounter + "." + t.attr("name"));
    });
    // Add remove button
    var r = $("<td><button type='button'>Remove</button></td>");
    r.find("button").click(attributeRemoveHandler);
    tr.append(r);

    $("#attributes tbody").append(tr);
}

function attributeRemoveHandler(event) {
    $(event.target).parents("tr:first").remove();
    if ($("#attributes tbody tr:visible").length === 0) {
        $("#noAttributesRow").show();
        $("#attributes thead,#generate-subject-scheme").hide();
    }
}

function idChangeHandler(event) {
    var id = $(event.target);
    var val = id.attr("value");    
    if (!pluginPatter.test(val)) { //!namePattern.test(val)
        setError(id, $("<span>Not a valid XML name</span>"),
                 "Type ID must be a valid XML name.");
    } else {
        setOk(id);
    }
}

function rootChangeHandler(event) {
    var id = $(event.target);
    var val = id.attr("value");
    if (!namePattern.test(val)) {
        setError(id, $("<span>Not a valid XML element name</span>"),
                 "Type ID must be a valid XML element name.");
    } else {
        setOk(id);
    }
}

// Initialization

$(document).ready(function() {
    $(":input[name=output]").change(typeChangeHandler);
    $(":input[name=version]").change(versionChangeHandler);
    $(":input[name=type]").change(topicChangeHandler);
    $(":input[name=id]").change(idChangeHandler);
    $(":input[name=root]").change(rootChangeHandler);
    $("#selectDefaultDomains").click(selectDefaultDomains);
    $("#selectAllDomains").click(selectAllDomains);
    $("#selectNoneDomains").click(selectNoneDomains);
    $("#addAttribute").click(attributeAddHandler);
    $("form").submit(validateForm);
    // init
    topicChangeHandler();
    typeChangeHandler();
    versionChangeHandler();
});