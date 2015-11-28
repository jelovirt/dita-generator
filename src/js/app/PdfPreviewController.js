define([
  '../app/pdf-utils'
], function (
  Utils
) {
  return function PdfPreviewController() {
    var factor = 0.12

    $(":input[name='title-numbering']").change(titleNumberingHandler).change()
    $(":input[name='table-numbering']," +
      ":input[name='figure-numbering']").change(tableAndFigureNumberingHandler).change()
    $(":input[name='dl']").change(definitionListHandler).change()
    $(":input[name='mirror-page-margins']").change(mirrorPageHandler).change()
    $(":input[name='task-label']").change(taskLabelHandler).change()
    $(":input[name='force-page-count']").change(forcePageCountChangeHandler).change()
    $(":input[name='page-size']," +
      ":input[name='orientation']," +
      ":input[name='page-margin-top']," +
      ":input[name='page-margin-bottom']," +
      ":input[name='page-margin-inside']," +
      ":input[name='page-margin-outside']," +
      ":input[name='body-column-count']," +
      ":input[name='column-gap']").change(pageMarginHandler).first().change()

    function pageMarginHandler(event) {
      $('.example-page').each(function () {
        updatePageExample($(this))
      })
      $('.example-block-page').each(function () {
        updateFixedPageExample($(this))
      })
    }

    /**
     * For pages with fixed factor
     */
    function updatePageExample(page) {
      var isOdd = page.is('.odd')
      var dim = readPageDimensions()

      page.height(dim.pageHeight * factor)
      page.width(dim.pageWidth * factor)

      var content = page.find('.example-page-body')
      content.css('margin-top', (dim.marginTop * factor) +  'px')
      content.css(isOdd ?  'margin-right' :  'margin-left', (dim.marginOutside * factor) +  'px')
      content.css('margin-bottom', (dim.marginBottom * factor) +  'px')
      content.css(isOdd ?  'margin-left' :  'margin-right', (dim.marginInside * factor) +  'px')
      content.height((dim.pageHeight - dim.marginTop - dim.marginBottom) * factor)
      content.width((dim.pageWidth - dim.marginInside - dim.marginOutside) * factor)

      var columns = Number($(":input[name='body-column-count']").val())
      var columnWidth = Utils.toPt(Utils.getVal($(":input[name='column-gap']")))
      var tr = page.find(".example-page-body tr")
      var buf = $("<tr></tr>")
      for (var i = 0; i < columns; i++) {
        if (i !== 0) {
          buf.append($("<td class='gap'><span/></td>").width(columnWidth * factor))
        }
        buf.append($("<td><div/></td>"))
      }
      tr.replaceWith(buf)
    }

    /**
     * For pages with fixed width
     */
    function updateFixedPageExample(page) {
      var dim = readPageDimensions()

      var blockWidth = 700
      var factor = blockWidth / dim.pageWidth

      var content = page.find('.example-page-content')
      content.css('margin-right', (dim.marginOutside * factor) +  'px')
      content.css('margin-left', (dim.marginInside * factor) +  'px')
    }

    /**
     * Page dimensions in points.
     */
    function Dimensions() {
      var pageWidth
      var pageHeight
      var marginTop
      var marginOutside
      var marginBottom
      var marginInside
    }

    /**
     * Return page dimensions in points.
     */
    function readPageDimensions() {
      var res = new Dimensions()

      var pageSize = $(":input[name='page-size']").val().split(' ')
      if ($(':input[name=orientation]').val() ===  'landscape') {
        res.pageWidth = Utils.toPt(pageSize[1])
        res.pageHeight = Utils.toPt(pageSize[0])
      } else {
        res.pageWidth = Utils.toPt(pageSize[0])
        res.pageHeight = Utils.toPt(pageSize[1])
      }
      res.marginTop = Utils.toPt(Utils.getVal($(":input[name='page-margin-top']")))
      res.marginOutside = Utils.toPt(Utils.getVal($(":input[name='page-margin-outside']")))
      res.marginBottom = Utils.toPt(Utils.getVal($(":input[name='page-margin-bottom']")))
      res.marginInside = Utils.toPt(Utils.getVal($(":input[name='page-margin-inside']")))

      return res
    }

    function forcePageCountChangeHandler(event) {
      var target = $(event.target)
      $(".force-page-count_example_auto, .force-page-count_example_odd, .force-page-count_example_even").each(function () {
        var t = $(this)
        if (t.is('.force-page-count_example_' + target.val())) {
          t.show()
        } else {
          t.hide()
        }
      })
    }

    function taskLabelHandler(event) {
      var target = $(event.target)
      var e = $('.example-task-label')
      if (target.is(":checked")) {
        e.show()
      } else {
        e.hide()
      }
    }

    function mirrorPageHandler(event) {
      var target = $(event.target)
      var evenPage = $('.even')
      if (target.prop('checked')) {
        evenPage.show()
      } else {
        evenPage.hide()
      }
      pageMarginHandler(event)
    }

    function definitionListHandler(event) {
      var target = $(event.target)
      $("*[id='dl.example.html'], *[id='dl.example.list'], *[id='dl.example.table']").hide()
      $("*[id='dl.example." + target.val() + "']").show()
    }

    function titleNumberingHandler(event) {
      var target = $(event.target)
      var preview = $("*[id='title-numbering.example']")
      preview.children().hide()
      $("*[id='title-numbering.example." + target.val() + "']").show()
    }

    function tableAndFigureNumberingHandler(event) {
      var target = $(event.target)
      var preview = $("*[id='" + target.attr('name') + ".example']")
      if (target.val() ===  'none') {
        preview.hide()
      } else {
        preview.show()
      }
    }
  }
})