#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
THIS FILE IS PART OF AZUR LANE TOOL BY MATT BELFAST BROWN
mode_BlP_Cal.py - The core mode of the Azur Lane Tool.

Author: Matt Belfast Brown 
Creat Date:2021-07-10
Version Date：2021-08-02
Version:0.3.9


THIS PROGRAM IS FREE FOR EVERYONE,IS LICENSED UNDER GPL-3.0
YOU SHOULD HAVE RECEIVED A COPY OF GPL-3.0 LICENSE.

Copyright (C) 2021  Matt Belfast Brown

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
#define variable name
 variable-name chinese
 #数据库内变量名称
 vari_shid     舰船编号
 vari_shnm     舰船名称
 vari_shty     科研类别
 vari_lbpr     剩余蓝图数
 vari_dlev     开发等级
 vari_dexp     开发经验值
 vari_cobp     开发消耗蓝图
 vari_nopl     满科研需求蓝图
 vari_figr     拟合等级
 vari_stra     阶段达成率
 vari_tyco     天运消耗
 vari_tyde     满天运需求
 vari_tobp     总用蓝图数
 vari_nebp     总需求蓝图数
 vari_expe     舰船经验值
 vari_leve     舰船等级
 vari_acex     积累经验值
 vari_texp     总获得经验
 #
 flag_pltp     布尔-科研类别
 flag_pftf     布尔-是否进行天运拟合
 fun_cnbp_rqup 函数-计算升级所需蓝图数量
 fun_cnbp_rqub 函数-计算升级所需基础蓝图数量
 fun_cnbp_rrcl 函数-计算升到某级所需蓝图数量
 fun_cnbp_tyfi 函数-计算天运拟合蓝图数量
 vari_plde     变量-需求的科研等级
 para_plle     参量-用于函数循环-科研等级
 para_plee     参量-用于函数循环-科研等级
 vari_plle     变量-科研等级
 vari_plln     变量-现有科研等级
 vari_epbp     变量-现有蓝图数量
 vari_bprb     变量-升一级所需基础蓝图数量
 vari_bprq     变量-升一级所需蓝图数量
 vari_tbpr     变量-升到某级总需的蓝图数
 vari_tebp     变量-已用的总蓝图数无天运拟合
 vari_tbpt     变量-已用的总蓝图数含天运拟合
 vari_prbp     变量-科研图纸需求无天运拟合
 vari_prbt     变量-科研图纸需求含天运拟合
 vari_tyfg     变量-天运拟合拟合等级
 vari_crtf     变量-天运拟合阶段完成率
 vari_bpty     变量-天运拟合总用蓝图数
 vari_tbtf     变量-天运拟合总需蓝图数
#define function

'''
#define import list
    #Null

def fun_cnbp_rqub (vari_plle) :
    #最高方案类型
    if 1 <= vari_plle <= 4 or 6 <= vari_plle <= 9 or 11 <= vari_plle <= 14 :
        vari_bprb = 0.4 * vari_plle - 0.4* ( vari_plle % 5 ) + 2
    elif 16 <= vari_plle <= 19 or 21 <= vari_plle<= 24 or 26 <= vari_plle <= 29 :
        vari_bprb = vari_plle - ( vari_plle % 5) - 5
    elif vari_plle == 5:
        vari_bprb = 5 
    elif vari_plle % 5 ==0:
        vari_bprb =int ( -(vari_plle ** 3 ) / 375 + ( vari_plle ** 2 ) / 5 - 2.9333 * vari_plle +20 )
    return vari_bprb  #升一级所需基础蓝图数量

def fun_cnbp_rqup (flag_pltp,vari_plle):
    if flag_pltp =='Top Solution':
        #最高方案
        vari_bprq = fun_cnbp_rqub(vari_plle)
    elif flag_pltp == 'Decisive Plan' :
        #决战方案
        vari_bprq = int(fun_cnbp_rqub(vari_plle)*1.5)  #最高方案类的1.5倍，并向下取整
    return vari_bprq  #升一级所需蓝图数量

def fun_cnbp_rrcl(flag_pltp,vari_plde,vari_epbp):
    vari_tbpr=0
    vari_tebp=0
    for para_plle in range (vari_lede):
        vari_tbpr+=fun_cnbp_rqup(flag_pltp,para_leve)
    for para_plee in range (vari_levn):
        vari_tebp+=fun_cnbp_rqup(flag_pltp,para_leex)
    vari_tebp+=vari_epbp
    vari_prbp=vari_tbpr-vari_tebp
    return vari_prbp,vari_tebp  #科研图纸需求计算结果 已用的总蓝图数

def fun_cnbp_tyfi(flag_pltp,vari_tfdl,vari_tyfg,vari_crtf):
    vari_bpty=0
    if flag_pltp == 'Top Solution' :
        for i in range(x):
            vari_bpty+=list_fitt[i]
        vari_bpty+=int((vari_crtf/100)*list_fitt[x])
        vari_tbtf=165-vari_bpty
    '''
        elif flag_pltp == 'Decisive Plan' :
        for i in range(x):
            vari_bpty+=list_fitd[i]
        vari_bpty+=int((vari_crtf/100)*list_fitt[x])
        vari_tbtf=215-vari_bpty   
    '''   #暂无彩船拟合方案
    return vari_tbtf,vari_bpty  #天运拟合总需蓝图数  天运拟合总用蓝图数
def fun_cnbp_rbpt(flag_pltp,flag_pftf,vari_plde,vari_epbp,vari_tfdl,vari_tyfg,vari_crtf):
    if flag_pftf == True:
        vari_tbtf,vari_bpty=fun_cnbp_tyfi(flag_pltp,vari_tfdl,vari_tyfg,vari_crtf)
    elif flag_pftf == False:
        vari_tbtf,vari_bpty=0,0
    vari_prbp,vari_tebp=fun_cnbp_rrcl(flag_pltp,vari_plde,vari_epbp)
    vari_prbt=vari_prbp+vari_tbtf
    vari_tbpt=vari_tebp+vari_bpty
    return [vari_prbt,vari_tbpt,vari_prbp,vari_tebp,vari_tbtf,vari_bpty]#[科研图纸需求含天运拟合,已用的总蓝图数含天运拟合,科研图纸需求计算结果,已用的总蓝图数,天运拟合总需蓝图数,天运拟合总用蓝图数]
    
#define list
list_fitt=[10,20,30,40,65]
#list_fitd=[12,24,36,48,78]