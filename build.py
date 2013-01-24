#!/usr/bin/env python

import os
import logging
import optparse

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

options = ''

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

    rFilePath = os.path.join(options.resource_folder, options.class_name + '.h')
    logging.info('Creating "%s" resources registry class', rFilePath)
    rFile = open(rFilePath, 'w')

    write_header(rFile)
    walk_folder(options.resource_folder, options, rFile)
    rFile.close()

def walk_folder(folder, options, file):
    for (dirPath, dirNames, fileNames) in os.walk(folder):
        logging.debug("Processing folder %s %s %s" % (dirPath, dirNames, fileNames))
        if dirPath != options.resource_folder:
            write_class(options, os.path.split(dirPath)[1], fileNames, file)

        for (dir) in dirNames:
            walk_folder(dir, options, file)

        # For each file in the folder we will need to emit properties on that class

def write_header(file):
    file.write("Header\n")

def write_class(options, className, properties, file):
    logging.debug("Creating class %s" % (className))

    className = "__%s_%s" % (options.class_name, className)
    file.write('@interface %s : NSObject\n' % className)
    file.write('\n')
    for (p) in properties:
        file.write('- (NSString *)%s;\n' % p)
    file.write('\n')
    file.write('@end\n')
    file.write('\n')
    file.write('@implementation %s\n' % className)
    file.write('\n')
    for (p) in properties:
        file.write('- (NSString *)%s {\n' % p)
        file.write('return @"%s";\n' % p)
    file.write('}\n')
    file.write('\n')
    file.write('@end\n')
    file.write('\n')


if __name__ == "__main__":
    main()