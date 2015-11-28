// XML 1.0 fifth edition rules
var nameStartChar = ":|[A-Z]|_|[a-z]|[\u00C0-\u00D6]|[\u00D8-\u00F6]|[\u00F8-\u02FF]|[\u0370-\u037D]|[\u037F-\u1FFF]|[\u200C-\u200D]|[\u2070-\u218F]|[\u2C00-\u2FEF]|[\u3001-\uD7FF]|[\uF900-\uFDCF]|[\uFDF0-\uFFFD]"; //|[\u10000-\uEFFFF]
var nameChar = nameStartChar + "|-|\\.|[0-9]|\u00B7|[\u0300-\u036F]|[\u203F-\u2040]";
var name = "^(" + nameStartChar + ")(" + nameChar + ")*$";
var nmtoken = "(" + nameChar + ")+";
var nmtokens = "^(" + nameChar + ")+(\\s+(" + nameChar + ")+)*$";

var namePattern = new RegExp(name);
var pluginPatter = new RegExp("[a-zA-Z\\-_]+(\\.[a-zA-Z\\-_]+)*")

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
        msg.html(text);
    } else {
        msg.empty();
    }
    if (tip != undefined) {
        msg.attr("title", tip);
    } else {
        msg.removeAttr("title");
    }
}

function helpHandler(event) {
  $(event.target).parents("fieldset:first").find(".help").show("fast");
  return cancelEvent(event);
}

function closeHandler(event) {
  $(event.target).parents(".help").hide("fast");
  return cancelEvent(event);
}

// Initialization

$(document).ready(function() {
    $(":input").change(validatePage);
    $("form").submit(validateForm);
    // wizard pages
    $(".page").each(function(i) {$(this).attr("id", "p" + i);}).hide();
    $(".page:first").addClass("current").show();
    var prev = $("<button type='button' id='prev'>&lt; Previous</button>").click(prevHandler);
    var next = $("<button type='button' id='next'>Next &gt;</button>").click(nextHandler);
    $("#generate").before(prev).before(" ").before(next).before(" ");
    // help
    $("fieldset label:not(.inline)").each(function() {
        var l = $(this);
        if (l.parents("fieldset:first").find(".help").length != 0) {
           l.append($("<span class='help-icon' title='Show help'></span>").click(helpHandler));
        }
    });
    $("fieldset .help").hide().each(function() {
        var l = $(this);
        l.prepend($("<span class='close-icon' title='Close help'></span>").click(closeHandler));
    });
    // init
    validatePage();

    setInterval(checkFragment, 100);
});