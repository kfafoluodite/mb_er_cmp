# -*- coding: utf-8 -*-
import tkFileDialog,xlrd,numpy,os
import matplotlib.pyplot as plt

from Mobileye_info import *
from Can_Data_Pretreatment import *
from DelphiEsr_info import *
from Mobileye_Trackinfo import *
from DelphiEsr_Trackinfo import *
from Rontgen_info import *

#显示中文和负号
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus']=False


#选择文件夹
print 'select excel directory'
os.chdir('c:/')
op_dir = tkFileDialog.askdirectory()

os.chdir(op_dir)
#根据目标目录设置mobileye和esr的主目标ID
dir_name = os.path.split(op_dir)[-1]
if dir_name == 'zhong':
    mmain_id = [0]
    esrmain_id = [59]
elif dir_name =='zhong-1':
    mmain_id = [18]






#综合考虑雷达，mobileye和rontgen的数据，确认对比的起始和结束帧号





#读取can的速度值

debuginfo_file = open('DebugInfo.txt')
debuginfos = debuginfo_file.readlines()
debuginfo_file.close()
caninfos = routgen_caninfo(debuginfos)
[can_frame,can_v] = caninfos.gt_caninfo()
"""can的纵轴值"""
can_v_y = numpy.array(can_v)


#读取mobileye的距离、速度和加速度信息并生成TTC信息
if os.path.exists('can00002.txt'):
    mobileye_can_file = open('can00002.txt')
else:
    mobileye_can_file = open('CanMidFrameInfo.txt')
mobileye_can_txt = mobileye_can_file.readlines()
mobileye_can_file.close()
post_mobileye_txt = can_date_pretreatment(mobileye_can_txt)
mbl_treatment_txt = post_mobileye_txt.mbl_pretreatment()
"""由于mobileye记录不完整，根据距离和速度计算跟踪值"""
mtrack_infos = mobileye_trackinfos()
mtrack_infos.c_trackinfos()

mtrack_d = []
mtrack_v = []
mtrack_a = []
mtrack_ttc = []


for mbl_txt in mbl_treatment_txt:
    mobileye_info = Mobile_Info(mbl_txt)
    obs_dates = mobileye_info.obs_infos()
    mtrack_infos.is_obs(obs_dates)
    mtrack_dates = mtrack_infos.up_trackinfos()
    m_count = 0
    for mtrack_date in mtrack_dates:
        [mtrack_id, mtrack_count, mtrack_flag, mobileye_id, obs_y, obs_x, obs_v, obs_a, obs_angle] = mtrack_date
        if mtrack_id in mmain_id:
            if obs_v < 0:
                obs_ttc = obs_y/math.fabs(obs_v)
            else:
                obs_ttc = -1
            mtrack_d.append(round(obs_y,2))
            mtrack_v.append(round(obs_v,2))
            mtrack_a.append(round(obs_a,2))
            mtrack_ttc.append(round(obs_ttc,2))
        else:
            m_count +=1
    if m_count == len(mtrack_dates):
        if mtrack_d !=[]:
            mtrack_d.append(mtrack_d[-1])
            mtrack_v.append(mtrack_v[-1])
            mtrack_a.append(mtrack_a[-1])
            mtrack_ttc.append(mtrack_ttc[-1])
        else:
            mtrack_d.append(0)
            mtrack_v.append(0)
            mtrack_a.append(0)
            mtrack_ttc.append(-1)



#读取雷达的距离，相对速度及相对加速度信息，并生成TTC信息
if os.path.exists('can00003.txt'):
    esr_can_file = open('can00003.txt')
else:
    esr_can_file = open('CanMidFrameInfo.txt')
esr_can_txt = esr_can_file.readlines()
esr_can_file.close()
post_esr_txt = can_date_pretreatment(esr_can_txt)
esr_treatment_txt = post_esr_txt.esr_pretreatment()

"""由于雷达存在断点，跟踪12帧产生连续的数据"""
esrtrack_infos = esr_trackinfos()
esrtrack_infos.c_trackinfos()
esrtrack_d = []
esrtrack_v = []
esrtrack_a = []
esrtrack_ttc = []

for esr_txt in esr_treatment_txt:
    esr_info = Esr_info(esr_txt)
    esr_obs = esr_info.track_info()
    esrtrack_infos.is_obs(esr_obs)
    esrtrack_dates =esrtrack_infos.up_trackinfos()
    esr_count = 0
    for esrtrack_date in esrtrack_dates:

        [esrtrack_id, esrtrack_count, esrtrack_flag, esr_id, esr_range, esr_range_rate,esr_range_accel, esr_range_angle] = esrtrack_date
        if esrtrack_id in esrmain_id:
            if esr_range_rate < 0 :
                esr_ttc = esr_range/math.fabs(esr_range_rate)
            else:
                esr_ttc = -1
            esrtrack_d.append(esr_range)
            esrtrack_v.append(esr_range_rate)
            esrtrack_a.append(esr_range_accel)
            esrtrack_ttc.append(esr_ttc)
        else:
            esr_count +=1
    if esr_count == len(esrtrack_dates):
        if esrtrack_d != []:
            esrtrack_d.append(esrtrack_d[-1])
            esrtrack_v.append(esrtrack_v[-1])
            esrtrack_a.append(esrtrack_a[-1])
            esrtrack_ttc.append(esrtrack_ttc[-1])
        else:
            esrtrack_d.append(0)
            esrtrack_v.append(0)
            esrtrack_a.append(0)
            esrtrack_ttc.append(-1)


