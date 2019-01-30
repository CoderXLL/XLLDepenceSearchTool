#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'工程中每个模块的耦合关系'

__author__ = 'CoderXLL'

import os
import re
import sys

modulePath = ''
# 获取工程路径
def getProjectPath():
    _selfDirPath = os.path.dirname(os.path.realpath(__file__))
    return _selfDirPath

projectPath = getProjectPath()
# 忽略的模块
ignoreModules = ['Pods']
# 所有类所处的模块map
allClsDic = {}
# 要检索的模块中依赖类的集合
allDepenceSet = set()
# 组件中被依赖的类对应的组件类集合
moduleClsDic = {}

# 每个类所在的模块
def searchAllCls(dirPath):
    fileList = os.listdir(dirPath)
    # 开始迭代
    for subFile in fileList:
        # 忽略pod文件
        if subFile in ignoreModules:
            continue
        # 拼接全路径
        absolutePath = os.path.join(dirPath, subFile)
        # 判断是否为目录
        isDir = os.path.isdir(absolutePath)
        if not isDir:
            pattern = r'^(\w+)\.+[h,m]$'
            regix = re.compile(pattern)
            match = regix.search(subFile)
            if match:
                allClsDic[match.group(1)] = os.path.dirname(absolutePath)
        else:
            searchAllCls(absolutePath)

# 开始运转插件
def startWork():
    searchAllCls(projectPath)
    enumerateModule(modulePath)
    otherModuleDic = getOtherModuleClses()
    print('\n')
    tempList = modulePath.split('/')
    moduleName = tempList[len(tempList) - 1]
    if len(otherModuleDic.keys()) == 0:
        print('%s组件实现完全解耦' % moduleName)
    else:
        print('%s组件依赖的所有其他模块信息如下:' % moduleName)
        for key, infoDict in otherModuleDic.items():
            depencedCls = infoDict['depenced']
            print('%s：其被%s组件类所依赖， 所属模块为:%s' % (key, '、'.join(depencedCls), infoDict['belongModule']))
            print('\n')

# 检索module模块
def enumerateModule(dirPath):
    fileList = os.listdir(dirPath)
    for subFile in fileList:
        absolutePath = os.path.join(dirPath, subFile)
        isDir = os.path.isdir(absolutePath)
        if not isDir:
            pattern = r'^(\w+)\.+[h,m]$'
            match = re.match(pattern, subFile)
            if match:
                # 去检索里面依赖了那些类
                searchDepenceClses(absolutePath)
        else:
            enumerateModule(absolutePath)

# 检索组件依赖了哪些类
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
                
                if not depenceCls in moduleClsDic.keys():
                    moduleClsDic[depenceCls] = []
                moduleLists = moduleClsDic[depenceCls]
                moduleLists.append(currentName)

# 获取依赖其他模块的类
def getOtherModuleClses():
    otherModuleDic = {}
    for clsName in allDepenceSet:
        clsModule = allClsDic.get(clsName)
        if clsModule == '':
            continue
        if not isinstance(clsModule, str):
            continue
        pattern = r'^' + modulePath
        match = re.match(pattern, clsModule)
        if not match:
            infoDict = {'belongModule': clsModule, 'depenced': moduleClsDic[clsName]}
            otherModuleDic[clsName] = infoDict
    return otherModuleDic

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
        print('正在检索中...')
        startWork()

if __name__ == '__main__':
    main()

# entry('/Users/xiaole/im_ios_sdk/XLLIMClient/XLLIMChat/XLLIMChat/General/Dialog')





