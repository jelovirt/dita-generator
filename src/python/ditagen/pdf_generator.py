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

NS_XSL = "{http://www.w3.org/1999/XSL/Transform}"
NS_FO = "{http://www.w3.org/1999/XSL/Format}"

styles = [{ "property": f[0], "type": f[1], "value": f[2], "inherit": f[3] } for f in [
    ("font-family", "body", "serif", False),
    ("font-size", "body", "10pt", False),
    ("color", "body", "black", False),
    ("font-weight", "body", "normal", False),
    ("font-style", "body", "normal", False),
    ("text-decoration", "body", "none", False),
    ("space-before", "body", "6pt", False),
    ("space-after", "body", "6pt", False),
    ("text-align", "body", "start", False),
    ("start-indent", "body", "25pt", False),
    
    ("font-family", "topic", "sans-serif", False),
    ("font-size", "topic", "18pt", False),
    ("color", "topic", "black", True),
    ("font-weight", "topic", "bold", False),
    ("font-style", "topic", "normal", False),
    ("text-decoration", "topic", "none", True),
    ("space-before", "topic", "0pt", False),
    ("space-after", "topic", "16.8pt", False),
    ("text-align", "topic", "start", False),
    ("start-indent", "topic", "0pt", False),
    
    ("font-family", "topic.topic", "sans-serif", False),
    ("font-size", "topic.topic", "14pt", False),
    ("color", "topic.topic", "black", True),
    ("font-weight", "topic.topic", "bold", False),
    ("font-style", "topic.topic", "normal", False),
    ("text-decoration", "topic.topic", "none", True),
    ("space-before", "topic.topic", "12pt", False),
    ("space-after", "topic.topic", "5pt", False),
    ("text-align", "topic.topic", "start", False),
    ("start-indent", "topic.topic", "0pt", False),
    
    ("font-family", "topic.topic.topic", "sans-serif", False),
    ("font-size", "topic.topic.topic", "12pt", False),
    ("color", "topic.topic.topic", "black", True),
    ("font-weight", "topic.topic.topic", "bold", False),
    ("font-style", "topic.topic.topic", "normal", False),
    ("text-decoration", "topic.topic.topic", "none", True),
    ("space-before", "topic.topic.topic", "12pt", False),
    ("space-after", "topic.topic.topic", "2pt", False),
    ("text-align", "topic.topic.topic", "start", False),
    ("start-indent", "topic.topic.topic", "0pt", False),
    
    ("font-family", "topic.topic.topic.topic", "serif", True),
    ("font-size", "topic.topic.topic.topic", "10pt", True),
    ("color", "topic.topic.topic.topic", "black", True),
    ("font-weight", "topic.topic.topic.topic", "bold", False),
    ("font-style", "topic.topic.topic.topic", "normal", False),
    ("text-decoration", "topic.topic.topic.topic", "none", True),
    ("space-before", "topic.topic.topic.topic", "12pt", False),
    ("space-after", "topic.topic.topic.topic", "0pt", False),
    ("text-align", "topic.topic.topic.topic", "start", False),
    ("start-indent", "topic.topic.topic.topic", None, True),

    ("font-family", "section", "sans-serif", False),
    ("font-size", "section", None, True),
    ("color", "section", None, True),
    ("font-weight", "section", None, True),
    ("font-style", "section", None, True),
    ("text-decoration", "section", None, True),
    ("space-before", "section", "15pt", False),
    ("space-after", "section", None, True),
    ("text-align", "section", None, True),
    ("start-indent", "section", None, True),
    
    ("font-family", "note", None, True),
    ("font-size", "note", None, True),
    ("color", "note", None, True),
    ("font-weight", "note", None, True),
    ("font-style", "note", None, True),
    ("text-decoration", "note", None, True),
    ("space-before", "note", None, True),
    ("space-after", "note", None, True),
    ("text-align", "note", None, True),
    ("start-indent", "note", None, True),
    
    ("font-family", "pre", "monospace", False),
    ("font-size", "pre", None, True),
    ("color", "pre", None, True),
    ("font-weight", "pre", None, True),
    ("font-style", "pre", None, True),
    ("text-decoration", "pre", None, True),
    ("space-before", "pre", "15pt", False),
    ("space-after", "pre", None, True),
    ("text-align", "pre", None, True),
    ("start-indent", "pre", None, True),
    
    
    ("font-family", "link", None, True),
    ("font-size", "link", None, True),
    ("color", "link", "blue", False),
    ("font-weight", "link", None, True),
    ("font-style", "link", None, True),
    ("text-decoration", "link", None, True),
    ("space-before", "link", None, False),
    ("space-after", "link", None, False),
    ("text-align", "link", None, False),
    ("start-indent", "link", None, False)
    ]]

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
        self.dl = None
        self.title_numbering = None
        self.generate_shell = None
        self.link_pagenumber = None
        self.table_continued = None
        self.formatter = None
        self.override_shell = False
        self.header = {
            "odd": ["pagenum"],
            "even": ["pagenum"]
            }
        self.footer = {
            "odd": [],
            "even": []
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
                "value": self.task_label
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

    def __generate_custom(self):
        """Generate plugin custom XSLT file."""
        __root = ET.Element(NS_XSL + "stylesheet", {"version":"2.0", "exclude-result-prefixes": "e opentopic"})
        
        __dl_list_raw = """
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                xmlns:e="e"
                exclude-result-prefixes="e"
                version="2.0">

  <xsl:template match="*[contains(@class, ' topic/dl ')]">
    <fo:list-block xsl:use-attribute-sets="ul">
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

</xsl:stylesheet>
"""
        __dl_html_raw = """
<xsl:stylesheet  xmlns:e="e"
                 xmlns:fo="http://www.w3.org/1999/XSL/Format"
                 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                 exclude-result-prefixes="e"
                 version="2.0">
  
  <xsl:template match="*[contains(@class, &apos; topic/dl &apos;)]">
    <fo:block>
      <xsl:call-template name="commonattributes" />
      <xsl:apply-templates select="*[contains(@class, &apos; topic/dlentry &apos;)]" />
    </fo:block>
  </xsl:template>
  
  <xsl:template match="*[contains(@class, &apos; topic/dlentry &apos;)]">
      <fo:block>
          <xsl:apply-templates select="*[contains(@class, &apos; topic/dt &apos;)]" />
          <xsl:apply-templates select="*[contains(@class, &apos; topic/dd &apos;)]" />
      </fo:block>
  </xsl:template>
  
  <xsl:template match="*[contains(@class, &apos; topic/dt &apos;)]">
    <fo:block xsl:use-attribute-sets="e:dlentry.dt__content">
      <xsl:apply-templates />
    </fo:block>
  </xsl:template>
  
  <xsl:template match="*[contains(@class, &apos; topic/dd &apos;)]">
    <fo:block xsl:use-attribute-sets="e:dlentry.dd__content">
      <xsl:apply-templates />
    </fo:block>
  </xsl:template>

</xsl:stylesheet>
"""
        __dl_raw = None
        if self.dl == "list":
            __dl_raw = __dl_list_raw
        elif self.dl == "html":
            __dl_raw = __dl_html_raw
        if __dl_raw:
            __root.append(ET.Comment("dl"))
            __dl = ET.fromstring(__dl_raw)
            for __c in list(__dl):
                __root.append(__c)
   
        __get_title_raw = """
<xsl:stylesheet xmlns:fo="http://www.w3.org/1999/XSL/Format"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:e="e"
                xmlns:opentopic="http://www.idiominc.com/opentopic"
                exclude-result-prefixes="e opentopic"
                version="2.0">
  
  <xsl:template match="*" mode="getTitle">
    <xsl:variable name="topic" select="ancestor-or-self::*[contains(@class, ' topic/topic ')][1]"/>
    <xsl:variable name="id" select="$topic/@id"/>
    <xsl:variable name="mapTopics" select="key('map-id', $id)"/>
    <fo:inline>
      <xsl:for-each select="$mapTopics[1]">
        <xsl:choose>
          <xsl:when test="parent::opentopic:map"/>
          <xsl:when test="ancestor-or-self::*[contains(@class, ' bookmap/frontmatter ') or
                                              contains(@class, ' bookmap/backmatter ')]"/>
          <xsl:when test="ancestor-or-self::*[contains(@class, ' bookmap/appendix ')]">
            <xsl:number count="*[contains(@class, ' map/topicref ')]
                                [ancestor-or-self::*[contains(@class, ' bookmap/appendix ')]]"
                        level="multiple"
                        format="A.1.1"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:number count="*[contains(@class, ' map/topicref ')]
                                [not(ancestor-or-self::*[contains(@class, ' bookmap/frontmatter ')])]"
                        level="multiple"
                        format="1.1"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>
    </fo:inline>
    <xsl:text> </xsl:text>
    <xsl:apply-templates/>
  </xsl:template>
  
</xsl:stylesheet>
"""
        if self.title_numbering:
            __root.append(ET.Comment("title numbering"))
            for __c in list(ET.fromstring(__get_title_raw)):
                __root.append(__c)
        
        __table_footer_raw = """
<xsl:stylesheet xmlns:fo="http://www.w3.org/1999/XSL/Format"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:e="e"
                exclude-result-prefixes="e"
                version="2.0">
                
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
                
</xsl:stylesheet>
"""
        __table_continued_raw = """
<xsl:stylesheet xmlns:fo="http://www.w3.org/1999/XSL/Format"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:e="e"
                exclude-result-prefixes="e"
                version="2.0">
                
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
                
</xsl:stylesheet>
"""
        __root.append(ET.Comment("table"))
        __table_raw = __table_footer_raw
        if self.table_continued:
            __table_raw = __table_continued_raw
        for __c in list(ET.fromstring(__table_raw)):
            __root.append(__c)
        
        ditagen.generator.indent(__root)
        ditagen.generator.set_prefixes(__root, {"xsl": "http://www.w3.org/1999/XSL/Transform", "fo": "http://www.w3.org/1999/XSL/Format", "e": self.plugin_name, "opentopic": "http://www.idiominc.com/opentopic"})
        
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def __generate_custom_attr(self):
        """Generate plugin custom XSLT file."""
        __root = ET.Element(NS_XSL + "stylesheet", {"version":"2.0", "exclude-result-prefixes": "e"})
        
        __root_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name="__fo__root")
        # font family
        for p in ["font-family", "color", "text-align"]:
            if p in self.style["body"]:
                ET.SubElement(__root_attr, NS_XSL + "attribute", name=p).text = self.style["body"][p]
        # titles
        for (k, e) in self.style.items():
            if k.startswith("topic") or k.startswith("section"):
                __title_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=k + ".title")
                for (p, v) in e.items():
                    ET.SubElement(__title_attr, NS_XSL + "attribute", name=p).text = v
        # link
        link_attr_sets = ["common.link"]
        for n in link_attr_sets:
            __link_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=n)
            for k, v in self.style["link"].items():
                ET.SubElement(__link_attr, NS_XSL + "attribute", name=k).text = v