#读取Rontgen的距离，相对速度，相对加速度和TTC的数据
if os.path.exists('10001TTC.txt'):
    testcase_ttc_file = open('10001TTC.txt')
    testcase_ttc_txt = testcase_ttc_file.readlines()
    testcase_ttc_file.close()
    testcase_ttc_info = tcase_ttcinfo(testcase_ttc_txt)
    [rontgen_frame,rontgen_d,rontgen_v,rontgen_a,rontgen_ttc] = testcase_ttc_info.gt_ttcinfo()



#根据帧号确认显示的区间和计算差值







#横轴坐标t














#读取MainObjinfo的帧号数据
if os.path.exists('MainObjInfo.txt'):
    MainObj_file = open('MainObjInfo.txt')
    Mainlines = MainObj_file.readlines()
    Main_fames = []
    for MainObj_line in Mainlines:
        Mainline = Mainlineinfo(MainObj_line)
        Main_fames.append(Mainline.frame())
    MainObj_file.close()



#读取excel文件
files = os.listdir(op_dir)
for file in files:
    if os.path.splitext(file)[-1] == '.xls' or os.path.splitext(file)[-1] == '.xlsx':
        xls_name = file
        radar_file = xlrd.open_workbook(xls_name)
R_table = radar_file.sheet_by_name('AEB-car')
n = len(R_table._cell_values)
Radar_frame = []
Radar_dist = []
Radar_v = []
Radar_ttc = []
number =1
frame = start_frame


while frame != int(R_table.cell(number,3).value):
    Radar_dist.append(0)
    Radar_v.append(0)
    Radar_ttc.append(0)
    frame += 2

while frame <= end_frame:
    if number <n:
        if frame == int(R_table.cell(number,3).value):
            Radar_dist.append(R_table.cell(number, 4).value)
            Radar_v.append(R_table.cell(number, 5).value)
            Radar_ttc.append(R_table.cell(number, 6).value)
            number+=1
        else:
            Radar_dist.append(Radar_dist[-1])
            Radar_v.append(Radar_v[-1])
            Radar_ttc.append(Radar_ttc[-1])
        frame +=2
    else:
        Radar_dist.append(Radar_dist[-1])
        Radar_v.append(Radar_v[-1])
        Radar_ttc.append(Radar_ttc[-1])
        frame +=2



#读取mobileye的can数据信息
if os.path.exists('CanMidFrameInfo.txt'):
    can_file = open('CanMidFrameInfo.txt')
    can_lines = can_file.readlines()

frame = start_frame
mobile_dist = []
mobile_v = []
mobile_ttc = []


"""mobile主目标ID

测试序列1

zhong: '38','43'
zhong-1: '61'
zhong-2: '6'

测试序列2
20-50 : '25'
20-50-1 : '33'
20-50-2 : '41'
"""
local_dir = os.path.split(op_dir)[-1]
if local_dir == 'zhong':
    main_id = ['38','43']
elif local_dir == 'zhong-1':
    main_id = ['61']
elif local_dir == 'zhong-2':
    main_id = ['6']
elif local_dir == '20-50':
    main_id = ['25']
elif local_dir == '20-50-1':
    main_id =['33']
elif local_dir == '20-50-2':
    main_id = ['41']

n = len(can_lines)

while str(frame) != can_lines[0].split()[0]:
    print frame,can_lines[0].split()[0]
    mobile_dist.append(0)
    mobile_v.append(0)
    mobile_ttc.append(0)
    frame +=2


"""相对速度对比图"""
plt.figure(1,figsize=(12,4))
plt.title(u'相对速度变化曲线')
plt.xlabel(u'帧号')
plt.ylabel(u'相对速度(米/秒)')

plt.xlim(x[0],x[-1])
plt.ylim(-20,20)
plt.plot(x,can_y,label='can',color = 'b',ls='-')
plt.plot(x,Radar_v,label = 'Radar',color = 'g',ls='-')
plt.plot(x,testcase_v,label = 'Rontgen',color = 'r',ls='-')
plt.plot(x,mobile_v,label = 'mobileye',color = 'y',ls='-')
plt.legend()


"""距离对比图"""
plt.figure(2,figsize=(12,4))
plt.title(u'距离变化曲线')
plt.xlabel(u'帧号')
plt.ylabel(u'两车车距（米）')



plt.plot(x,Radar_dist,label = 'Radar',color = 'g',ls='-')
plt.plot(x,testcase_dist,label = 'Rontgen',color = 'r',ls='-')
plt.plot(x,mobile_dist,label = 'mobileye',color = 'y',ls='-')
plt.legend()

"""TTC变化对比图"""
plt.figure(3,figsize=(12,4))
plt.title(u'TTC变化曲线')
plt.xlabel(u'帧号')
plt.ylabel(u'碰撞时间（秒）')

# plt.xlim(33930,34030)
plt.ylim(-15,15)

plt.plot(x,Radar_ttc,label = 'Radar',color = 'g',ls='-')
plt.plot(x,testcase_ttc,label = 'Rontgen',color = 'r',ls='-')
plt.plot(x,mobile_ttc,label = 'mobileye',color = 'y',ls='-')
# plt.xticks(x,[])
plt.legend()

plt.show()
