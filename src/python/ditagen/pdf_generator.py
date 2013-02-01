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
    ("line-height", "body", "1.2em", False),
    
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
    ("line-height", "topic", None, True),
    
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
    ("line-height", "topic.topic", None, True),
    
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
    ("line-height", "topic.topic.topic", None, True),
    
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
    ("line-height", "topic.topic.topic.topic", None, True),

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
    ("line-height", "section", None, True),
    
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
    ("line-height", "note", None, True),
    
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
    ("line-height", "pre", None, True),
    
    ("font-family", "link", None, True),
    ("font-size", "link", None, True),
    ("color", "link", "blue", False),
    ("font-weight", "link", None, True),
    ("font-style", "link", None, True),
    ("text-decoration", "link", None, True),
    ("space-before", "link", None, False),
    ("space-after", "link", None, False),
    ("text-align", "link", None, False),
    ("start-indent", "link", None, False),
    ("line-height", "link", None, False)
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

langs = {
  u"de": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Abbildung: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabelle: <param ref-name='title'/></variable>"
  },
  u"en": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Figure: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Table: <param ref-name='title'/></variable>"
  },
  u"es": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Figura: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabla: <param ref-name='title'/></variable>"
  },
  u"fi": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Kuva. <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Taulu. <param ref-name='title'/></variable>"
  },
  u"fr": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Illustration: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Table: <param ref-name='title'/></variable>"
  },
  u"he": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>&#x5d0;&#x5d9;&#x5d5;&#x5e8;. <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>&#x5d8;&#x5d1;&#x5dc;&#x5d4;. <param ref-name='title'/></variable>"
  },
  u"it": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'> Figura: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabella: <param ref-name='title'/></variable>"
  },
  u"ja": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>&#x56f3; : <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>&#x8868; : <param ref-name='title'/></variable>"
  },
  u"nl": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Figuur: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabel: <param ref-name='title'/></variable>"
  },
  u"ro": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Fig.. <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabel. <param ref-name='title'/></variable>"
  },
  u"ru": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>&#x420;&#x438;&#x441;&#x443;&#x43d;&#x43e;&#x43a;. <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>&#x422;&#x430;&#x431;&#x43b;&#x438;&#x446;&#x430;. <param ref-name='title'/></variable>"
  },
  u"sv": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>Figur. <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>Tabell. <param ref-name='title'/></variable>"
  },
  u"zh_CN": {
    u"#table-continued": u"<variable id='#table-continued'>Table continued&#x2026;</variable>",
    u"Figure": u"<variable id='Figure'>&#x56fe;: <param ref-name='title'/></variable>",
    u"Table": u"<variable id='Table'>&#x8868;: <param ref-name='title'/></variable>"
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
        self.dl = None
        self.title_numbering = None
        self.table_numbering = None
        self.figure_numbering = None
        self.generate_shell = None
        self.link_pagenumber = None
        self.table_continued = None
        self.formatter = None
        self.override_shell = False
        self.cover_image = None
        self.cover_image_name = None
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

    def __generate_custom(self, stylesheet=None):
        """Generate plugin custom XSLT file."""
        __root = ET.Element(NS_XSL + "stylesheet", {"version":"2.0", "exclude-result-prefixes": "e opentopic"})
        
        __cover_raw = """
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                xmlns:e="e"
                exclude-result-prefixes="e"
                version="2.0">

  <xsl:template name="createFrontMatter_1.0">
    <fo:page-sequence master-reference="front-matter" xsl:use-attribute-sets="__force__page__count">
      <xsl:call-template name="insertFrontMatterStaticContents"/>
      <fo:flow flow-name="xsl-region-body">
        <fo:block xsl:use-attribute-sets="__frontmatter">
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
          <xsl:apply-templates select="$map//*[contains(@class,' bookmap/booktitlealt ')]"/>
          <fo:block xsl:use-attribute-sets="__frontmatter__owner">
            <xsl:apply-templates select="$map//*[contains(@class,' bookmap/bookmeta ')]"/>
          </fo:block>
          <fo:external-graphic src="url({concat($artworkPrefix, $e:cover-image-path)})" xsl:use-attribute-sets="image"/>
        </fo:block>
      </fo:flow>
    </fo:page-sequence>
    <xsl:if test="not($retain-bookmap-order)">
      <xsl:call-template name="createNotices"/>
    </xsl:if>
  </xsl:template>
  
</xsl:stylesheet>"""

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
        if stylesheet == "front-matter" or not stylesheet:
            if self.cover_image_name:
                __root.append(ET.Comment("cover"))
                for __c in list(ET.fromstring(__cover_raw)):
                        __root.append(__c)
        
        if stylesheet == "tables" or not stylesheet:
            __root.append(ET.Comment("table"))
            __table_raw = __table_footer_raw
            if self.table_continued:
                __table_raw = __table_continued_raw
            for __c in list(ET.fromstring(__table_raw)):
                __root.append(__c)
        
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
    
        if stylesheet == "commons" or not stylesheet:
            if self.title_numbering:
                __root.append(ET.Comment("title numbering"))
                for __c in list(ET.fromstring(__get_title_raw)):
                    __root.append(__c)
                    
        if not stylesheet:
            if not self.override_shell and self.toc_maximum_level:
                __root.append(ET.Comment("TOC"))
                ET.SubElement(__root, NS_XSL + "variable", name=u"tocMaximumLevel").text = self.toc_maximum_level
        
        ditagen.generator.indent(__root)
        ditagen.generator.set_prefixes(__root, {"xsl": "http://www.w3.org/1999/XSL/Transform", "fo": "http://www.w3.org/1999/XSL/Format", "e": self.plugin_name, "opentopic": "http://www.idiominc.com/opentopic"})
        
        __d = ET.ElementTree(__root)
        __d.write(self.out, "UTF-8")

    def __generate_custom_attr(self, stylesheet=None):
        """Generate plugin custom XSLT file."""
        __root = ET.Element(NS_XSL + "stylesheet", {"version":"2.0", "exclude-result-prefixes": "e"})
        
        if stylesheet == "front-matter-attr" or not stylesheet:
            if self.cover_image_name:
                ET.SubElement(__root, NS_XSL + "variable", name="e:cover-image-path").text = "Customization/OpenTopic/common/artwork/" + self.cover_image_name
        
        if stylesheet == "commons-attr" or not stylesheet:
            # force page count
            if self.force_page_count:
                __page_count_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name="__force__page__count")
                ET.SubElement(__page_count_attr, NS_XSL + "attribute", name=u"force-page-count").text = self.force_page_count
        
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
                ET.SubElement(__pre_attr, NS_XSL + "attribute", name=k).text = v
        
        if stylesheet == "tables-attr" or not stylesheet:
            # dl
            if self.dl:
                __dt_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name="e:dlentry.dt__content")
                ET.SubElement(__dt_attr, NS_XSL + "attribute", name=u"font-weight").text = "bold"
                ET.SubElement(__dt_attr, NS_XSL + "attribute", name=u"keep-with-next").text = "always"
                __dd_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name="e:dlentry.dd__content")
                if self.dl == "html":
                    ET.SubElement(__dd_attr, NS_XSL + "attribute", name=u"start-indent").text = "from-parent(start-indent) + 5mm"
            # table continued
            if self.table_continued:
                __table_continued_attr = ET.SubElement(__root, NS_XSL + "attribute-set", { "name": "e:tfoot.row.entry.continued" })
                ET.SubElement(__table_continued_attr, NS_XSL + "attribute", name=u"border-right-style").text = "hidden"
                ET.SubElement(__table_continued_attr, NS_XSL + "attribute", name=u"border-left-style").text = "hidden"
                ET.SubElement(__table_continued_attr, NS_XSL + "attribute", name=u"text-align").text = "end"
                ET.SubElement(__table_continued_attr, NS_XSL + "attribute", name=u"font-style").text = "italic"
        
        if stylesheet == "layout-masters-attr" or not stylesheet:
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
                    ET.SubElement(__root, NS_XSL + "variable", name=k).text = v
            # font size
            if "font-size" in self.style["body"]:
                ET.SubElement(__root, NS_XSL + "variable", name=u"default-font-size").text = self.style["body"]["font-size"]
            # line height
            if "line-height" in self.style["body"]:
                ET.SubElement(__root, NS_XSL + "variable", name=u"default-line-height").text = self.style["body"]["line-height"]
            # body indent
            if "start-indent" in self.style["body"]:
                ET.SubElement(__root, NS_XSL + "variable", name=u"side-col-width").text = self.style["body"]["start-indent"]
        
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
        fs.append("plugin:org.dita.pdf2:cfg/fo/attrs/lists-attr.xsl")
        fs.append("plugin:org.dita.pdf2:xsl/fo/lists.xsl")
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
            #ET.SubElement(__root, u"variable", id=u"#table-continued").text = u"Table continued\u2026"
            __root.append(ET.fromstring(langs[lang][u"#table-continued"]))
        # table caption numbering
        if self.table_numbering == u"none":
            __root.append(ET.fromstring(langs[lang][u"Table"]))
        # figure caption numbering
        if self.figure_numbering == u"none":
            __root.append(ET.fromstring(langs[lang][u"Figure"]))
        
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
                if self.override_shell:
                    for s in ["front-matter", "commons", "tables"]:
                        self._run_generation(__zip, lambda: self.__generate_custom(s),
                                            "%s/xsl/fo/%s.xsl" % (self.plugin_name, s))
                else:
                    self._run_generation(__zip, self.__generate_custom,
                                        "%s/cfg/fo/xsl/custom.xsl" % (self.plugin_name))
                # custom XSLT attribute sets
                if self.override_shell:
                    for s in ["front-matter-attr", "commons-attr", "layout-masters-attr", "tables-attr", "basic-settings"]:
                        self._run_generation(__zip, lambda: self.__generate_custom_attr(s),
                                            "%s/cfg/fo/attrs/%s.xsl" % (self.plugin_name, s))
                else:
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
