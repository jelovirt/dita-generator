# -*- coding: UTF-8; indent-tabs-mode:nil; tab-width:4 -*-

# This file is part of DITA DTD Generator.
#
# Copyright 2009 Jarno Elovirta <http://www.elovirta.com/>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import ditagen.dita
import ditagen.dita.v1_1
import ditagen.dita.v1_2
from ditagen.generator import DitaGenerator
from ditagen.generator import Version
import ditagen.generator
import StringIO
from zipfile import ZipFile, ZipInfo
from xml.etree import ElementTree as ET
from datetime import datetime

NS_XSL = "{http://www.w3.org/1999/XSL/Transform}"
NS_FO = "{http://www.w3.org/1999/XSL/Format}"

properties = set(["absolute-position", "active-state", "alignment-adjust", "alignment-baseline", "allowed-height-scale", "allowed-width-scale", "auto-restore", "azimuth", "background-attachment", "background-color", "background-image", "background-position-horizontal", "background-position-vertical", "background-repeat", "baseline-shift", "blank-or-not-blank", "block-progression-dimension", "border-after-color", "border-after-precedence", "border-after-style", "border-after-width", "border-before-color", "border-before-precedence", "border-before-style", "border-before-width", "border-bottom-color", "border-bottom-style", "border-bottom-width", "border-collapse", "border-end-color", "border-end-precedence", "border-end-style", "border-end-width", "border-left-color", "border-left-style", "border-left-width", "border-right-color", "border-right-style", "border-right-width", "border-separation", "border-start-color", "border-start-precedence", "border-start-style", "border-start-width", "border-top-color", "border-top-style", "border-top-width", "bottom", "bottom", "break-after", "break-before", "caption-side", "case-name", "case-title", "change-bar-class", "change-bar-color", "change-bar-offset", "change-bar-placement", "change-bar-style", "change-bar-width", "character", "clear", "clip", "color", "color-profile-name", "column-count", "column-gap", "column-number", "column-width", "content-height", "content-type", "content-width", "country", "cue-after", "cue-before", "destination-placement-offset", "direction", "display-align", "dominant-baseline", "elevation", "empty-cells", "end-indent", "ends-row", "extent", "external-destination", "float", "flow-map-name", "flow-map-reference", "flow-name", "flow-name-reference", "font-family", "font-selection-strategy", "font-size", "font-size-adjust", "font-stretch", "font-style", "font-variant", "font-weight", "force-page-count", "format", "glyph-orientation-horizontal", "glyph-orientation-vertical", "grouping-separator", "grouping-size", "height", "hyphenate", "hyphenation-character", "hyphenation-keep", "hyphenation-ladder-count", "hyphenation-push-character-count", "hyphenation-remain-character-count", "id", "index-class", "index-key", "indicate-destination", "initial-page-number", "inline-progression-dimension", "internal-destination", "intrinsic-scale-value", "intrusion-displace", "keep-together", "keep-with-next", "keep-with-previous", "language", "last-line-end-indent", "leader-alignment", "leader-length", "leader-pattern", "leader-pattern-width", "left", "left", "letter-spacing", "letter-value", "linefeed-treatment", "line-height", "line-height-shift-adjustment", "line-stacking-strategy", "margin-bottom", "margin-bottom", "margin-left", "margin-left", "margin-right", "margin-right", "margin-top", "margin-top", "marker-class-name", "master-name", "master-reference", "maximum-repeats", "media-usage", "merge-pages-across-index-key-references", "merge-ranges-across-index-key-references", "merge-sequential-page-numbers", "number-columns-repeated", "number-columns-spanned", "number-rows-spanned", "odd-or-even", "orphans", "overflow", "padding-after", "padding-before", "padding-bottom", "padding-end", "padding-left", "padding-right", "padding-start", "padding-top", "page-citation-strategy", "page-height", "page-number-treatment", "page-position", "page-width", "pause-after", "pause-before", "pitch", "pitch-range", "play-during", "precedence", "provisional-distance-between-starts", "provisional-label-separation", "reference-orientation", "ref-id", "ref-index-key", "region-name", "region-name-reference", "relative-align", "relative-position", "rendering-intent", "retrieve-boundary", "retrieve-boundary-within-table", "retrieve-class-name", "retrieve-position", "retrieve-position-within-table", "richness", "right", "right", "role", "rule-style", "rule-thickness", "scale-option", "scaling", "scaling-method", "score-spaces", "script", "show-destination", "source-document", "space-after", "space-before", "space-end", "space-start", "span", "speak", "speak-header", "speak-numeral", "speak-punctuation", "speech-rate", "src", "start-indent", "starting-state", "starts-row", "stress", "suppress-at-line-break", "switch-to", "table-layout", "table-omit-footer-at-break", "table-omit-header-at-break", "target-presentation-context", "target-processing-context", "target-stylesheet", "text-align", "text-align-last", "text-altitude", "text-decoration", "text-depth", "text-indent", "text-shadow", "text-transform", "top", "top", "treat-as-word-space", "unicode-bidi", "visibility", "voice-family", "volume", "white-space-collapse", "white-space-treatment", "widows", "width", "word-spacing", "wrap-option", "writing-mode", "z-index"])

