define([
  '../app/pdf-utils'
], function (
  Utils
) {
  return function StyleController() {

    const storeFields = ['font-family', 'font-size', 'font-weight', 'font-style', 'color', 'background-color', 'space-before', 'space-after', 'start-indent', 'text-align', 'text-decoration', 'line-height',
      // titles
      'title-numbering',
      // note
      'icon',
      // link
      'link-page-number', 'link-url',
      // dl
      'dl-type',
      // ol
      'ol-1', 'ol-2', 'ol-3', 'ol-4',
      'ol-before-1', 'ol-before-2', 'ol-before-3', 'ol-before-4',
      'ol-after-1', 'ol-after-2', 'ol-after-3', 'ol-after-4',
      'ol-sublevel',
      // ul
      'ul-1', 'ul-2', 'ul-3', 'ul-4',
      // table, fig
      'caption-number', 'caption-position']

    var styleModel = $("#style-model :input")
    styleModel.change(previewSpaceHandler).change()
    _.forEach(storeFields, function (field) {
      $(":input[id='" + field + "']").change(styleEditorHandler)
    })
    $("#style-selector").change(styleHandler)
    readFromModel('body');// initialize style dialog
    var pdfStyleSelectorCurrent = 'body'
    $("#style-selector").change()

    // Style dialog methods

    function previewSpaceHandler(event) {
      var model = $(event.target)
      var id = model.attr('name')
      var idx = id.indexOf(".")
      var field = id.substring(0, idx)
      var type = id.substring(idx + 1)

      var v = Utils.getVal(model)
      if (v === undefined && model.data('inherit') !== undefined) {
        v = Utils.getVal($(":input[name='" + field + "." + model.data('inherit') + "']"))
      }

      var isLength = false
      var property
      switch (field) {
        case 'space-before':
          property = 'margin-top'
          isLength = true
          break
        case 'space-after':
          property = 'margin-bottom'
          isLength = true
          break
        case 'start-indent':
          property = 'margin-left'
          isLength = true
          break
        case 'font-size':
          property = field
          isLength = true
          break
        case 'line-height':
          property = field
          isLength = isNaN(Number(v))
          break
        case 'text-align':
          property = field
          switch (v) {
            case 'start':
              v = 'left'
              break
            case 'end':
              v = 'right'
              break
          }
          break
        default:
          var all = $("[data-field='" + field + "'][data-style='" + type + "']")
          if (all.length) {
            if (all.filter("[data-value]").length) {
              all.hide()
              all.filter("[data-value='" + v + "']").show()
            } else {
              all.text(v)
            }
          } else {
            property = field
          }
          break
      }
      if (property !== undefined) {
        if (isLength) {
          if (v === undefined) { // support undefined values
            return true
          }
          v = Utils.toPt(v)
          var f = 0.9
          v = String(v * f) + 'px'
        }
        $("*[class~='example-page-content-" + type + "']").css(property, v)
      }
    }

    /**
     * Change which style to edit
     * @param event UI change event
     */
    function styleHandler(event) {
      var target = $(event.target)
      var style = target.val()
      $("#style-form [data-style]").each(function () {
        var f = $(this)
        f.toggle($(this).attr('data-style').split(" ").indexOf(style) !== -1)
      })
      var type = target.find(":selected").parent("optgroup.block")
      if (type.length === 0) {
        $(".style-selector-block").hide().find(":input").attr('disabled', true)
      } else {
        $(".style-selector-block").show().find(":input").removeAttr('disabled')
      }
      pdfStyleSelectorCurrent = target.val()
      readFromModel(target.val())
    }

    /**
     * Read fields from model to UI.
     * @param type
     */
    function readFromModel(type) {
      for (var i = 0; i < storeFields.length; i++) {
        var model = styleModel.filter("[name='" + storeFields[i] + "." + type + "']")
        // if no value, inherit from body
        if (model.data('inherit') !== undefined && (model.val() === undefined || model.val() === "")) {
          model = styleModel.filter("[name='" + storeFields[i] + "." + 'body' + "']")
        }
        var view = $("#style-form :input[id='" + storeFields[i] + "']")
        if (view.is(":checkbox")) {
          view.prop('checked', model.val() === view.val())
        } else if (view.is(".editable-list")) {
          //var id = view.attr('name') !== undefined ? ui.attr('name') : view.attr('id')
          //var id = storeFields[i];//view.attr('id')
          //var store = styleModel.filter("[id='" + id + "']")
          //store.val(model.val())
          //store.change()
          //console.log("readFromModel: " + storeFields[i] + " = " + model.val())
          view.val(model.val())
        } else {
          view.val(model.val())
        }
        view.change()
      }
    }

    function writeFieldToModel(field, type) {
      var view = $("#style-form :input[id='" + field + "']")
      var model = styleModel.filter("[name='" + field + "." + type + "']")
      var oldValue = model.val()
      var newValue
      if (view.is(":checkbox")) {
        if (view.is(":checked")) {
          newValue = view.val()
        } else if (field === 'text-decoration') {
          newValue = 'none'
        } else {
          newValue = 'normal'
        }
      } else if (view.is(".editable-list")) {
        newValue = view.val()
      } else {
        newValue = view.val()
      }

      // if equals body value, treat as inherit value
      if (model.data('inherit') !== undefined) {
        var b = styleModel.filter("[name='" + field + "." + 'body' + "']")
        if (oldValue === b.val()) {
          newValue = undefined
        }
        // update inheriting model fields
      } else if (type === 'body') {
        styleModel.filter("[data-inherit=body]").each(function () {
          var m = $(this)
          if (m.is("[name^='" + field + "']")) {
            if (m.val() === undefined || m.val() === "" || m.val() === oldValue) {
              m.val(newValue)
              m.change()
            }
          }
        })
      }

      model.val(newValue)
      // fire change event
      model.change()
    }

    /**
     * Update store when UI changes
     * @param event UI change event
     */
    function styleEditorHandler(event) {
      var ui = $(event.target)
      var field = ui.attr('id')
      writeFieldToModel(field, pdfStyleSelectorCurrent)
    }
  }
})