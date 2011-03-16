# -*- Mode: Python; tab-width: 2; indent-tabs-mode:nil; -*-
# vim: set ts=2 et sw=2 tw=80:
# ***** BEGIN LICENSE BLOCK *****
# Version: Apache License 2.0
#
# Copyright (c) 2011 Design Science, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Contributor(s):
#   Frederic Wang <fred.wang@free.fr> (original author)
#
# ***** END LICENSE BLOCK *****

from datetime import datetime
import ConfigParser
import HTMLTestRunner
import platform
import reftest
import seleniumMathJax
import argparse
import time
import unittest

def getOperatingSystem(aOperatingSystem):

    if aOperatingSystem != "auto":
        return aOperatingSystem

    return platform.system()

def getBrowserStartCommand(aBrowserPath, aOS, aBrowser):

    if aBrowser == "Firefox":
        startCommand = "*firefox"
    elif (aOS == "Windows" or aOS == "Mac") and aBrowser == "Safari":
        startCommand = "*safariproxy"
    elif aBrowser == "Chrome":
        startCommand = "*googlechrome"
    elif aBrowser == "Opera":
        startCommand = "*opera"
    elif aOS == "Windows" and aBrowser == "MSIE":
        startCommand = "*iexploreproxy"
    elif aOS == "Linux" and aBrowser == "Konqueror":
        startCommand = "*konqueror"
    else:
        startCommand = "*custom"
    
    if aBrowserPath == "auto":
        if startCommand == "*custom":
            print "Unknown browser version"
            return "unknown"

        if aOS == "Linux" and aBrowser == "Konqueror":
           startCommand = startCommand + " /usr/bin/konqueror" 
    else:
        startCommand = startCommand + " " + aBrowserPath
    
    return startCommand

def getOutputFileName(aOutput, aSelenium):

    if aOutput != "auto":
        return aOutput

    utcdate = datetime.now().isoformat("_")
    return "results/" + \
        aSelenium.mOperatingSystem + "_" + \
        aSelenium.mBrowser + "_" + \
        aSelenium.mBrowserVersion + "_" + \
        aSelenium.mFont + "_" + \
        utcdate + ".html"

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="A Python script to run MathJax automated tests.")
    parser.add_argument("-c", "--config", nargs='?', default="default.cfg",
                        help="A file describing the parameters of the \
automated test instance to run. The default configuration file is default.cfg.")
    args = parser.parse_args()

    # Load configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open(args.config))

    # framework section
    section = "framework"
    host = config.get(section, "host")
    port = config.getint(section, "port")
    mathJaxPath = config.get(section, "mathJaxPath")
    mathJaxTestPath = config.get(section, "mathJaxTestPath")
    timeOut = config.getint(section, "timeOut")
    fullScreenMode = config.getboolean(section, "fullScreenMode")
    
    # platform section
    section = "platform"
    operatingSystem = getOperatingSystem(config.get(section, "operatingSystem"))
    browserList = config.get(section, "browser").split()
    browserVersionList = config.get(section, "browserVersion").split()
    browserModeList = config.get(section, "browserMode").split()
    browserPath = config.get(section, "browserPath")
    fontList = config.get(section, "font").split()
    nativeMathML = config.getboolean(section, "nativeMathML")
    
    # testsuite section
    section = "testsuite"
    outputFile = config.get(section, "outputFile")
    runSlowTests = config.getboolean(section, "runSlowTests")
       
    if (len(browserList) > 1 or len(browserVersionList) > 1 or
        len(browserModeList) or len(fontList) > 1):
        msg =  " can not be specified when launching several instances at the"
        msg += "same time."
        if browserPath != "auto":
            print "browserPath" + msg
            exit(1)
        if outputFile != "auto":
            print "outputFile" + msg
            exit(1)

    for browser in browserList:
        for browserVersion in browserVersionList:
            for font in fontList:
                for browserMode in browserModeList:

                    # Browser mode is only relevant for MSIE
                    if not(browserMode == "StandardMode" or browser == "MSIE"):
                        continue

                    browserStartCommand = getBrowserStartCommand(
                        browserPath,
                        operatingSystem,
                        browser)

                    if browserStartCommand != "unknown":
                        
                        # Create a Selenium instance
                        selenium = seleniumMathJax.seleniumMathJax(
                            host, port, mathJaxPath, mathJaxTestPath,
                            operatingSystem,
                            browser,
                            browserVersion,
                            browserMode,
                            browserStartCommand, 
                            font,
                            nativeMathML,
                            timeOut,
                            fullScreenMode)
                        
                        # Create the test suite
                        suite = reftest.reftestSuite(runSlowTests)
                        suite.addReftests(selenium, "reftest.list")
                        
                        # Create the output file
                        output = getOutputFileName(outputFile, selenium)
                        
                        # Run the test suite
                        selenium.start()
                        
                        fp = file(output, "wb")
                        HTMLTestRunner.HTMLTestRunner(stream=fp,
                                                      verbosity=2).run(suite)
                        fp.close()
                        
                        selenium.stop()
                        time.sleep(4)

                # end if browserStartCommand
            # end for font
        # end browserVersion
    # end browser

    exit(0)
