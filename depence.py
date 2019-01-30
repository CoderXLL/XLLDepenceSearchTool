#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'工程中每个模块的耦合关系'

__author__ = 'CoderXLL'

import os
import re
import sys

modulePath = ''
#获取工程路径
def getProjectPath():
    _selfDirPath = os.path.dirname(os.path.realpath(__file__))
    return os.path.dirname(_selfDirPath)
projectPath = getProjectPath()
#忽略的模块
ignoreModules = ['Pods']
#所有类所处的模块map
allClsDic = {}
#要检索的模块中依赖类的集合
allDepenceSet = set()
#每个类所在的模块
def searchAllCls(dirPath):
    fileList = os.listdir(dirPath)
    #开始迭代
    for subFile in fileList:
        #忽略pod文件
        if subFile in ignoreModules:
            continue
        #拼接全路径
        absolutePath = os.path.join(dirPath, subFile)
        #判断是否为目录
        isDir = os.path.isdir(absolutePath)
        if not isDir:
            pattern = r'^(\w+)\.+[h,m]$'
            regix = re.compile(pattern)
            match = regix.search(subFile)
            if match:
                allClsDic[match.group(1)] = os.path.dirname(absolutePath)
        else:
            searchAllCls(absolutePath)

#开始运转插件
def startWork():
    print('正在迭代该模块之外的耦合关系...')
    searchAllCls(projectPath)
    enumerateModule(modulePath)
    otherModuleList = getOtherModuleClses()
    if len(otherModuleList) == 0:
        print('该模块实现完全解耦')
    else:
        print('该模块依赖的所有其他模块的类如下:')
        for otherModuleDic in otherModuleList:
            for key, value in otherModuleDic.items():
                print('类名:%s, 所属模块为:%s' % (key, value))


#获取依赖其他模块的类
def getOtherModuleClses():
    otherModuduleList = []
    otherModuleDic = {}
    for clsName in allDepenceSet:
        clsModule = allClsDic.get(clsName)
        if clsModule == '':
            continue
        if not isinstance(clsModule, str):
            continue
        pattern = r'^' + modulePath
        regix = re.compile(pattern)
        match = regix.match(clsModule)
        if not match:
            otherModuleDic[clsName] = clsModule
            isExist = False
            for dict in otherModuduleList:
                if clsName in dict.keys():
                    isExist = True
            if not isExist:
                otherModuduleList.append(otherModuleDic)
    return otherModuduleList

#检索module模块
def enumerateModule(dirPath):
    fileList = os.listdir(dirPath)
    for subFile in fileList:
        absolutePath = os.path.join(dirPath, subFile)
        isDir = os.path.isdir(absolutePath)
        if not isDir:
            pattern = r'^(\w+)\.+[h,m]$'
            match = re.match(pattern, subFile)
            if match:
                #去检索里面依赖了那些类
                searchDepenceClses(absolutePath)
        else:
            enumerateModule(absolutePath)

#检索依赖了哪些类
def searchDepenceClses(filePath):
    pathComponents = filePath.split('/')
    temp = pathComponents[len(pathComponents) - 1]
    currentName = temp[:len(temp) - 2]
    fm = open(filePath, "r")
    for line in fm.readlines():
        pattern = r'^\s*#import\s+\"(\w+).h\"$'
        match = re.match(pattern, line)
        if match:
            depenceCls = match.group(1)
            if not currentName == depenceCls:
                allDepenceSet.add(depenceCls)


def entry(tempModulePath):
    global modulePath
    modulePath = tempModulePath
    startWork()

def main():
    argvCount = len(sys.argv)
    global modulePath
    if not argvCount == 2:
        raise AttributeError('请传入正确的参数')
    else:
        modulePath = sys.argv[1]
        startWork()

if __name__ == '__main__':
    main()

# entry('/Users/xiaole/GitProject/GitHub/KKTalkee_iPhone/KKTalkee_iPhone/Network')


