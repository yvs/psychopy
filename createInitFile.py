#!/usr/bin/env python
"""Writes the current version, build platform etc to 
"""
import os, copy, platform, subprocess

#read the current version from the file
f = open('version')
version = f.read()
f.close()

template="""# Part of the PsychoPy library
# Copyright (C) 2011 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).

#version info for PsychoPy
#This file is automatically generated during build (do not edit directly).
__version__='$version$'
__license__='GNU GPLv3 (or more recent equivalent)'
__author__='Jonathan Peirce'
__author_email__='jon@peirce.org.uk'
__maintainer_email__='psychopy-dev@googlegroups.com'
__url__='http://www.psychopy.org'
__downloadUrl__='http://code.google.com/p/psychopy/downloads'
"""
template = template.replace('$version$', version)

allList = '\n__all__ = ["gui", "misc", "visual", "core", "event", "data", "filters"]'

getGitShaRuntime="""
if __git_sha__=='n/a':
    import subprocess
    #see if we're in a git repo and fetch from there
    repo_commit=False
    proc = subprocess.Popen('git rev-parse --short HEAD',
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd='.', shell=True)
    repo_commit, _ = proc.communicate()
    del proc#to get rid of the background process
    if repo_commit:
        __git_sha__=repo_commit.strip()#remove final linefeed
"""

def _getGitShaString(dist=None):
    """If generic==True then returns empty __git_sha__ string
    """
    if dist==None:
        shaStr='n/a'
    else:
        import subprocess
        #see if we're in a git repo and fetch from there
        proc = subprocess.Popen('git rev-parse --short HEAD',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd='.', shell=True)
        repo_commit, _ = proc.communicate()
        del proc#to get rid of the background process
        if repo_commit:
            shaStr=repo_commit.strip()#remove final linefeed
        else: 
            shaStr='n/a'
    return "__git_sha__='%s'" %shaStr
    
def _getPlatformString(dist=None):
    """If generic==True then returns empty __build_platform__ string
    """
    if dist=='bdist':
        #get platform-specific info
        if os.sys.platform=='darwin':
            OSXver, junk, architecture = platform.mac_ver()
            systemInfo = "OSX_%s_%s" %(OSXver, architecture)
        elif os.sys.platform=='linux':
            systemInfo = '%s_%s_%s' % (
                'Linux',
                ':'.join([x for x in platform.dist() if x != '']),
                platform.release())
        elif os.sys.platform=='win32':
            ver=os.sys.getwindowsversion()
            if len(ver[4])>0:
                systemInfo="win32_v%i.%i.%i (%s)" %(ver[0],ver[1],ver[2],ver[4])
            else:
                systemInfo="win32_v%i.%i.%i" %(ver[0],ver[1],ver[2])
        else:
            systemInfo = platform.system()+platform.release()
    else:
        systemInfo="n/a"
    return "__build_platform__='%s'\n" %systemInfo
    
def createInitFile(dist=None):
    """Write the version file to psychopy/version.py
    
    :param:`dist` can be:
        None: 
            writes __version__
        'sdist': 
            for python setup.py sdist - writes __version__ and git id (__git_sha__)
        'bdist': 
            for python setup.py bdist - writes __version__, git id (__git_sha__) 
            and __build_platform__
    """
    f = open(os.path.join('psychopy','__init__.py'), 'w')
    outStr = copy.copy(template)
    outStr += _getPlatformString(dist)
    outStr += _getGitShaString(dist)
    outStr += getGitShaRuntime
    outStr += allList
    f.write(outStr)
    f.close()
    return outStr
    