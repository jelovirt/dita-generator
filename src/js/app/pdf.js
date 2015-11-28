define([
  '../app/StyleController',
  '../app/pdf-utils',
  '../app/pdf-preview'
], function (
  StyleController,
  Utils
) {
  function toolkitVersionChangeHandler(event) {
    toggleByClass($(event.target), "v")
  }

  function formatterHandler(event) {
    toggleByClass($(event.target), "f")
  }

  function toggleByClass(p, prefix) {
    var val = p.val()
    p.find("option").each(function () {
      var s = $(this).attr("value")
      var c = "." + prefix + s.replace(/\./g, "_")
      $(c).addClass("disabled").find(":input").attr("disabled", true)
    })
    p.find("option").each(function () {
      var s = $(this).attr("value")
      var c = "." + prefix + s.replace(/\./g, "_")
      if (val == s) {
        $(c).removeClass("disabled").find(":input").removeAttr("disabled")
      }
    })
  }

  /**
   * Validate transtype value.
   */
  function transtypeChangeHandler(event) {
    var id = $(event.target)
    var val = id.attr("value")
    if (!pluginPatter.test(val)) { //!namePattern.test(val)
      setError(id, $("<span>Not a valid XML name</span>"),
        "Type ID must be a valid XML name.")
    } else {
      setOk(id)
    }
  }

// UI --------------------------------------------------------------------------

  function validateLength(event) {
    var target = $(event.target)
    var val = Utils.toPt(Utils.getVal(target))
    if (val == undefined) {
      setError(target, $("<span>Invalid value</span>"), "Invalid XSL FO length value")
    } else {
      setOk(target)
    }
  }

  function coverChangeHandler(event) {
    var target = $(event.target)
    var $all = $('#cover_image_file, #cover_image_metadata, #cover_image_topic')
    $('#cover_image_' + target.val()).prop("disable", false).show()
    $all.not('#cover_image_' + target.val()).prop("disable", true).hide()
  }

// Column methods

  /**
   * Show/hide column gap input based on column count.
   */
  function columnChangeHandler(event) {
    var target = $(event.target)
    if (target.val() == 1) {
      $(":input[name='column-gap']").prop("disable", true).parent().hide()
    } else {
      $(":input[name='column-gap']").prop("disable", false).parent().show()
    }
  }

// Editable list methods

  function editableHandler(event) {
    var target = $(event.target)
    var id = target.attr("name") != undefined ? target.attr("name") : target.attr("id")
    var list = $(":input[id='" + id + ".list" + "']")
    var other = $(":input[id='" + id + ".other" + "']")
    other.val(target.val())
    if (list.find("option[value='" + other.val() + "']").length != 0) { // same value in list
      other.hide().prop("disabled", true)
      list.val(other.val())
      other.val(undefined)
    } else {
      list.val("#other")
      other.show().prop("disabled", false).focus()
    }
  }

  function editableListHandler(store, list, other) {
    if (list.val() == "#other") {
      store.val(other.val()).change()
    } else {
      store.val(list.val()).change()
    }

  }

  function editableOtherHandler(store, list, other) {
    store.val(other.val()).change()
  }

  // Value increment/decrement methods

  function valueChangeHandler(event) {
    switch (event.keyCode) {
      case 38:
        var t = $(event.target)
        addToValue(t, 1)
        event.preventDefault()
        event.stopPropagation()
        t.change()
        return false
      case 40:
        var t = $(event.target)
        addToValue(t, -1)
        event.preventDefault()
        event.stopPropagation()
        t.change()
        return false
    }
  }

  function addToValue(target, add) {
    var val = target.val()
    if (val == "") {
      val = target.attr("placeholder")
    }
    var num = Number(val.substring(0, val.length - 2))
    var unit = val.substring(val.length - 2)
    target.val((num + add).toString() + unit)
  }

  // Init

  StyleController()
  init()

  function init() {
    // widget initialization
    $(":input.editable-list").each(function () {
      var s = $(this)
      var id = s.attr("name") != undefined ? s.attr("name") : s.attr("id")
      var l = $(":input[id='" + id + ".list']")
      var o = $(":input[id='" + id + ".other']")
      s.change(editableHandler)
      o.change(function () {
        editableOtherHandler(s, l, o)
      })
      l.change(function () {
        editableListHandler(s, l, o)
      })
    })

    // form initialization
    $(":input[name='ot.version']").change(toolkitVersionChangeHandler).change()
    $(":input[name='formatter']").change(formatterHandler).change()
    $(":input[name='transtype']").change(transtypeChangeHandler)
    $(":input[name='body-column-count']").change(columnChangeHandler).change()
    $("#cover_image_chooser").change(coverChangeHandler).change()
    $(":input.length-value").keydown(valueChangeHandler).change(validateLength)
  }

})