#            if self.link_color:
#                ET.SubElement(__link_attr, NS_XSL + "attribute", name=u"color").text = self.link_color
#            if self.link_font_weight:
#                ET.SubElement(__link_attr, NS_XSL + "attribute", name=u"font-weight").text = self.link_font_weight
#            if self.link_font_style:
#                ET.SubElement(__link_attr, NS_XSL + "attribute", name=u"font-style").text = self.link_font_style
#            if self.link_text_decoration:
#                ET.SubElement(__link_attr, NS_XSL + "attribute", name=u"text-decoration").text = self.link_text_decoration

        # normal block
        spacing_attr_sets = ["common.block"]
        for n in spacing_attr_sets:
            __spacing_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=n)
            for k, v in self.style["body"].items():
                if k != "start-indent":
                    ET.SubElement(__spacing_attr, NS_XSL + "attribute", name=k).text = v

        # note
        __note_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=u"note__table")
        for k, v in self.style["note"].items():
            ET.SubElement(__note_attr, NS_XSL + "attribute", name=k).text = v
            
        # pre
        __pre_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=u"pre")
        for k, v in self.style["pre"].items():
            ET.SubElement(__note_attr, NS_XSL + "attribute", name=k).text = v

        # dl
        if self.dl:
            __dt_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name="e:dlentry.dt__content")
            ET.SubElement(__dt_attr, NS_XSL + "attribute", name=u"font-weight").text = "bold"
            ET.SubElement(__dt_attr, NS_XSL + "attribute", name=u"keep-with-next").text = "always"
            __dd_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name="e:dlentry.dd__content")
            if self.dl == "html":
                ET.SubElement(__dd_attr, NS_XSL + "attribute", name=u"start-indent").text = "from-parent(start-indent) + 5mm"

        # page column count
        if self.body_column_count:
            for a in ["region-body.odd", "region-body.even"]:
                __region_body_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=a)
                ET.SubElement(__region_body_attr, NS_XSL + "attribute", name=u"column-count").text = self.body_column_count
                if self.column_gap:
                    ET.SubElement(__region_body_attr, NS_XSL + "attribute", name=u"column-gap").text = self.column_gap
            for a in ["region-body__frontmatter.odd", "region-body__frontmatter.even"]:
                __region_body_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=a)
                ET.SubElement(__region_body_attr, NS_XSL + "attribute", name=u"column-count").text = "1"
            if self.index_column_count:
                for a in ["region-body__index.odd", "region-body__index.even"]:
                    __region_body_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=a)
                    ET.SubElement(__region_body_attr, NS_XSL + "attribute", name=u"column-count").text = self.index_column_count
                

        # force page count
        if self.force_page_count:
            __page_count_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name="__force__page__count")
            ET.SubElement(__page_count_attr, NS_XSL + "attribute", name=u"force-page-count").text = self.force_page_count
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
                ET.SubElement(__root, NS_XSL + "variable", name=k).text = v
        # font size
        if "font-size" in self.style["body"]:
            ET.SubElement(__root, NS_XSL + "variable", name=u"default-font-size").text = self.style["body"]["font-size"]
        # body indent
        if "start-indent" in self.style["body"]:
            ET.SubElement(__root, NS_XSL + "variable", name=u"side-col-width").text = self.style["body"]["start-indent"]
        # toc
        if not self.override_shell and self.toc_maximum_level:
            ET.SubElement(__root, NS_XSL + "variable", name=u"tocMaximumLevel").text = self.toc_maximum_level
        # table continued
        if self.table_continued:
            __table_continued_attr = ET.SubElement(__root, NS_XSL + "attribute-set", { "name": "e:tfoot.row.entry.continued" })
            ET.SubElement(__table_continued_attr, NS_XSL + "attribute", name=u"border-right-style").text = "hidden"
            ET.SubElement(__table_continued_attr, NS_XSL + "attribute", name=u"border-left-style").text = "hidden"
            ET.SubElement(__table_continued_attr, NS_XSL + "attribute", name=u"text-align").text = "end"
            ET.SubElement(__table_continued_attr, NS_XSL + "attribute", name=u"font-style").text = "italic"
        
        ditagen.generator.indent(__root)
        ditagen.generator.set_prefixes(__root, {"xsl": "http://www.w3.org/1999/XSL/Transform", "fo": "http://www.w3.org/1999/XSL/Format", "e": self.plugin_name})
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def __generate_shell(self):
        __root = ET.Element(NS_XSL + "stylesheet", {
            "version":"2.0",
            "exclude-result-prefixes": "ditaarch e",
            })
        
        __root.append(ET.Comment("base imports"))
        for i in [
                  "plugin:org.dita.base:xsl/common/dita-utilities.xsl",
                  "plugin:org.dita.base:xsl/common/dita-textonly.xsl",
        
                  "plugin:org.dita.pdf2:xsl/common/attr-set-reflection.xsl",
                  "plugin:org.dita.pdf2:xsl/common/vars.xsl",
        
                  "plugin:org.dita.pdf2:cfg/fo/attrs/basic-settings.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/layout-masters-attr.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/layout-masters.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/links-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/links.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/lists-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/lists.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/tables-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/tables.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/root-processing.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/commons-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/commons.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/toc-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/toc.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/bookmarks.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/index-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/index.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/front-matter-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/front-matter.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/preface.xsl",
            
                  "plugin:org.dita.pdf2:cfg/fo/attrs/map-elements-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/map-elements.xsl",
            
                  "plugin:org.dita.pdf2:cfg/fo/attrs/task-elements-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/task-elements.xsl",
            
                  "plugin:org.dita.pdf2:cfg/fo/attrs/reference-elements-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/reference-elements.xsl",
            
                  "plugin:org.dita.pdf2:cfg/fo/attrs/sw-domain-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/sw-domain.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/pr-domain-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/pr-domain.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/hi-domain-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/hi-domain.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/ui-domain-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/ui-domain.xsl",
            
                  "plugin:org.dita.pdf2:cfg/fo/attrs/static-content-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/static-content.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/glossary-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/glossary.xsl",
                  "plugin:org.dita.pdf2:cfg/fo/attrs/lot-lof-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/lot-lof.xsl",
            
                  "plugin:org.dita.pdf2:cfg/fo/attrs/learning-elements-attr.xsl",
                  "plugin:org.dita.pdf2:xsl/fo/learning-elements.xsl",
            
                  "plugin:org.dita.pdf2:xsl/fo/flagging.xsl"]:
            ET.SubElement(__root, "xsl:import", href=i)
        __root.append(ET.Comment("formatter specific imports"))
        for i in imports[self.formatter]:
            ET.SubElement(__root, "xsl:import", href=i)
        __root.append(ET.Comment("configuration overrides"))
        for i in ["cfg:fo/attrs/custom.xsl",
                  "cfg:fo/xsl/custom.xsl"]:
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
        ET.SubElement(__root, "xsl:param", name="tocMaximumLevel", select=self.toc_maximum_level)
        ET.SubElement(__root, "xsl:param", name="ditaVersion", select="number(/*[contains(@class,' map/map ')]/@ditaarch:DITAArchVersion)")
        
        ditagen.generator.indent(__root)
        ditagen.generator.set_prefixes(__root, {
            "xsl": "http://www.w3.org/1999/XSL/Transform",
            "fo": "http://www.w3.org/1999/XSL/Format",
            "e": self.plugin_name,
            "ditaarch": "http://dita.oasis-open.org/architecture/2005/"
            })
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
        if not self.link_pagenumber:
            ET.SubElement(__root, u"variable", id=u"On the page")
        # table continued
        if self.table_continued:
            ET.SubElement(__root, u"variable", id=u"#table-continued").text = u"Table continued\u2026"
        
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
                self._run_generation(__zip, self.__generate_custom,
                                    "%s/cfg/fo/xsl/custom.xsl" % (self.plugin_name))
                # custom XSLT attribute sets
                self._run_generation(__zip, self.__generate_custom_attr,
                                    "%s/cfg/fo/attrs/custom.xsl" % (self.plugin_name))
                # shell XSLT
                if self.override_shell:
                    self._run_generation(__zip, self.__generate_shell,
                                        "%s/xsl/fo/topic2fo_shell_%s.xsl" % (self.plugin_name, self.formatter))
#                if not self.link_pagenumber or self.table_continued:
                for lang in self.variable_languages:
                    self._run_generation(__zip, lambda: self.__generate_vars(lang),
                                         "%s/cfg/common/vars/%s.xml" % (self.plugin_name, lang))
#                if self.generate_shell:
#                    # shell XSLT
#                    self._run_generation(__zip, self.__generate_shell,
#                                        "%s/xsl/fo/.xsl" % (self.plugin_name))
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
