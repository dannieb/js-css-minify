from optparse import OptionParser
from subprocess import check_call
import os
import re

'''
Base Minifier
'''
class Minifier(object):
    def minify(self, directory):
        raise Exception("Unimplemented")
    
'''
YUI Compressor recursive minification
'''
class YUIMinifier(Minifier):
    def __init__(self):
        directory = os.path.split(os.path.abspath(__file__))[0]
        self.__compressor = os.path.join(directory, "yuicompressor-2.4.7.jar")
    
    def minify(self, directory):
        regex = re.compile(r'.*\.(css|js)$')
        files = os.listdir(directory)
        for file in files :
            fullPath = os.path.join(directory, file)
            if os.path.isdir(fullPath) :
                self.minify(fullPath)
            elif regex.findall(file) :
                try :
                    check_call(["java", "-jar", self.__compressor, fullPath, "-o", fullPath])
                    print "%s" % fullPath
                except Exception, ex :
                    print "failed to minify %s" % fullPath
                

if __name__ == "__main__" :
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="directory",
                      help="Minify will traverse this directory and recursively minify js and css files")

    (options, args) = parser.parse_args()
    
    minifier = YUIMinifier()
    if options.directory :
        minifier.minify(options.directory)
        