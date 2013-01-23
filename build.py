#!/usr/bin/env python

import os
import re
import subprocess
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

    r_file_path = os.path.join(options.resource_folder, options.class_name + '.h')
    logging.info('Creating "%s" resources registry class', r_file_path)
    r_file = open(r_file_path, 'w')


    r_file.write("hi there 2")
    r_file.close()


if __name__ == "__main__":
    main()