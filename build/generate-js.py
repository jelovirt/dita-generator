#!/usr/bin/env python
import ditagen
import ditagen.generator

class DomainGenerator:
    
    def __init__(self):
        self.i = 0
        
    def main(self):
        self.write("// Generated from code, do not edit")
        self.write("var domains = {")
        self.i += 1
        for v in ditagen.TOPIC_MAP.keys():
            self.write(v + ": {")
            self.i += 1
            for t in ditagen.TOPIC_MAP[v].keys():
                self.write(t + ": {")
                self.i += 1
                type = ditagen.TOPIC_MAP[v][t]
                o = type()
                default_domains = [d() for d in o.default_domains]
                ps = []
                for d in default_domains:
                    ps.extend(d.parent)
                ps = set(ps)
                #for p in ps:
                #    print "// " + str(p) +  " == " + str(type) + " --> " + str(ditagen.generator.isinstancetype(type, p))#str(ditagen.generator.get_parent_list(type))
                #    if o.parent:
                #        print "  // " + str(o.parent)
                ps = [p for p in set(ps) if p == type or ditagen.generator.isinstancetype(o, p)]
                self.write("domainClass: [" +  ", ".join(['"' + p().id + '"' for p in ps]) +  "],")
                self.write("defaultDomains: [" + ", ".join(['"' + d.id + '"' for d in default_domains])  + "]")
                self.i -= 1
                self.write("},")
            self.i -= 1
            self.write("},")
        self.i -= 1
        self.write("}")
        
    def write(self, line):
        print (" " * 4 * self.i) + line


if __name__ == '__main__':
    DomainGenerator().main()