styles = [{ "property": f[0], "type": f[1], "value": f[2], "inherit": f[3] } for f in [
    ("font-family", "body", "serif", None),
    ("font-size", "body", "10pt", None),
    ("color", "body", "black", None),
    ("background-color", "body", "transparent", None),
    ("font-weight", "body", "normal", None),
    ("font-style", "body", "normal", None),
    ("text-decoration", "body", "none", None),
    ("space-before", "body", "6pt", None),
    ("space-after", "body", "6pt", None),
    ("text-align", "body", "start", None),
    ("start-indent", "body", "25pt", None),
    ("line-height", "body", "1.2", None),
    
    ("font-family", "topic", "sans-serif", None),
    ("font-size", "topic", "18pt", None),
    ("color", "topic", "black", "body"),
    ("background-color", "topic", "transparent", None),
    ("font-weight", "topic", "bold", None),
    ("font-style", "topic", "normal", None),
    ("text-decoration", "topic", "none", "body"),
    ("space-before", "topic", "0pt", None),
    ("space-after", "topic", "16.8pt", None),
    ("text-align", "topic", "start", None),
    ("start-indent", "topic", "0pt", None),
    ("line-height", "topic", None, "body"),
    # custom
    ("title-numbering", "topic", "true", None),
    
    ("font-family", "topic.topic", "sans-serif", None),
    ("font-size", "topic.topic", "14pt", None),
    ("color", "topic.topic", "black", "body"),
    ("background-color", "topic.topic", "transparent", None),
    ("font-weight", "topic.topic", "bold", None),
    ("font-style", "topic.topic", "normal", None),
    ("text-decoration", "topic.topic", "none", "body"),
    ("space-before", "topic.topic", "12pt", None),
    ("space-after", "topic.topic", "5pt", None),
    ("text-align", "topic.topic", "start", None),
    ("start-indent", "topic.topic", "0pt", None),
    ("line-height", "topic.topic", None, "body"),
    # custom
    ("title-numbering", "topic.topic", "false", None),

    ("font-family", "topic.topic.topic", "sans-serif", None),
    ("font-size", "topic.topic.topic", "12pt", None),
    ("color", "topic.topic.topic", "black", "body"),
    ("background-color", "topic.topic.topic", "transparent", None),
    ("font-weight", "topic.topic.topic", "bold", None),
    ("font-style", "topic.topic.topic", "normal", None),
    ("text-decoration", "topic.topic.topic", "none", "body"),
    ("space-before", "topic.topic.topic", "12pt", None),
    ("space-after", "topic.topic.topic", "2pt", None),
    ("text-align", "topic.topic.topic", "start", None),
    ("start-indent", "topic.topic.topic", "0pt", None),
    ("line-height", "topic.topic.topic", None, "body"),
    # custom
    ("title-numbering", "topic.topic.topic", "false", None),
    
    ("font-family", "topic.topic.topic.topic", "serif", "body"),
    ("font-size", "topic.topic.topic.topic", "10pt", "body"),
    ("color", "topic.topic.topic.topic", "black", "body"),
    ("background-color", "topic.topic.topic.topic", "transparent", None),
    ("font-weight", "topic.topic.topic.topic", "bold", None),
    ("font-style", "topic.topic.topic.topic", "normal", None),
    ("text-decoration", "topic.topic.topic.topic", "none", "body"),
    ("space-before", "topic.topic.topic.topic", "12pt", None),
    ("space-after", "topic.topic.topic.topic", "0pt", None),
    ("text-align", "topic.topic.topic.topic", "start", None),
    ("start-indent", "topic.topic.topic.topic", None, "body"),
    ("line-height", "topic.topic.topic.topic", None, "body"),
    # custom
    ("title-numbering", "topic.topic.topic.topic", "false", None),

    ("font-family", "section", "sans-serif", None),
    ("font-size", "section", None, "body"),
    ("color", "section", None, "body"),
    ("background-color", "section", "transparent", None),
    ("font-weight", "section", None, "body"),
    ("font-style", "section", None, "body"),
    ("text-decoration", "section", None, "body"),
    ("space-before", "section", "15pt", None),
    ("space-after", "section", None, "body"),
    ("text-align", "section", None, "body"),
    ("start-indent", "section", None, "body"),
    ("line-height", "section", None, "body"),
    
    ("font-family", "note", None, "body"),
    ("font-size", "note", None, "body"),
    ("color", "note", None, "body"),
    ("background-color", "note", "transparent", None),
    ("font-weight", "note", None, "body"),
    ("font-style", "note", None, "body"),
    ("text-decoration", "note", None, "body"),
    ("space-before", "note", None, "body"),
    ("space-after", "note", None, "body"),
    ("text-align", "note", None, "body"),
    ("start-indent", "note", None, "body"),
    ("line-height", "note", None, "body"),
    # custom
    ("icon", "note", "icon", None),
    
    ("font-family", "pre", "monospace", None),
    ("font-size", "pre", None, "body"),
    ("color", "pre", None, "body"),
    ("background-color", "pre", "transparent", None),
    ("font-weight", "pre", None, "body"),
    ("font-style", "pre", None, "body"),
    ("text-decoration", "pre", None, "body"),
    ("space-before", "pre", "15pt", None),
    ("space-after", "pre", None, "body"),
    ("text-align", "pre", None, "body"),
    ("start-indent", "pre", None, "body"),
    ("line-height", "pre", None, "body"),
    
    ("font-family", "codeblock", "monospace", None),
    ("font-size", "codeblock", None, "body"),
    ("color", "codeblock", None, "body"),
    ("background-color", "codeblock", "transparent", None),
    ("font-weight", "codeblock", None, "body"),
    ("font-style", "codeblock", None, "body"),
    ("text-decoration", "codeblock", None, "body"),
    ("space-before", "codeblock", "15pt", None),
    ("space-after", "codeblock", None, "body"),
    ("text-align", "codeblock", None, "body"),
    ("start-indent", "codeblock", "31pt", "body"),#+6pt
    ("line-height", "codeblock", None, "body"),
    
    ("font-family", "dl", None, "body"),
    ("font-size", "dl", None, "body"),
    ("color", "dl", None, "body"),
    ("background-color", "dl", None, "body"),
    ("font-weight", "dl", None, "body"),
    ("font-style", "dl", None, "body"),
    ("text-decoration", "dl", None, "body"),
    ("space-before", "dl", None, "body"),
    ("space-after", "dl", None, "body"),
    ("text-align", "dl", None, "body"),
    ("start-indent", "dl", None, "body"),
    ("line-height", "dl", None, "body"),
    # custom
    ("dl-type", "dl", "table", None),

    ("font-family", "ol", None, "body"),
    ("font-size", "ol", None, "body"),
    ("color", "ol", None, "body"),
    ("background-color", "ol", None, "body"),
    ("font-weight", "ol", None, "body"),
    ("font-style", "ol", None, "body"),
    ("text-decoration", "ol", None, "body"),
    ("space-before", "ol", None, "body"),
    ("space-after", "ol", None, "body"),
    ("text-align", "ol", None, "body"),
    ("start-indent", "ol", None, "body"),
    ("line-height", "ol", None, "body"),
    # custom
    ("ol-1", "ol", "1", None),
    ("ol-2", "ol", "1", None),
    ("ol-3", "ol", "1", None),
    ("ol-4", "ol", "1", None),
    ("ol-before-1", "ol", "", None),
    ("ol-before-2", "ol", "", None),
    ("ol-before-3", "ol", "", None),
    ("ol-before-4", "ol", "", None),
    ("ol-after-1", "ol", ". ", None),
    ("ol-after-2", "ol", ". ", None),
    ("ol-after-3", "ol", ". ", None),
    ("ol-after-4", "ol", ". ", None),
    ("ol-sublevel", "ol", "false", None),

    ("font-family", "ul", None, "body"),
    ("font-size", "ul", None, "body"),
    ("color", "ul", None, "body"),
    ("background-color", "ul", None, "body"),
    ("font-weight", "ul", None, "body"),
    ("font-style", "ul", None, "body"),
    ("text-decoration", "ul", None, "body"),
    ("space-before", "ul", None, "body"),
    ("space-after", "ul", None, "body"),
    ("text-align", "ul", None, "body"),
    ("start-indent", "ul", None, "body"),
    ("line-height", "ul", None, "body"),
    # custom
    ("ul-1", "ul", u"\u2022", None),
    ("ul-2", "ul", u"\u2022", None),
    ("ul-3", "ul", u"\u2022", None),
    ("ul-4", "ul", u"\u2022", None),
    
    ("font-family", "table", None, "body"),
    ("font-size", "table", None, "body"),
    ("color", "table", None, "body"),
    ("background-color", "table", None, "body"),
    ("font-weight", "table", None, "body"),
    ("font-style", "table", None, "body"),
    ("text-decoration", "table", None, "body"),
    ("space-before", "table", None, "body"),
    ("space-after", "table", None, "body"),
    ("text-align", "table", None, "body"),
    ("start-indent", "table", None, "body"),
    ("line-height", "table", None, "body"),
    # custom
    ("caption-number", "table", "document", None),
    ("caption-position", "table", "before", None),
    
    ("font-family", "fig", None, "body"),
    ("font-size", "fig", None, "body"),
    ("color", "fig", None, "body"),
    ("background-color", "fig", None, "body"),
    ("font-weight", "fig", None, "body"),
    ("font-style", "fig", None, "body"),
    ("text-decoration", "fig", None, "body"),
    ("space-before", "fig", None, "body"),
    ("space-after", "fig", None, "body"),
    ("text-align", "fig", None, "body"),
    ("start-indent", "fig", None, "body"),
    ("line-height", "fig", None, "body"),
    # custom
    ("caption-number", "fig", "document", None),
    ("caption-position", "fig", "after", None),
    
    ("font-family", "link", None, "body"),
    ("font-size", "link", None, "body"),
    ("color", "link", "blue", None),
    ("background-color", "link", "transparent", None),
    ("font-weight", "link", None, "body"),
    ("font-style", "link", None, "body"),
    ("text-decoration", "link", None, "body"),
    #("space-before", "link", None, None),
    #("space-after", "link", None, None),
    #("text-align", "link", None, None),
    #("start-indent", "link", None, None),
    ("line-height", "link", None, None),
    # custom
    ("link-page-number", "link", "true", None),
    ("link-url", "link", None, None)
    ]]

def default_style(type, property):
    for s in styles:
        if s["property"] == property and s["type"] == type:
            return s["value"]
    return None

fonts = {
    "Sans": {
        "default": ["Helvetica"],
        "Simplified Chinese": ["AdobeSongStd-Light"],
        "Japanese": ["KozMinProVI-Regular"],
        "Korean": ["AdobeMyungjoStd-Medium"],
        "Symbols": ["ZapfDingbats"],
        "SubmenuSymbol": ["ZapfDingbats"],
        "SymbolsSuperscript": ["Helvetica", "20%", "smaller"]
        },
    "Serif": {
        "default": ["Times"],
        "Simplified Chinese": ["AdobeSongStd-Light"],
        "Japanese": ["KozMinProVI-Regular"],
        "Korean": ["AdobeMyungjoStd-Medium"],
        "Symbols": ["ZapfDingbats"],
        "SubmenuSymbol": ["ZapfDingbats"],
        "SymbolsSuperscript": ["Times", "20%", "smaller"]
        },
    "Monospaced": {
        "default": ["Courier"],
        "Simplified Chinese": ["AdobeSongStd-Light"],
        "Japanese": ["KozMinProVI-Regular"],
        "Korean": ["AdobeMyungjoStd-Medium"],
        "Symbols": ["ZapfDingbats"],
        "SymbolsSuperscript": ["Courier", "20%", "smaller"]
        }
    }

imports = {
    "ah": [
        "plugin:org.dita.pdf2:cfg/fo/attrs/tables-attr_axf.xsl", 
        "plugin:org.dita.pdf2:cfg/fo/attrs/toc-attr_axf.xsl", 
        "plugin:org.dita.pdf2:cfg/fo/attrs/index-attr_axf.xsl",
        "plugin:org.dita.pdf2:xsl/fo/root-processing_axf.xsl", 
        "plugin:org.dita.pdf2:xsl/fo/index_axf.xsl"],
    "fop": [
        "plugin:org.dita.pdf2:cfg/fo/attrs/commons-attr_fop.xsl", 
        "plugin:org.dita.pdf2:cfg/fo/attrs/tables-attr_fop.xsl", 
        "plugin:org.dita.pdf2:cfg/fo/attrs/toc-attr_fop.xsl",
        "plugin:org.dita.pdf2:xsl/fo/root-processing_fop.xsl", 
        "plugin:org.dita.pdf2:xsl/fo/index_fop.xsl"],
    "xep": [
        "plugin:org.dita.pdf2:cfg/fo/attrs/commons-attr_xep.xsl", 
        "plugin:org.dita.pdf2:cfg/fo/attrs/layout-masters-attr_xep.xsl", 
        "plugin:org.dita.pdf2:xsl/fo/root-processing_xep.xsl", 
        "plugin:org.dita.pdf2:xsl/fo/index_xep.xsl"]
    }

