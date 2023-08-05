#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
THIS FILE IS PART OF AZUR LANE TOOL BY MATT BELFAST BROWN
__init__.py - The core part of the Azur Lane Tool.

Author: Matt Belfast Brown 
Creat Date:2021-07-10
Version Date：2021-08-04
Version:0.4.1


THIS PROGRAM IS FREE FOR EVERYONE,IS LICENSED UNDER GPL-3.0
YOU SHOULD HAVE RECEIVED A COPY OF GPL-3.0 LICENSE.

Copyright (C) 2021  Matt Belfast Brown

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

#import
import AzurLaneToolLib.mode.mode_EXP_Cal as mode_EXP_Cal
import AzurLaneToolLib.mode.mode_BlP_Cal as mode_BlP_Cal
import AzurLaneToolLib.mode.mode_JKN_Com as mode_JKN_Com

#information
__title__ = 'AzurLaneToolLib'
__version__ = '0.4.1'
__author__ = 'Matt Belfast Brown'
__license__ = 'GPL-3.0'
__copyright__ = 'Copyright (c) 2020-2021 Matt Belfast Brown'
__all__ = ['mode',
    'mode_EXP_Cal','mode_BlP_Cal','mode_JKN_Com']

#function
fun_cexp_vrfu=mode_EXP_Cal.fun_cexp_vrfu
fun_crex_cele=mode_EXP_Cal.fun_crex_cele
fun_cnbp_rqup=mode_BlP_Cal.fun_cnbp_rqup
fun_cnbp_rqub=mode_BlP_Cal.fun_cnbp_rqub
fun_cnbp_rrcl=mode_BlP_Cal.fun_cnbp_rrcl
fun_cnbp_tyfi=mode_BlP_Cal.fun_cnbp_tyfi
fun_cnbp_rbpt=mode_BlP_Cal.fun_cnbp_rbpt
fun_jpkn_nmco=mode_JKN_Com.fun_jpkn_nmco