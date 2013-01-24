#!/usr/bin/env python

import os
import logging
import optparse

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

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

    for (dirPath, dirNames, fileNames) in os.walk(options.resource_folder):
        logging.info("%s %s %s" % (dirPath, dirNames, fileNames))
        write_class(options.class_name, rFile, dirNames, fileNames)
        # For each folder we will need to emit a class
        # For each file in the folder we will need to emit properties on that class


    rFile.close()

def write_header(file):
    file.write("Header\n")

def write_class(rClassName, file, className, properties):
    className = "__%s_%s" % (rClassName, className)
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