langs = {
  u"de": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Abbildung: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabelle: <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>Anhang:&#xA0;</variable>"
  },
  u"en": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Figure: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Table: <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>Appendix:&#xA0;</variable>"
  },
  u"es": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Figura: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabla: <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>Ap&#xe9;ndice:&#xA0;</variable>"
  },
  u"fi": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Kuva. <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Taulu. <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>Liite </variable>"
  },
  u"fr": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Illustration: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Table: <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>Annexe&#xA0;:&#xA0;</variable>"
  },
  u"he": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>&#x5d0;&#x5d9;&#x5d5;&#x5e8;. <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>&#x5d8;&#x5d1;&#x5dc;&#x5d4;. <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>&#x5e0;&#x5e1;&#x5e4;&#x5d7; </variable>"
  },
  u"it": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'> Figura: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabella: <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>Appendice:&#xA0;</variable>"
  },
  u"ja": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>&#x56f3; : <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>&#x8868; : <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>&#x4ed8;&#x9332; : </variable>"
  },
  u"nl": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Figuur: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabel: <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>Bijlage:&#xA0;</variable>"
  },
  u"ro": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Fig. <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabel. <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>Anexa </variable>"
  },
  u"ru": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>&#x420;&#x438;&#x441;&#x443;&#x43d;&#x43e;&#x43a;. <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>&#x422;&#x430;&#x431;&#x43b;&#x438;&#x446;&#x430;. <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>&#x41f;&#x440;&#x438;&#x43b;&#x43e;&#x436;&#x435;&#x43d;&#x438;&#x435; </variable>"
  },
  u"sl": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Slika: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabela: <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>Kazalo dodatka:&#xA0;</variable>"
  },
  u"sv": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Figur. <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabell. <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>Appendix </variable>"
  },
  u"zh_CN": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>&#x56fe;: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>&#x8868;: <param ref-name='title'/></variable>",
    #u"Chapter with number": u"<variable id='Chapter with number'></variable>",
    u"Table of Contents Chapter": u"<variable id='Table of Contents Chapter'></variable>",
    u"Table of Contents Appendix": u"<variable id='Table of Contents Appendix'>&#x9644;&#x5f55;:&#xA0;</variable>"
  }
} 

