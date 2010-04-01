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

function validatePage() {
    var elements = $(".current .required:enabled");
    var valid = true;
    if (elements.filter(":radio, :checkbox").length > 0 && elements.filter(":checked").length == 0) {
        valid = false;
    }
    if (elements.find("option").length > 0 && elements.find("option:selected").length == 0) {
        value = true;
    }
    elements.filter(":text").each(function(i) {
        var elem = $(this);
        var value = elem.val();
        if (value === "") {
            valid = false;
        }
    });
    if (elements.filter(".invalid").length > 0) {
        valid = false;
    }
    
    if ($(".current").prevAll(".page:first").length === 0) { // first page
        $("#prev").attr("disabled", true);
    } else {
        $("#prev").removeAttr("disabled");
    }
    if ($(".current").nextAll(".page:first").length === 0) { // last page
        $("#next").attr("disabled", true);
        if (valid) {
            $("#generate").removeAttr("disabled");
        } else {
            $("#generate").attr("disabled", true);
        }
    } else {
        if (valid) {
            $("#next").removeAttr("disabled");
        } else {
            $("#next").attr("disabled", true);
        }
        $("#generate").attr("disabled", true);
    }
    //alert(valid);
    return true;
}

function getLabel(elem) {
    return $("label[for=" + elem.name + "]:first").text();
}

function cancelEvent(event) {
    if (event.preventDefault) {
      event.stopPropagation();
      event.preventDefault();
    } else {
      event.cancelBubble = true;
      event.returnValue = false;
    }
    return false;
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
        $("input[name=nested]").attr("disabled", true);
    } else {
        $("input[name=nested]").removeAttr("disabled");
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
    var version = $(":input[name=version]").val();
    var type = $(":input[name=type]:checked").val();
    if (type != undefined && type != "") {
        var ds = domains[version][type].defaultDomains;
        $("input[name=domain]").val(ds);
    }
}
/**
 * Check all domains.
 */
function selectAllDomains(event) {
    $("input[name=domain]").attr("checked", true);
}
/**
 * Uncheck all domain
 */
function selectNoneDomains(event) {
    $("input[name=domain]").removeAttr("checked");
}

/**
 * Previous page button handler.
 */
function prevHandler(event) {
    var p = $(".current").prevAll(".page:not(.disabled):first");
    $(".current").removeClass("current").hide();
    p.addClass("current").show();
    validatePage();
    setFragment();
}
/**
 * Next page button handler.
 */
function nextHandler(event) {
    var n = $(".current").nextAll(".page:not(.disabled):first");
    $(".current").removeClass("current").hide();
    n.addClass("current").show();
    validatePage();
    setFragment();
}

/** Set location fragment to current page. */
function setFragment(i) {
    hash = $(".current").attr("id");
    location.hash = hash;
}
/** Check if location fragment has changed and change page accordingly. */
function checkFragment() {
    if (location.hash.substr(1) != hash) {
        //alert("changed: " + location.hash.substr(1) + " " + hash);
        if (location.hash.substr(1) == "") {
            location.replace("#" + $(".page:first").attr("id"));
        }
        hash = location.hash.substr(1);
        $(".current").removeClass("current").hide();
        $("#" + hash).addClass("current").show();
        validatePage();
    }
}

function attributeAddHandler(event) {
    $("#noAttributesRow").hide();
    
    attributeCounter++;
    var tr = $("<tr></tr>");
    var p = "att." + attributeCounter; 
    tr.append("<td><input name='" + p + ".name'></td>");
    tr.append("<td><select name='" + p + ".type'><option value='props'>props</option><option value='base'>base</option></select></td>");
    var d = $("<td><select name='" + p + ".datatype'><option value='CDATA'>space-separated values</option><option value='NMTOKENS'>enumeration</option></select> "
              + "<input name='" + p + ".values' style='display:none' disabled title='Space-separated list of possible values'></td>");
    d.find("select").change(function(event) {
            var t = $(event.target);
            if (t.val() == "NMTOKENS") {
                t.nextAll("input").show().removeAttr("disabled");
            } else {
                t.nextAll("input").hide().attr("disabled", true);
            }
        });
    tr.append(d);
    var r = $("<td><button type='button'>remove</button></td>");
    r.find("button").click(function(event) {
            $(event.target).parents("tr:first").remove();
            if ($("#attributes tbody tr:visible").length === 0) {
                $("#noAttributesRow").show();
            }
        });
    tr.append(r);
    $("#attributes tbody").append(tr);
}

// XML 1.0 fifth edition rules
var nameStartChar = ":|[A-Z]|_|[a-z]|[\u00C0-\u00D6]|[\u00D8-\u00F6]|[\u00F8-\u02FF]|[\u0370-\u037D]|[\u037F-\u1FFF]|[\u200C-\u200D]|[\u2070-\u218F]|[\u2C00-\u2FEF]|[\u3001-\uD7FF]|[\uF900-\uFDCF]|[\uFDF0-\uFFFD]"; //|[\u10000-\uEFFFF]
var nameChar = nameStartChar + "|-|\\.|[0-9]|\u00B7|[\u0300-\u036F]|[\u203F-\u2040]";
var name = "^(" + nameStartChar + ")(" + nameChar + ")*$";

function idChangeHandler(event) {
    var id = $(event.target);
    var val = id.attr("value");
    var idPattern = new RegExp(name);
    if (!idPattern.test(val)) {
        setError(id, $("<span>Not a valid <a href='http://www.w3.org/TR/REC-xml/#NT-Name' target='_blank'>XML name</a></span>"),
                 "Type ID must be a valid XML name.");
    } else {
        setOk(id);
    }
}

function setError(input, text, tip) {
    setMessage(input, "err", text, tip);
    input.addClass("invalid");
}
function setWarning(input, text, tip) {
    setMessage(input, "warn", text, tip);
    input.removeClass("invalid");
}
function setOk(input) {
    setMessage(input, "ok");
    input.removeClass("invalid");
}
function setMessage(input, level, text, tip) {
    var msg = input.nextAll(".msg");
    if (msg.length == 0) {
        msg = $("<span class='msg'></span>");
        input.after(msg);
    }
    msg.removeClass().addClass("msg " + level);
    if (text != undefined) {
        msg.append(text);
    } else {
        msg.empty();
    }
    if (tip != undefined) {
        msg.attr("title", tip);
    } else {
        msg.removeAttr("title");
    }
}

// Initialization

$(document).ready(function() {
    // handlers
    $(":input[name=output]").change(typeChangeHandler);
    $(":input[name=version]").change(versionChangeHandler);
    $(":input[name=type]").change(topicChangeHandler);
    $(":input[name=id]").change(idChangeHandler);
    $(":input").change(validatePage);
    $("#selectDefaultDomains").click(selectDefaultDomains);
    $("#selectAllDomains").click(selectAllDomains);
    $("#selectNoneDomains").click(selectNoneDomains);
    $("#addAttribute").click(attributeAddHandler);
    $("form").submit(validateForm);
    // wizard pages
    $(".page").each(function(i) { $(this).attr("id", "p" + i); }).hide();
    $(".page:first").addClass("current").show();
    var prev = $("<button type='button' id='prev'>&lt; Previous</button>").click(prevHandler);
    var next = $("<button type='button' id='next'>Next &gt;</button>").click(nextHandler);
    $("#generate").before(prev).before(" ").before(next).before(" ");
    // init
    topicChangeHandler();
    typeChangeHandler();
    versionChangeHandler();
    validatePage();

    setInterval(checkFragment, 100);
});