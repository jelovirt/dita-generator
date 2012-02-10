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

class StylePluginGenerator(DitaGenerator):
    """Generator for a DITA-OT style plug-in."""

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

    def __init__(self):
        DitaGenerator.__init__(self)
        self.ot_version = None
        self.transtype = None
        self.plugin_name = None
        self.plugin_version = None
        self.page_size = None
        self.page_margins = None
        self.font_family = None
        self.color = None
        self.link_font_weight = None
        self.link_font_style = None
        self.link_color = None
        self.link_text_decoration = None
        self.force_page_count = None
        self.chapter_layout = None
        self.body_column_count = None
        self.index_column_count = None
        self.bookmark_style = None
        self.toc_maximum_level = None
        self.task_label = None
        self.include_related_links = None
        self.side_col_width = None
        self.column_gap = None
        self.mirror_page_margins = None
        self.text_align = None
        self.dl = None
        self.title_numbering = None
        self._stylesheet_stump = []

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
        __root = ET.Element(NS_XSL + "stylesheet", {"version":"2.0", "exclude-result-prefixes": "e"})
        
        __dl_list_raw = """
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                xmlns:e="com.example.print-pdf"
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
<xsl:stylesheet  xmlns:e="com.example.print-pdf"
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
            __dl = ET.fromstring(__dl_raw)
            for __c in list(__dl):
                __root.append(__c)
   
        __get_title_raw = """
<xsl:stylesheet xmlns:fo="http://www.w3.org/1999/XSL/Format"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:e="raystation"
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
                        format="A.1"/>
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
            __get_title = ET.fromstring(__get_title_raw)
            for __c in list(__get_title):
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
        if self.font_family:
            ET.SubElement(__root_attr, NS_XSL + "attribute", name=u"font-family").text = self.font_family
        # font color
        if self.color:
            ET.SubElement(__root_attr, NS_XSL + "attribute", name=u"color").text = self.color
        # text alignment
        if self.text_align:
            ET.SubElement(__root_attr, NS_XSL + "attribute", name=u"text-align").text = self.text_align
        # link
        link_attr_sets = []
        if self.ot_version >= Version("1.5.4"):
            link_attr_sets.extend(["common.link"])
        else:
            link_attr_sets.extend(["link__content", "xref"])
        for n in link_attr_sets:
            __link_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name=n)
            if self.link_color:
                ET.SubElement(__link_attr, NS_XSL + "attribute", name=u"color").text = self.link_color
            if self.link_font_weight:
                ET.SubElement(__link_attr, NS_XSL + "attribute", name=u"font-weight").text = self.link_font_weight
            if self.link_font_style:
                ET.SubElement(__link_attr, NS_XSL + "attribute", name=u"font-style").text = self.link_font_style
            if self.link_text_decoration:
                ET.SubElement(__link_attr, NS_XSL + "attribute", name=u"text-decoration").text = self.link_text_decoration

        # dl
        if self.dl:
            __dt_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name="e:dlentry.dt__content")
            ET.SubElement(__dt_attr, NS_XSL + "attribute", name=u"font-weight").text = "bold"
            ET.SubElement(__dt_attr, NS_XSL + "attribute", name=u"keep-with-next").text = "always"
            __dd_attr = ET.SubElement(__root, NS_XSL + "attribute-set", name="e:dlentry.dd__content")
            if self.dl == "html":
                ET.SubElement(__dd_attr, NS_XSL + "attribute", name=u"start-indent").text = "from-parent(start-indent) + 5mm"

        # page column count
        if self.body_column_count and self.ot_version >= Version("1.5.4"):
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
        if self.default_font_size:
            ET.SubElement(__root, NS_XSL + "variable", name=u"default-font-size").text = self.default_font_size
        # body indent
        if self.side_col_width:
            ET.SubElement(__root, NS_XSL + "variable", name=u"side-col-width").text = self.side_col_width
        # toc
        if self.toc_maximum_level:
            ET.SubElement(__root, NS_XSL + "variable", name=u"tocMaximumLevel").text = self.toc_maximum_level
        
        ditagen.generator.indent(__root)
        ditagen.generator.set_prefixes(__root, {"xsl": "http://www.w3.org/1999/XSL/Transform", "fo": "http://www.w3.org/1999/XSL/Format", "e": self.plugin_name})
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