class StylePluginGenerator(DitaGenerator):
    """Generator for a DITA-OT style plug-in."""

    variable_languages = ["de", "en", "es", "fi", "fr", "he", "it", "ja", "nl", "ro", "ru", "sv", "zh_CN"]

    def __init__(self):
        DitaGenerator.__init__(self)
        self.ot_version = None
        self.transtype = None
        self.plugin_name = None
        self.plugin_version = None
        self.page_size = ()
        self.style = {}
        self.page_margins = None
        self.force_page_count = None
        self.chapter_layout = None
        self.body_column_count = None
        self.index_column_count = None
        self.bookmark_style = None
        self.toc_maximum_level = None
        self.task_label = None
        self.include_related_links = None
        self.column_gap = None
        self.mirror_page_margins = None
        self.table_continued = None
        self.formatter = None
        self.override_shell = False
        self.cover_image = None
        self.cover_image_name = None
        self.cover_image_metadata = None
        self.cover_image_topic = None
        self.header = {
            "odd": ["pagenum"],
            "even": ["pagenum"]
            }
        self.footer = {
            "odd": [],
            "even": []
            }
        self.page_number = None
            
    def __get_ns(self):
        return {
            "xsl": "http://www.w3.org/1999/XSL/Transform",
            "fo": "http://www.w3.org/1999/XSL/Format",
            "xs": "http://www.w3.org/2001/XMLSchema",
            "e": self.plugin_name,
            "ditaarch": "http://dita.oasis-open.org/architecture/2005/",
            "opentopic": "http://www.idiominc.com/opentopic",
            "opentopic-func": "http://www.idiominc.com/opentopic/exsl/function"
            }

    def _preprocess(self):
        """Preprocess arguments."""
        if self._initialized == False:
            DitaGenerator._preprocess(self)
            self._initialized = True

    def __generate_integrator(self):
        """Generate plugin integrator Ant file."""
        __root = ET.Element("project", {
            "name": self.plugin_name,
            })
        __init = ET.SubElement(__root, "target", {
            "name": ("dita2%s.init" % self.transtype)
            })
        ET.SubElement(__init, "property", {
            "name": "customization.dir",
            "location": ("${dita.plugin.%s.dir}/cfg" % self.plugin_name)
            })
        if self.override_shell:
            ET.SubElement(__init, "property", {
                "name": "args.xsl.pdf",
                "location": ("${dita.plugin.%s.dir}/xsl/fo/topic2fo_shell_%s.xsl" % (self.plugin_name, self.formatter))
                })
        if self.chapter_layout:
            ET.SubElement(__init, "property", {
                "name": "args.chapter.layout",
                "value": self.chapter_layout
                })
        if self.bookmark_style:
            ET.SubElement(__init, "property", {
                "name": "args.bookmark.style",
                "value": self.bookmark_style
                })
        if self.task_label:
            __t = ""
            ET.SubElement(__init, "property", {
                "name": "args.gen.task.lbl",
                "value": str(self.task_label)
                })
        if self.include_related_links:
            ET.SubElement(__init, "property", {
                "name": "args.fo.include.rellinks",
                "value": self.include_related_links
                })
        ET.SubElement(__root, "target", {
            "name": "dita2%s" % self.transtype,
            "depends": ("dita2%s.init, dita2pdf2" % self.transtype),
            })
        ditagen.generator.indent(__root)
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def __generate_plugin_file(self):
        """Generate plugin configuration file."""
        __root = ET.Element("plugin", id=self.plugin_name)
        if self.plugin_version:
            ET.SubElement(__root, "feature", extension="package.version", value=self.plugin_version)
        ET.SubElement(__root, "require", plugin="org.dita.pdf2")
        ET.SubElement(__root, "feature", extension="dita.conductor.transtype.check", value=self.transtype)
        ET.SubElement(__root, "feature", extension="dita.transtype.print", value=self.transtype)
        ET.SubElement(__root, "feature", extension="dita.conductor.target.relative", file="integrator.xml")
        ditagen.generator.indent(__root)
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def __generate_catalog(self):
        """Generate plugin configuration file."""
        __root = ET.Element("catalog", prefer="system")
        ET.SubElement(__root, "uri", name="cfg:fo/attrs/custom.xsl", uri="fo/attrs/custom.xsl")
        ET.SubElement(__root, "uri", name="cfg:fo/xsl/custom.xsl", uri="fo/xsl/custom.xsl")
        ditagen.generator.indent(__root)
        ditagen.generator.set_prefixes(__root, {"": "urn:oasis:names:tc:entity:xmlns:xml:catalog"})
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    @staticmethod
    def copy_xml(__root, __raw):
        for __c in list(ET.fromstring("""
<xsl:stylesheet xmlns:fo="http://www.w3.org/1999/XSL/Format"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:e="e"
                xmlns:opentopic="http://www.idiominc.com/opentopic"
                xmlns:opentopic-func="http://www.idiominc.com/opentopic/exsl/function"
                exclude-result-prefixes="e opentopic opentopic-func"
                version="2.0">%s</xsl:stylesheet>""" % __raw)):
             __root.append(__c)

    def __generate_custom(self, stylesheet=None):
        """Generate plugin custom XSLT file."""
        __root = ET.Element(NS_XSL + "stylesheet", {"version":"2.0", "exclude-result-prefixes": "ditaarch opentopic e"})
        
        __cover_metadata_raw = """
  <xsl:template name="e:cover-image">
    <xsl:for-each select="($map//*[contains(@class, ' topic/data ')][@name = '%s']/*[contains(@class, ' topic/image ')])[1]">
      <xsl:apply-templates select="." mode="placeImage">
        <xsl:with-param name="imageAlign" select="@align"/>
        <xsl:with-param name="href" select="if (@scope = 'external' or opentopic-func:isAbsolute(@href)) then @href else concat($input.dir.url, @href)"/>
        <xsl:with-param name="height" select="@height"/>
        <xsl:with-param name="width" select="@width"/>
      </xsl:apply-templates>
    </xsl:for-each>
  </xsl:template>
"""
        # Backport from DITA-OT 2.0
        __cover_metadata_v1_raw = """
  <!-- Test whether URI is absolute -->
  <xsl:function name="opentopic-func:isAbsolute" as="xs:boolean">
    <xsl:param name="uri" as="xs:anyURI"/>
    <xsl:sequence select="some $prefix in ('/', 'file:') satisfies starts-with($uri, $prefix) or
                          contains($uri, '://')"/>
  </xsl:function>
"""
        __cover_topic_raw = """
  <xsl:template name="e:cover-image">
    <xsl:for-each select="($map//*[contains(@class, ' map/topicref ')][@outputclass = '%s'])[1]">
      <xsl:apply-templates select="key('id', @id)/*[contains(@class, ' topic/body ')]/node()"/>
    </xsl:for-each>
  </xsl:template>
"""
        __cover_file_raw = """
  <xsl:template name="e:cover-image">
    <xsl:variable name="path">
      <xsl:call-template name="insertVariable">
        <xsl:with-param name="theVariableID" select="'cover-image-path'"/>
      </xsl:call-template>
    </xsl:variable>
    <xsl:apply-templates select="." mode="placeImage">
      <xsl:with-param name="imageAlign" select="'center'"/>
      <xsl:with-param name="href" select="concat($artworkPrefix, $path)"/>
      <xsl:with-param name="height" select="()"/>
      <xsl:with-param name="width" select="()"/>
    </xsl:apply-templates>
  </xsl:template>
"""
        # Backport from DITA-OT 2.0
        __cover_raw = """
  <xsl:template name="createFrontMatter_1.0">
    <fo:page-sequence master-reference="front-matter" xsl:use-attribute-sets="__force__page__count">
      <xsl:call-template name="insertFrontMatterStaticContents"/>
      <fo:flow flow-name="xsl-region-body">
        <fo:block xsl:use-attribute-sets="__frontmatter">
          <xsl:call-template name="createFrontCoverContents"/>
        </fo:block>
      </fo:flow>
    </fo:page-sequence>
    <xsl:if test="not($retain-bookmap-order)">
      <xsl:call-template name="createNotices"/>
    </xsl:if>
  </xsl:template>
"""
        __cover_contents_raw = """
  <xsl:template name="createFrontCoverContents">
    <!-- set the title -->
    <fo:block xsl:use-attribute-sets="__frontmatter__title">
      <xsl:choose>
        <xsl:when test="$map/*[contains(@class,' topic/title ')][1]">
          <xsl:apply-templates select="$map/*[contains(@class,' topic/title ')][1]"/>
        </xsl:when>
        <xsl:when test="$map//*[contains(@class,' bookmap/mainbooktitle ')][1]">
          <xsl:apply-templates select="$map//*[contains(@class,' bookmap/mainbooktitle ')][1]"/>
        </xsl:when>
        <xsl:when test="//*[contains(@class, ' map/map ')]/@title">
          <xsl:value-of select="//*[contains(@class, ' map/map ')]/@title"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="/descendant::*[contains(@class, ' topic/topic ')][1]/*[contains(@class, ' topic/title ')]"/>
        </xsl:otherwise>
      </xsl:choose>
    </fo:block>
    <!-- set the subtitle -->
    <xsl:apply-templates select="$map//*[contains(@class,' bookmap/booktitlealt ')]"/>
    <fo:block xsl:use-attribute-sets="__frontmatter__owner">
      <xsl:apply-templates select="$map//*[contains(@class,' bookmap/bookmeta ')]"/>
    </fo:block>
    <!-- cover image -->
    <fo:block xsl:use-attribute-sets="image__block">
      <xsl:call-template name="e:cover-image"/>
    </fo:block>
  </xsl:template>
"""

        __table_footer_raw = """
  <xsl:template match="*[contains(@class, ' topic/tbody ')]" name="topic.tbody">
    <fo:table-footer xsl:use-attribute-sets="tgroup.tfoot">
      <fo:table-row>
        <fo:table-cell number-columns-spanned="{../@cols}"/>
      </fo:table-row>
    </fo:table-footer>
    <fo:table-body xsl:use-attribute-sets="tgroup.tbody">
      <xsl:call-template name="commonattributes"/>
      <xsl:apply-templates/>
    </fo:table-body>
  </xsl:template>
"""
        __table_continued_raw = """
  <xsl:variable name="table.frame-default" select="'all'"/>
                
  <xsl:template match="*[contains(@class, ' topic/tbody ')]" name="topic.tbody">
    <fo:table-footer xsl:use-attribute-sets="tgroup.tfoot table__tableframe__top">
      <fo:retrieve-table-marker retrieve-class-name="e:continued" retrieve-position-within-table="last-ending" retrieve-boundary-within-table="table-fragment"/>
    </fo:table-footer>
    <fo:table-body xsl:use-attribute-sets="tgroup.tbody">
      <xsl:call-template name="commonattributes"/>
      <fo:marker marker-class-name="e:continued">
        <fo:table-row>
          <fo:table-cell xsl:use-attribute-sets="e:tfoot.row.entry.continued" number-columns-spanned="{../@cols}">
            <xsl:variable name="frame">
              <xsl:choose>
                <xsl:when test="../../@frame">
                  <xsl:value-of select="../../@frame"/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:value-of select="$table.frame-default"/>
                </xsl:otherwise>
              </xsl:choose>
            </xsl:variable>
            <xsl:if test="$frame = 'all' or $frame = 'topbot' or $frame = 'bottom'">
              <xsl:call-template name="processAttrSetReflection">
                <xsl:with-param name="attrSet" select="'__tableframe__top'"/>
                <xsl:with-param name="path" select="$tableAttrs"/>
              </xsl:call-template>
            </xsl:if>
            <fo:block>
              <xsl:call-template name="insertVariable">
                <xsl:with-param name="theVariableID" select="'#table-continued'"/>
              </xsl:call-template>
            </fo:block>
          </fo:table-cell>
        </fo:table-row>
      </fo:marker>
      <xsl:apply-templates/>
    </fo:table-body>
  </xsl:template>
  
  <xsl:template match="*[contains(@class, ' topic/tbody ')]/*[contains(@class, ' topic/row ')]" name="topic.tbody_row">
    <fo:table-row xsl:use-attribute-sets="tbody.row">
      <xsl:call-template name="commonattributes"/>
      <xsl:if test="not(following-sibling::*)">
        <fo:marker marker-class-name="e:continued"/>
      </xsl:if>
      <xsl:apply-templates/>
    </fo:table-row>
  </xsl:template>
"""
        __dl_list_raw = """
  <xsl:template match="*[contains(@class, ' topic/dl ')]">
    <fo:list-block xsl:use-attribute-sets="ul e:dl">
      <xsl:call-template name="commonattributes"/>
      <xsl:apply-templates select="*[contains(@class, ' topic/dlentry ')]"/>
    </fo:list-block>
  </xsl:template>

  <xsl:template match="*[contains(@class, ' topic/dlentry ')]">
    <fo:list-item xsl:use-attribute-sets="ul.li">
      <fo:list-item-label xsl:use-attribute-sets="ul.li__label">
        <fo:block xsl:use-attribute-sets="ul.li__label__content">
          <xsl:call-template name="commonattributes"/>
          <xsl:call-template name="insertVariable">
            <xsl:with-param name="theVariableID" select="'Unordered List bullet'"/>
          </xsl:call-template>
        </fo:block>
      </fo:list-item-label>
      <fo:list-item-body xsl:use-attribute-sets="ul.li__body">
        <fo:block xsl:use-attribute-sets="ul.li__content">
          <xsl:apply-templates select="*[contains(@class, ' topic/dt ')]"/>
          <xsl:apply-templates select="*[contains(@class, ' topic/dd ')]"/>
        </fo:block>
      </fo:list-item-body>
    </fo:list-item>
  </xsl:template>

  <xsl:template match="*[contains(@class, ' topic/dt ')]">
    <fo:block xsl:use-attribute-sets="e:dlentry.dt__content">
      <xsl:apply-templates/>
    </fo:block>
  </xsl:template>

  <xsl:template match="*[contains(@class, ' topic/dd ')]">
    <fo:block xsl:use-attribute-sets="e:dlentry.dd__content">
      <xsl:apply-templates/>
    </fo:block>
  </xsl:template>
"""
        __dl_html_raw = """
  <xsl:template match="*[contains(@class, ' topic/dl ')]">
    <fo:block xsl:use-attribute-sets="e:dl">
      <xsl:call-template name="commonattributes" />
      <xsl:apply-templates select="*[contains(@class, ' topic/dlentry ')]" />
    </fo:block>
  </xsl:template>
  
  <xsl:template match="*[contains(@class, ' topic/dlentry ')]">
      <fo:block>
          <xsl:apply-templates select="*[contains(@class, ' topic/dt ')]" />
          <xsl:apply-templates select="*[contains(@class, ' topic/dd ')]" />
      </fo:block>
  </xsl:template>
  
  <xsl:template match="*[contains(@class, ' topic/dt ')]">
    <fo:block xsl:use-attribute-sets="e:dlentry.dt__content">
      <xsl:apply-templates />
    </fo:block>
  </xsl:template>
  
  <xsl:template match="*[contains(@class, ' topic/dd ')]">
    <fo:block xsl:use-attribute-sets="e:dlentry.dd__content">
      <xsl:apply-templates />
    </fo:block>
  </xsl:template>
"""   
        __get_title_raw = """
  <xsl:template match="*" mode="getTitle">
    <xsl:variable name="topic" select="ancestor-or-self::*[contains(@class, ' topic/topic ')][1]"/>
    <xsl:variable name="id" select="$topic/@id"/>
    <xsl:variable name="mapTopics" select="key('map-id', $id)"/>
    <fo:inline>
      <xsl:for-each select="$mapTopics[1]">
        <xsl:variable name="depth" select="count(ancestor-or-self::*[contains(@class, ' map/topicref')])"/>
        <xsl:choose>
          <xsl:when test="parent::opentopic:map and contains(@class, ' bookmap/bookmap ')"/>
          <xsl:when test="ancestor-or-self::*[contains(@class, ' bookmap/frontmatter ') or
                                              contains(@class, ' bookmap/backmatter ')]"/>
          <xsl:when test="ancestor-or-self::*[contains(@class, ' bookmap/appendix ')] and
                          $e:number-levels[$depth]">
            <xsl:number count="*[contains(@class, ' map/topicref ')]
                                [ancestor-or-self::*[contains(@class, ' bookmap/appendix ')]] "
                        level="multiple"
                        format="A.1.1"/>
          </xsl:when>
          <xsl:when test="$e:number-levels[$depth]">
            <xsl:number count="*[contains(@class, ' map/topicref ')]
                                [not(ancestor-or-self::*[contains(@class, ' bookmap/frontmatter ')])]"
                        level="multiple"
                        format="1.1"/>
          </xsl:when>
        </xsl:choose>
      </xsl:for-each>
    </fo:inline>
    <xsl:text> </xsl:text>
    <xsl:apply-templates/>
  </xsl:template>
"""
        __numberless_chapter_raw = """
<xsl:template name="insertChapterFirstpageStaticContent">
    <xsl:param name="type"/>
    <fo:block>
        <xsl:attribute name="id">
            <xsl:call-template name="generate-toc-id"/>
        </xsl:attribute>
        <xsl:choose>
            <xsl:when test="$type = 'chapter'">
                <fo:block xsl:use-attribute-sets="__chapter__frontmatter__name__container">
                    <xsl:call-template name="insertVariable">
                        <xsl:with-param name="theVariableID" select="'Chapter with number'"/>
                        <xsl:with-param name="theParameters">
                            <number>
                                <!--fo:block xsl:use-attribute-sets="__chapter__frontmatter__number__container">
                                    <xsl:apply-templates select="key('map-id', @id)[1]" mode="topicTitleNumber"/>
                                </fo:block-->
                            </number>
                        </xsl:with-param>
                    </xsl:call-template>
                </fo:block>
            </xsl:when>
            <xsl:when test="$type = 'appendix'">
                <fo:block xsl:use-attribute-sets="__chapter__frontmatter__name__container">
                    <xsl:call-template name="insertVariable">
                        <xsl:with-param name="theVariableID" select="'Appendix with number'"/>
                        <xsl:with-param name="theParameters">
                            <number>
                                <!--fo:block xsl:use-attribute-sets="__chapter__frontmatter__number__container">
                                    <xsl:apply-templates select="key('map-id', @id)[1]" mode="topicTitleNumber"/>
                                </fo:block-->
                            </number>
                        </xsl:with-param>
                    </xsl:call-template>
                </fo:block>
            </xsl:when>
            <xsl:when test="$type = 'appendices'">
                <fo:block xsl:use-attribute-sets="__chapter__frontmatter__name__container">
                  <xsl:call-template name="insertVariable">
                    <xsl:with-param name="theVariableID" select="'Appendix with number'"/>
                    <xsl:with-param name="theParameters">
                      <number>
                        <fo:block xsl:use-attribute-sets="__chapter__frontmatter__number__container">
                          <xsl:text>&#xA0;</xsl:text>
                        </fo:block>
                      </number>
                    </xsl:with-param>
                  </xsl:call-template>
                </fo:block>
            </xsl:when>
            <xsl:when test="$type = 'part'">
                <fo:block xsl:use-attribute-sets="__chapter__frontmatter__name__container">
                    <xsl:call-template name="insertVariable">
                        <xsl:with-param name="theVariableID" select="'Part with number'"/>
                        <xsl:with-param name="theParameters">
                            <number>
                                <fo:block xsl:use-attribute-sets="__chapter__frontmatter__number__container">
                                    <xsl:apply-templates select="key('map-id', @id)[1]" mode="topicTitleNumber"/>
                                </fo:block>
                            </number>
                        </xsl:with-param>
                    </xsl:call-template>
                </fo:block>
            </xsl:when>
            <xsl:when test="$type = 'preface'">
                <fo:block xsl:use-attribute-sets="__chapter__frontmatter__name__container">
                    <xsl:call-template name="insertVariable">
                        <xsl:with-param name="theVariableID" select="'Preface title'"/>
                    </xsl:call-template>
                </fo:block>
            </xsl:when>
            <xsl:when test="$type = 'notices'">
                <fo:block xsl:use-attribute-sets="__chapter__frontmatter__name__container">
                    <xsl:call-template name="insertVariable">
                        <xsl:with-param name="theVariableID" select="'Notices title'"/>
                    </xsl:call-template>
                </fo:block>
            </xsl:when>
        </xsl:choose>
    </fo:block>
</xsl:template>
"""
        if stylesheet == "front-matter" or not stylesheet:
            if self.cover_image_name or self.cover_image_metadata or self.cover_image_topic:
                __root.append(ET.Comment("cover"))
                if self.ot_version < Version("2.0"):
                    self.copy_xml(__root, __cover_raw)
                self.copy_xml(__root, __cover_contents_raw)
                if self.cover_image_name:
                    self.copy_xml(__root, __cover_file_raw)
                elif self.cover_image_metadata:
                    self.copy_xml(__root, __cover_metadata_raw % self.cover_image_metadata)
                    if self.ot_version < Version("2.0"):
                        self.copy_xml(__root, __cover_metadata_v1_raw)
                elif self.cover_image_topic:
                    self.copy_xml(__root, __cover_topic_raw % self.cover_image_topic)
        
        __table_title_raw = """
<xsl:template match="*[contains(@class, ' topic/table ')]">
    <xsl:variable name="scale">
        <xsl:call-template name="getTableScale"/>
    </xsl:variable>
    <fo:block xsl:use-attribute-sets="table">
        <xsl:call-template name="commonattributes"/>
        <xsl:if test="not(@id)">
          <xsl:attribute name="id">
            <xsl:call-template name="get-id"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="not($scale = '')">
            <xsl:attribute name="font-size"><xsl:value-of select="concat($scale, '%')"/></xsl:attribute>
        </xsl:if>
        <xsl:apply-templates select="*[contains(@class, ' topic/tgroup ')]"/>
        <xsl:apply-templates select="*[contains(@class, ' topic/title ') or contains(@class, ' topic/desc ')]"/>
    </fo:block>
</xsl:template>"""

        if stylesheet == "tables" or not stylesheet:
            __root.append(ET.Comment("table"))
            if "table" in self.style and "caption-position" in self.style["table"] and self.style["table"]["caption-position"] == "after":
                self.copy_xml(__root, __table_title_raw)
            if self.table_continued:
                self.copy_xml(__root, __table_continued_raw)
            else:
                self.copy_xml(__root, __table_footer_raw)

            if "dl-type" in self.style["dl"]:
                if self.style["dl"]["dl-type"] == "list":
                    __root.append(ET.Comment("dl"))
                    self.copy_xml(__root, __dl_list_raw)
                elif self.style["dl"]["dl-type"] == "html":
                    __root.append(ET.Comment("dl"))
                    self.copy_xml(__root, __dl_html_raw)

        __note_raw = """
  <xsl:template match="*[contains(@class,' topic/note ')]">
    <fo:table xsl:use-attribute-sets="note__table">
      <fo:table-column xsl:use-attribute-sets="note__text__column"/>
      <fo:table-body>
        <fo:table-row>
          <fo:table-cell xsl:use-attribute-sets="note__text__entry">
            <xsl:apply-templates select="." mode="placeNoteContent"/>
          </fo:table-cell>
        </fo:table-row>
      </fo:table-body>
    </fo:table>
  </xsl:template>
"""
        __chapter_page_number_raw = """
<xsl:template name="startPageNumbering">
  <xsl:variable name="topicType" as="xs:string">
    <xsl:call-template name="determineTopicType"/>
  </xsl:variable>
  <xsl:variable name="topic" select="ancestor-or-self::*[contains(@class, ' topic/topic ')][1]"/>
  <xsl:variable name="id" select="$topic/@id"/>
  <xsl:variable name="mapTopics" select="key('map-id', $id)"/>  
  <xsl:for-each select="$mapTopics[1]">
    <xsl:choose>
      <xsl:when test="$topicType = 'topicChapter'">
        <xsl:attribute name="initial-page-number">1</xsl:attribute>
        <fo:folio-prefix>
          <xsl:number format="1" count="*[contains(@class, ' bookmap/chapter ')]"/>
          <xsl:text>&#x2014;</xsl:text>
        </fo:folio-prefix>
      </xsl:when>
      <xsl:when test="$topicType = ('topicAppendix', 'topicAppendices')">
        <xsl:attribute name="initial-page-number">1</xsl:attribute>
        <fo:folio-prefix>
          <xsl:number format="A" count="*[contains(@class, ' bookmap/appendix ')]"/>
          <xsl:text>&#x2014;</xsl:text>
        </fo:folio-prefix>
      </xsl:when>
    </xsl:choose>
  </xsl:for-each>
  <xsl:comment>topicType: <xsl:value-of select="$topicType"/></xsl:comment>
</xsl:template>
"""
        __figure_raw = """
<xsl:template match="*[contains(@class,' topic/fig ')]">
    <fo:block xsl:use-attribute-sets="fig">
        <xsl:call-template name="commonattributes"/>
        <xsl:if test="not(@id)">
          <xsl:attribute name="id">
            <xsl:call-template name="get-id"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:apply-templates/>
    </fo:block>
</xsl:template>
"""

        if stylesheet == "commons" or not stylesheet:
            __root.append(ET.Comment("title numbering"))
            __number_levels = [s in self.style and "title-numbering" in self.style[s] and self.style[s]["title-numbering"] == "true" for s in ['topic', 'topic.topic', 'topic.topic.topic', 'topic.topic.topic.topic']]
            ET.SubElement(__root, NS_XSL + "variable", name=u"e:number-levels", select="(" + ", ".join([str(l).lower() + "()" for l in __number_levels]) + ")")
            self.copy_xml(__root, __get_title_raw)
            if "title-numbering" in self.style["topic"] and self.style["topic"]["title-numbering"] != "true":
                self.copy_xml(__root, __numberless_chapter_raw)

            if not ("icon" in self.style["note"] and self.style["note"]["icon"] == "icon"):
                __root.append(ET.Comment("note"))
                self.copy_xml(__root, __note_raw)
            if self.page_number:
                if self.page_number == "chapter-page":
                    self.copy_xml(__root, __chapter_page_number_raw)
            if "fig" in self.style and "caption-position" in self.style["fig"] and self.style["fig"]["caption-position"] == "before":
                self.copy_xml(__root, __figure_raw)
            if self.cover_image_topic:
                ET.SubElement(__root, NS_XSL + "template", match="*[contains(@class, ' topic/topic ')][@outputclass = '%s']" % self.cover_image_topic, priority="1000")

        __link_raw = """
  <xsl:template match="*[contains(@class,' topic/xref ')]" name="topic.xref">
    <fo:inline>
      <xsl:call-template name="commonattributes"/>
    </fo:inline>
    <xsl:variable name="destination" select="opentopic-func:getDestinationId(@href)"/>
    <xsl:variable name="element" select="key('key_anchor',$destination)[1]"/>
    <xsl:variable name="referenceTitle">
      <xsl:apply-templates select="." mode="insertReferenceTitle">
        <xsl:with-param name="href" select="@href"/>
        <xsl:with-param name="titlePrefix" select="''"/>
        <xsl:with-param name="destination" select="$destination"/>
        <xsl:with-param name="element" select="$element"/>
      </xsl:apply-templates>
    </xsl:variable>
    <fo:basic-link xsl:use-attribute-sets="xref">
      <xsl:call-template name="buildBasicLinkDestination">
        <xsl:with-param name="scope" select="@scope"/>
        <xsl:with-param name="format" select="@format"/>
        <xsl:with-param name="href" select="@href"/>
      </xsl:call-template>
      <xsl:choose>
        <xsl:when test="not(@scope = 'external' or @format = 'html') and not($referenceTitle = '')">
          <xsl:copy-of select="$referenceTitle"/>
        </xsl:when>
        <xsl:when test="not(@scope = 'external' or @format = 'html')">
          <xsl:call-template name="insertPageNumberCitation">
            <xsl:with-param name="isTitleEmpty" select="'yes'"/>
            <xsl:with-param name="destination" select="$destination"/>
            <xsl:with-param name="element" select="$element"/>
          </xsl:call-template>
        </xsl:when>
        <xsl:otherwise>
          <xsl:choose>
            <xsl:when test="exists(*[not(contains(@class,' topic/desc '))] | text()) and
                            exists(processing-instruction()[name()='ditaot'][.='usertext'])">
              <xsl:apply-templates select="*[not(contains(@class,' topic/desc '))] | text()"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="e:format-link-url(@href)"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:otherwise>
      </xsl:choose>
    </fo:basic-link>
    <xsl:if test="not(@scope = 'external' or @format = 'html') and not($referenceTitle = '') and not($element[contains(@class, ' topic/fn ')])">
      <xsl:if test="not(processing-instruction()[name()='ditaot'][.='usertext'])">
        <xsl:call-template name="insertPageNumberCitation">
          <xsl:with-param name="destination" select="$destination"/>
          <xsl:with-param name="element" select="$element"/>
        </xsl:call-template>
      </xsl:if>
    </xsl:if>
    <xsl:if test="@scope = 'external' and exists(processing-instruction()[name()='ditaot'][.='usertext'])">
      <xsl:text> at </xsl:text>
      <xsl:value-of select="e:format-link-url(@href)"/>
    </xsl:if>
  </xsl:template>
  
  <xsl:function name="e:format-link-url">
    <xsl:param name="href"/>
    <xsl:variable name="h" select="if (starts-with($href, 'http://')) then substring($href, 8) else $href"/>
    <xsl:value-of select="if (contains($h, '/') and substring-after($h, '/') = '') then substring($h, 0, string-length($h)) else $h"/>
  </xsl:function>
"""

        if stylesheet == "links" or not stylesheet:
            if "link-url" in self.style["link"] and self.style["link"]["link-url"] == "true":
                __root.append(ET.Comment("link"))
                self.copy_xml(__root, __link_raw)

        __list_raw = """
<xsl:template match="*[contains(@class, ' topic/ul ')]/*[contains(@class, ' topic/li ')]">
    <xsl:variable name="depth" select="count(ancestor::*[contains(@class, ' topic/ul ')])"/>
    <fo:list-item xsl:use-attribute-sets="ul.li">
        <fo:list-item-label xsl:use-attribute-sets="ul.li__label">
            <fo:block xsl:use-attribute-sets="ul.li__label__content">
                <fo:inline>
                    <xsl:call-template name="commonattributes"/>
                </fo:inline>
                <xsl:call-template name="insertVariable">
                    <xsl:with-param name="theVariableID" select="concat('Unordered List bullet ', $depth)"/>
                </xsl:call-template>
            </fo:block>
        </fo:list-item-label>
        <fo:list-item-body xsl:use-attribute-sets="ul.li__body">
            <fo:block xsl:use-attribute-sets="ul.li__content">
                <xsl:apply-templates/>
            </fo:block>
        </fo:list-item-body>
    </fo:list-item>
</xsl:template>

<xsl:template match="*[contains(@class, ' topic/ol ')]/*[contains(@class, ' topic/li ')]">
    <xsl:variable name="depth" select="count(ancestor::*[contains(@class, ' topic/ol ')])"/>
    <xsl:variable name="format">
        <xsl:call-template name="insertVariable">
            <xsl:with-param name="theVariableID" select="concat('Ordered List Format ', $depth)"/>
        </xsl:call-template>
    </xsl:variable>
    <fo:list-item xsl:use-attribute-sets="ol.li">
        <fo:list-item-label xsl:use-attribute-sets="ol.li__label">
            <fo:block xsl:use-attribute-sets="ol.li__label__content">
                <fo:inline>
                    <xsl:call-template name="commonattributes"/>
                </fo:inline>
                <xsl:call-template name="insertVariable">
                    <xsl:with-param name="theVariableID" select="concat('Ordered List Number ', $depth)"/>
                    <xsl:with-param name="theParameters">
                        <number>
                            <xsl:number format="{$format}"/>
                        </number>
                    </xsl:with-param>
                </xsl:call-template>
            </fo:block>
        </fo:list-item-label>
        <fo:list-item-body xsl:use-attribute-sets="ol.li__body">
            <fo:block xsl:use-attribute-sets="ol.li__content">
                <xsl:apply-templates/>
            </fo:block>
        </fo:list-item-body>
    </fo:list-item>
</xsl:template>
"""

        if stylesheet == "lists" or not stylesheet:
            if "ol" in self.style or "ul" in self.style:
                __root.append(ET.Comment("list"))
                self.copy_xml(__root, __list_raw)

        if not stylesheet:
            if not self.override_shell and self.toc_maximum_level:
                __root.append(ET.Comment("TOC"))
                ET.SubElement(__root, NS_XSL + "variable", name=u"tocMaximumLevel").text = str(self.toc_maximum_level)
        
        ditagen.generator.indent(__root)
        ditagen.generator.set_prefixes(__root, self.__get_ns())
        
        __d = ET.ElementTree(__root)
        __d.write(self.out, "ASCII")#"UTF-8"

    def __attribute_set(self, __root, __style, __attribute_set, __include=properties):
        """Generate attribute set."""
        __attrs = ET.SubElement(__root, NS_XSL + "attribute-set", name=__attribute_set)
        for k, v in self.style[__style].items():
            if k in __include:
                ET.SubElement(__attrs, NS_XSL + "attribute", name=k).text = v


    def __generate_custom_attr(self, stylesheet=None):
        """Generate plugin custom XSLT file."""
        __root = ET.Element(NS_XSL + "stylesheet", {"version":"2.0", "exclude-result-prefixes": "xs ditaarch opentopic e"})
        
        #if stylesheet == "front-matter-attr" or not stylesheet:
            #if self.cover_image_name:
            #    ET.SubElement(__root, NS_XSL + "variable", name="e:cover-image-path", select="concat($artworkPrefix, 'Customization/OpenTopic/common/artwork/%s'" % self.cover_image_name)
            #el
            #if self.cover_image_metadata:
                #__cover_image_path = ET.SubElement(__root, NS_XSL + "variable", name="e:cover-image-path", select="($map//*[contains(@class, ' topic/data ')][@name = '%s'])[1]/@href" % self.cover_image_metadata)
            #    __cover_image_path = ET.SubElement(__root, NS_XSL + "variable", name="e:cover-image")
            #    ET.SubElement(__cover_image_path, NS_XSL + "apply-templates", select="($map//*[contains(@class, ' topic/data ')][@name = '%s']/*[contains(@class, ' topic/image ')])[1]" % self.cover_image_metadata, mode="e:cover-image")
        
        if stylesheet == "commons-attr" or not stylesheet:
            # force page count
            if self.force_page_count:
                __page_count_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name="__force__page__count")
                ET.SubElement(__page_count_attr, NS_XSL + "attribute", name=u"force-page-count").text = self.force_page_count
        
            # font family
            self.__attribute_set(__root, "body", "__fo__root", ["font-family", "color", "text-align"])
            # titles
            for (k, e) in self.style.items():
                if k.startswith("topic") or k.startswith("section"):
                    __title_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=k + ".title")
                    for (p, v) in e.items():
                        if p in properties:
                            ET.SubElement(__title_attr, NS_XSL + "attribute", name=p).text = v
            # link
            link_attr_sets = ["common.link"]
            for n in link_attr_sets:
                self.__attribute_set(__root, "link", n)
    
            # normal block
            spacing_attr_sets = ["common.block"]
            for n in spacing_attr_sets:
                self.__attribute_set(__root, "body", n, properties.difference(["start-indent"]))

            # note
            self.__attribute_set(__root, "note", "note__table")
            if not ("icon" in self.style["note"] and self.style["note"]["icon"] == "icon"):
                __note_text = ET.SubElement(__root, NS_XSL + "attribute-set", name=u"note__text__column")
                ET.SubElement(__note_text, NS_XSL + "attribute", name="column-number").text = "1"

            # pre
            self.__attribute_set(__root, "pre", "pre")
            
            # fig
            self.__attribute_set(__root, "fig", "fig")
        
        if stylesheet == "tables-attr" or not stylesheet:
            # dl
            if "dl-type" in self.style["dl"]:
                self.__attribute_set(__root, "dl", "e:dl")
                __dt_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name="e:dlentry.dt__content")
                ET.SubElement(__dt_attr, NS_XSL + "attribute", name=u"font-weight").text = "bold"
                ET.SubElement(__dt_attr, NS_XSL + "attribute", name=u"keep-with-next").text = "always"
                __dd_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name="e:dlentry.dd__content")
                if self.style["dl"]["dl-type"] == "html":
                    ET.SubElement(__dd_attr, NS_XSL + "attribute", name=u"start-indent").text = "from-parent(start-indent) + 5mm"
            # table continued
            if self.table_continued:
                __table_continued_attr = ET.SubElement(__root, NS_XSL + "attribute-set", { "name": "e:tfoot.row.entry.continued" })
                ET.SubElement(__table_continued_attr, NS_XSL + "attribute", name=u"border-right-style").text = "hidden"
                ET.SubElement(__table_continued_attr, NS_XSL + "attribute", name=u"border-left-style").text = "hidden"
                ET.SubElement(__table_continued_attr, NS_XSL + "attribute", name=u"text-align").text = "end"
                ET.SubElement(__table_continued_attr, NS_XSL + "attribute", name=u"font-style").text = "italic"
            # table
            self.__attribute_set(__root, "table", "table.tgroup")
            __thead_row_entry_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=u"thead.row.entry")
            ET.SubElement(__thead_row_entry_attr, NS_XSL + "attribute", name="background-color").text = "inherit"
        
        if stylesheet == "layout-masters-attr" or not stylesheet:
            # page column count
            if self.body_column_count:
                for a in ["region-body.odd", "region-body.even"]:
                    __region_body_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=a)
                    ET.SubElement(__region_body_attr, NS_XSL + "attribute", name=u"column-count").text = str(self.body_column_count)
                    if self.column_gap:
                        ET.SubElement(__region_body_attr, NS_XSL + "attribute", name=u"column-gap").text = self.column_gap
                for a in ["region-body__frontmatter.odd", "region-body__frontmatter.even"]:
                    __region_body_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=a)
                    ET.SubElement(__region_body_attr, NS_XSL + "attribute", name=u"column-count").text = "1"
                if self.index_column_count:
                    for a in ["region-body__index.odd", "region-body__index.even"]:
                        __region_body_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=a)
                        ET.SubElement(__region_body_attr, NS_XSL + "attribute", name=u"column-count").text = str(self.index_column_count)
        
        if stylesheet == "basic-settings" or not stylesheet:       
            # page size
            if self.page_size:
                ET.SubElement(__root, NS_XSL + "variable", name=u"page-width").text = self.page_size[0]
                ET.SubElement(__root, NS_XSL + "variable", name=u"page-height").text = self.page_size[1]
            # mirror pages
            if self.mirror_page_margins:
                ET.SubElement(__root, NS_XSL + "variable", name=u"mirror-page-margins", select=u"true()")
            # page margins
            for k, v in self.page_margins.iteritems():
                if v:
                    ET.SubElement(__root, NS_XSL + "variable", name="page-margin-" + k).text = v
            # font size
            if "font-size" in self.style["body"]:
                ET.SubElement(__root, NS_XSL + "variable", name=u"default-font-size").text = self.style["body"]["font-size"]
            # line height
            if "line-height" in self.style["body"]:
                ET.SubElement(__root, NS_XSL + "variable", name=u"default-line-height").text = self.style["body"]["line-height"]
            # body indent
            if "start-indent" in self.style["body"]:
                ET.SubElement(__root, NS_XSL + "variable", name=u"side-col-width").text = self.style["body"]["start-indent"]
        
        __list_raw = """
  <xsl:attribute-set name="ol">
    <xsl:attribute name="provisional-distance-between-starts">
      <xsl:call-template name="e:list-label-length"/>
      <xsl:text>em * 0.7</xsl:text>
    </xsl:attribute>
  </xsl:attribute-set>

  <xsl:template name="e:list-label-length">
    <xsl:variable name="labels" as="xs:integer*">
      <xsl:variable name="depth" select="count(ancestor-or-self::*[contains(@class, ' topic/ol ')])" />
      <xsl:variable name="format" as="xs:string">
        <xsl:call-template name="insertVariable">
          <xsl:with-param name="theVariableID" select="concat('Ordered List Format ', $depth)" />
        </xsl:call-template>
      </xsl:variable>
      <xsl:for-each select="*[contains(@class, ' topic/li ')]">
        <xsl:variable name="s">
          <xsl:call-template name="insertVariable">
            <xsl:with-param name="theVariableID" select="concat('Ordered List Number ', $depth)" />
            <xsl:with-param name="theParameters">
              <number>
                <xsl:number format="{$format}" />
              </number>
            </xsl:with-param>
          </xsl:call-template>
        </xsl:variable>
        <xsl:sequence select="string-length(normalize-space($s))"/>
      </xsl:for-each>
    </xsl:variable>
    <xsl:sequence select="max($labels)"/>
  </xsl:template>
"""

        if stylesheet == "lists-attr" or not stylesheet:
            __root.append(ET.Comment("list"))
            self.copy_xml(__root, __list_raw)

        if stylesheet == "pr-domain-attr" or not stylesheet:
            # codeblock
            __pre_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=u"codeblock")
            for k, v in self.style["codeblock"].items():
                ET.SubElement(__pre_attr, NS_XSL + "attribute", name=k).text = v
        
        ditagen.generator.indent(__root)
        ditagen.generator.set_prefixes(__root, self.__get_ns())
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def __generate_shell(self):
        __root = ET.Element(NS_XSL + "stylesheet", {"version":"2.0", "exclude-result-prefixes": "ditaarch opentopic e"})
        
        __root.append(ET.Comment("base imports"))
        fs = []
        fs.append("plugin:org.dita.base:xsl/common/dita-utilities.xsl")
        fs.append("plugin:org.dita.base:xsl/common/dita-textonly.xsl")
        
        fs.append("plugin:org.dita.pdf2:xsl/common/attr-set-reflection.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/common/vars.xsl")
        
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/basic-settings.xsl")
        if self.override_shell:
            fs.append("plugin:%s:cfg/fo/attrs/basic-settings.xsl" % (self.plugin_name))
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/layout-masters-attr.xsl")
        if self.override_shell:
            fs.append("plugin:%s:cfg/fo/attrs/layout-masters-attr.xsl" % (self.plugin_name))
        fs.append("plugin:org.dita.pdf2:cfg/fo/layout-masters.xsl")
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/links-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/links.xsl")
        if self.override_shell:
            fs.append("plugin:%s:xsl/fo/links.xsl" % (self.plugin_name))
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/lists-attr.xsl")
        if self.override_shell:
            fs.append("plugin:%s:cfg/fo/attrs/lists-attr.xsl" % (self.plugin_name))
        fs.append("plugin:org.dita.pdf2:xsl/fo/lists.xsl")
        if self.override_shell:
            fs.append("plugin:%s:xsl/fo/lists.xsl" % (self.plugin_name))
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/tables-attr.xsl")
        if self.override_shell:
            fs.append("plugin:%s:cfg/fo/attrs/tables-attr.xsl" % (self.plugin_name))
        fs.append("plugin:org.dita.pdf2:xsl/fo/tables.xsl")
        if self.override_shell:
            fs.append("plugin:%s:xsl/fo/tables.xsl" % (self.plugin_name))
        fs.append("plugin:org.dita.pdf2:xsl/fo/root-processing.xsl")
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/commons-attr.xsl")
        if self.override_shell:
            fs.append("plugin:%s:cfg/fo/attrs/commons-attr.xsl" % (self.plugin_name))
        fs.append("plugin:org.dita.pdf2:xsl/fo/commons.xsl")
        if self.override_shell:
            fs.append("plugin:%s:xsl/fo/commons.xsl" % (self.plugin_name))
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/toc-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/toc.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/bookmarks.xsl")
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/index-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/index.xsl")
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/front-matter-attr.xsl")
        if self.override_shell:
            fs.append("plugin:%s:cfg/fo/attrs/front-matter-attr.xsl" % (self.plugin_name))
        fs.append("plugin:org.dita.pdf2:xsl/fo/front-matter.xsl")
        if self.override_shell:
            fs.append("plugin:%s:xsl/fo/front-matter.xsl" % (self.plugin_name))
        fs.append("plugin:org.dita.pdf2:xsl/fo/preface.xsl")
        
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/map-elements-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/map-elements.xsl")
        
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/task-elements-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/task-elements.xsl")
        
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/reference-elements-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/reference-elements.xsl")
        
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/sw-domain-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/sw-domain.xsl")
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/pr-domain-attr.xsl")
        if self.override_shell:
            fs.append("plugin:%s:cfg/fo/attrs/pr-domain-attr.xsl" % (self.plugin_name))
        fs.append("plugin:org.dita.pdf2:xsl/fo/pr-domain.xsl")
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/hi-domain-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/hi-domain.xsl")
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/ui-domain-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/ui-domain.xsl")
        
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/static-content-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/static-content.xsl")
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/glossary-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/glossary.xsl")
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/lot-lof-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/lot-lof.xsl")
        
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/learning-elements-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/learning-elements.xsl")
        
        fs.append("plugin:org.dita.pdf2:xsl/fo/flagging.xsl")

        for i in fs:
            ET.SubElement(__root, "xsl:import", href=i)
            
        __root.append(ET.Comment("formatter specific imports"))
        for i in imports[self.formatter]:
            ET.SubElement(__root, "xsl:import", href=i)
        
        if not self.override_shell:
            __root.append(ET.Comment("configuration overrides"))
            for i in ["cfg:fo/attrs/custom.xsl", "cfg:fo/xsl/custom.xsl"]:
                ET.SubElement(__root, "xsl:import", href=i)
        
        __root.append(ET.Comment("parameters"))
        ET.SubElement(__root, "xsl:param", name="locale")
        ET.SubElement(__root, "xsl:param", name="customizationDir.url")
        ET.SubElement(__root, "xsl:param", name="artworkPrefix")
        ET.SubElement(__root, "xsl:param", name="publishRequiredCleanup")
        ET.SubElement(__root, "xsl:param", name="DRAFT")
        ET.SubElement(__root, "xsl:param", name="output.dir.url")
        ET.SubElement(__root, "xsl:param", name="work.dir.url")
        ET.SubElement(__root, "xsl:param", name="input.dir.url")
        ET.SubElement(__root, "xsl:param", name="disableRelatedLinks", select="'yes'")
        ET.SubElement(__root, "xsl:param", name="pdfFormatter", select="'%s'" % self.formatter)
        ET.SubElement(__root, "xsl:param", name="antArgsBookmarkStyle")
        ET.SubElement(__root, "xsl:param", name="antArgsChapterLayout")
        ET.SubElement(__root, "xsl:param", name="antArgsIncludeRelatedLinks")
        ET.SubElement(__root, "xsl:param", name="include.rellinks")
        ET.SubElement(__root, "xsl:param", name="antArgsGenerateTaskLabels")
        ET.SubElement(__root, "xsl:param", name="tocMaximumLevel", select=str(self.toc_maximum_level))
        ET.SubElement(__root, "xsl:param", name="ditaVersion", select="number(/*[contains(@class,' map/map ')]/@ditaarch:DITAArchVersion)")
        
        ditagen.generator.indent(__root)
        ditagen.generator.set_prefixes(__root, self.__get_ns())
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def __generate_font_mappings(self):
        """Generate font mapping file."""
        __root = ET.Element(u"font-mappings")
        __table = ET.SubElement(__root, u"font-table")
        for k, v in self.fonts.iteritems():
            __logical = ET.SubElement(__table, u"logical-font", name=k)
            for pk, pv in v.iteritems():
                __physical = ET.SubElement(__logical, u"physical-font", { "char-set": pk })
                ET.SubElement(__physical, u"font-face").text = pv[0]
                if len(pv) > 1:
                    ET.SubElement(__physical, u"baseline-shift").text = pv[1]
                if len(pv) > 2:
                    ET.SubElement(__physical, u"override-size").text = pv[2]
        ditagen.generator.indent(__root)
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    __headers = ["Body first header",
                 "Body odd header",
                 "Body even header",
                 "Preface odd header",
                 "Preface even header",
                 "Preface first header",
                 "Toc odd header",
                 "Toc even header",
                 "Index odd header",
                 "Index even header",
                 "Glossary odd header",
                 "Glossary even header"]
    __footers = ["Body odd footer",
                 "Body even footer",
                 "Body first footer",
                 "Preface odd footer",
                 "Preface even footer",
                 "Preface first footer",
                 "Toc odd footer",
                 "Toc even footer",
                 "Index odd footer",
                 "Index even footer",
                 "Glossary odd footer",
                 "Glossary even footer"]
    
    def __generate_vars(self, lang):
        """Generate variable file."""
        __root = ET.Element(u"vars")
        
        # page number reference
        if not ("link-page-number" in self.style["link"] and self.style["link"]["link-page-number"] == "true"):
            ET.SubElement(__root, u"variable", id=u"On the page")
        # table continued
        if self.table_continued:
            __root.append(ET.fromstring(langs[lang][u"#table-continued"]))
        # table caption numbering
        if "caption-number" in self.style["table"] and self.style["table"]["caption-number"] == "none":
            __root.append(ET.fromstring(langs[lang][u"Table"]))
        # figure caption numbering
        if "caption-number" in self.style["fig"] and self.style["fig"]["caption-number"] == "none":
            __root.append(ET.fromstring(langs[lang][u"Figure"]))
        # chapter numbering
        if "title-numbering" in self.style["topic"] and self.style["topic"]["title-numbering"] != "true":
        #    __root.append(ET.fromstring(langs[lang]["Chapter with number"]))
            __root.append(ET.fromstring(langs[lang]["Table of Contents Chapter"]))
            __root.append(ET.fromstring(langs[lang]["Table of Contents Appendix"]))
        # cover image
        if self.cover_image_name:
            ET.SubElement(__root, "variable", id="cover-image-path").text = "Customization/OpenTopic/common/artwork/%s" % self.cover_image_name
        # static content
        for args, var_names in [(self.header, self.__headers), (self.footer, self.__footers)]:
            for id in var_names: 
                vars = []
                if "even" in id:
                    vars = args["even"]
                else:
                    vars = args["odd"]
                f = ET.SubElement(__root, u"variable", id=id)
                i = 1
                for v in vars:
                    e = ET.Element(u"param", { "ref-name": v })
                    if i < len(vars):
                        e.tail = " | "
                    f.append(e)
                    i = i + 1
        for level in range(1, 5):
            v = "ol-%s" % level
            var = ET.SubElement(__root, "variable", id="Ordered List Number %d" %level)
            if "ol" in self.style and "ol-before-%d" % level in self.style["ol"]:
                var.text = self.style["ol"]["ol-before-%s" %level]
            else:
                var.text = default_style("ol", "ol-before-%d" % level)
            p = ET.SubElement(var, u"param", { "ref-name": "number" })
            if "ol" in self.style and "ol-after-%d" % level in self.style["ol"]:
                p.tail = self.style["ol"]["ol-after-%d" % level]
            else:
                p.tail = default_style("ol", "ol-after-%d" % level)
        for level in range(1, 5):
            v = "ol-%d" % level
            var = ET.SubElement(__root, "variable", id="Ordered List Format %d" %level)
            if "ol" in self.style and "ol-%d" % level in self.style["ol"]:
                var.text = self.style["ol"]["ol-%s" %level]
            else:
                var.text = default_style("ol", "ol-%d" % level)
        for level in range(1, 5):
            v = "ul-%d" % level
            var = ET.SubElement(__root, "variable", id="Unordered List bullet %d" %level)
            if "ul" in self.style and "ul-%d" % level in self.style["ul"]:
                var.text = self.style["ul"]["ul-%s" %level]
            else:
                var.text = default_style("ul", "ul-%d" % level)

        ditagen.generator.indent(__root, max=1)
        ditagen.generator.set_prefixes(__root, {"": "http://www.idiominc.com/opentopic/vars"})
        __d = ET.ElementTree(__root)
        # Write output in ASCII because ZIP writer will re-encode into UTF-8
        __d.write(self.out, "ASCII")

    def generate_plugin(self):
        """Generate ZIP file with specified stylesheets."""
        self._preprocess()

        __output = self.out

        __temp = StringIO.StringIO()
        __failed = False
        try:
            __zip = ZipFile(__temp, "w")
            __zip.debug = 3
            try:
                # integrator
                self._run_generation(__zip, self.__generate_integrator,
                                    "%s/integrator.xml" % (self.plugin_name))
                # plugin
                self._run_generation(__zip, self.__generate_plugin_file,
                                    "%s/plugin.xml" % (self.plugin_name))
                # catalog
                self._run_generation(__zip, self.__generate_catalog,
                                    "%s/cfg/catalog.xml" % (self.plugin_name))
                # font-mappings
