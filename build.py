#!/usr/bin/env python
import fnmatch

import os
import logging
import optparse
import re

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

class Property:
    def __init__(self, name, fileName):
        self.name = name
        self.fileName = fileName

class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.nodes = []
        self.properties = []

    def full_name(self):
        full = self.name
        parent = self.parent
        while parent is not None:
            full += "_" + parent.name
            parent = parent.parent
        return full

    def write_class(self, file):
        file.write('@interface %s : NSObject\n' % self.full_name())
        file.write('\n')
        for (p) in self.properties:
            file.write('- (NSString *)%s;\n' % p.name)
        file.write('\n')
        file.write('@end\n')
        file.write('\n')
#        file.write('@implementation %s\n' % className)
#        file.write('\n')
#        for (p) in fileNames:
#            file.write('- (NSString *)%s {\n' % os.path.splitext(p)[0])
#            file.write('return @"%s";\n' % p)
#        file.write('}\n')
#        file.write('\n')
#        file.write('@end\n')
#        file.write('\n')


def main():
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)

    parser.add_option("-r", "--resource-folder", dest="resource_folder",
                      default="./resources",
                      help="Specifies the resources folder")

    parser.add_option("-c", "--class", dest="class_name",
                      default="R",
                      help="Specifies the name of the resources registry class")

    options, args = parser.parse_args()

    exists = os.path.isdir(options.resource_folder)
    if not exists:
        parser.error("The resource folder specified (%s) does not exist." % options.resource_folder)

    root = Node(options.class_name)
    walk_folder(root, options.resource_folder)

    rFilePath = os.path.join(options.resource_folder, options.class_name + '.h')
    logging.info('Creating "%s" resources registry class', rFilePath)
    rFile = open(rFilePath, 'w')

    write_header(rFile)
    root.write_class(rFile)
    rFile.close()

def walk_folder(node, folder):
    includes = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.ttf', '*.otf', '*.mp3', '*.caf']
    includes = r'|'.join([fnmatch.translate(x) for x in includes])

    for (dirPath, dirNames, fileNames) in os.walk(folder):
        logging.debug("Processing folder %s %s %s" % (dirPath, dirNames, fileNames))
        filtered = [f for f in fileNames if re.match(includes, f)]
        for f in filtered:
            node.properties.append(Property(os.path.splitext(f)[0], f))

#        for (dir) in dirNames:
#            logging.debug("Creating class %s" % dir)
#            child = Node(dir)
#            node.nodes.append(child)
#            child.parent = node
#            walk_folder(child, dir)

def write_header(file):
    file.write("Header\n")


if __name__ == "__main__":
    main()