#                self._run_generation(__zip, self.__generate_font_mappings,
#                                    "%s/cfg/fo/font-mappins.xml" % (self.plugin_name))
                
                # custom XSLT
                if self.override_shell:
                    for s in ["front-matter", "commons", "tables", "links", "lists"]:
                        self._run_generation(__zip, lambda: self.__generate_custom(s),
                                            "%s/xsl/fo/%s.xsl" % (self.plugin_name, s))
                else:
                    self._run_generation(__zip, self.__generate_custom,
                                        "%s/cfg/fo/xsl/custom.xsl" % (self.plugin_name))
                # custom XSLT attribute sets
                if self.override_shell:
                    for s in ["front-matter-attr", "commons-attr", "layout-masters-attr", "tables-attr", "basic-settings", "lists-attr", "pr-domain-attr"]:
                        self._run_generation(__zip, lambda: self.__generate_custom_attr(s),
                                            "%s/cfg/fo/attrs/%s.xsl" % (self.plugin_name, s))
                else:
                    self._run_generation(__zip, self.__generate_custom_attr,
                                        "%s/cfg/fo/attrs/custom.xsl" % (self.plugin_name))
                
                # shell XSLT
                if self.override_shell:
                    self._run_generation(__zip, self.__generate_shell,
                                        "%s/xsl/fo/topic2fo_shell_%s.xsl" % (self.plugin_name, self.formatter))
                for lang in self.variable_languages:
                    self._run_generation(__zip, lambda: self.__generate_vars(lang),
                                         "%s/cfg/common/vars/%s.xml" % (self.plugin_name, lang))
                if self.cover_image:
                    self._store_file(__zip, self.cover_image,
                                      "%s/cfg/common/artwork/%s" % (self.plugin_name, self.cover_image_name))
            except:
                __failed = True
                raise Exception("Failed to write plugin", sys.exc_info()[1]), None, sys.exc_info()[2]
            finally:
                if __zip != None:
                    __zip.close()
            if not __failed:
                __output.write(__temp.getvalue())
        except:
            __failed = True
            raise Exception("Failed to write ZIP file to output", sys.exc_info()[1]), None, sys.exc_info()[2]
        finally:
            __temp.close()
    
    def _store_file(self, __zip, __file, filename):
        """Run a file generation."""
        __dt = datetime.now()
        __zipinfo = ZipInfo(filename.encode("UTF-8"), (__dt.year, __dt.month, __dt.day, __dt.hour, __dt.minute, __dt.second))
        __zipinfo.external_attr = 0755 << 16L # give full access to included file
        try:
            __zip.writestr(__zipinfo, __file)
        except:
            raise Exception("Failed to write " + filename, sys.exc_info()[1]), None, sys.exc_info()[2]            
