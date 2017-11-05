# -*- coding: utf-8 -*-

import  math

class can_date_pretreatment():
    def __init__(self,can_txt):
        self.can_txt = can_txt
        self.start_frame = 0
    """将can信息中的mobile信息提取出来"""
    def mbl_pretreatment(self):
        mbl_can = []
        if self.start_frame !=0:
            start_frame = self.start_frame
        else:
            start_frame = int(self.can_txt[0].split()[0])

        """这里需要处理丢帧和帧重复"""

        end_frame = int(self.can_txt[-1].split()[0])
        num = start_frame
        loc = 0
        while num < end_frame:
            frame = int(self.can_txt[loc].split()[0])
            mbl_can_line = []
            if frame < num:
                loc +=1
                continue
            elif frame == num:
                mbl_can_line = []
                can_line = self.can_txt[loc].split()[1:]
                n_can_line = self.can_txt[loc+1].split()[1:]
                mbl_can_line.append(str(frame))
                """当前程序用到的mobileye的ID，0x700,0x738,0x737,0x669"""
                # mbl_canid = [str(int(0x669)),str(int(0x700)),str(int(0x737)),str(int(0x738))]
                """AWS的id是 0x700"""
                aws_canid = str(int(0x700))
                if aws_canid in can_line:
                    aws_loc = int(can_line.index(aws_canid))
                    aws_count = int(can_line[aws_loc+1])
                    aws_date = can_line[aws_loc:aws_loc+aws_count+2]
                else:
                    aws_date = [0]
                mbl_can_line.append(aws_date)
                """Obstacle的数量id是0x738"""
                obs_canid = str(int(0x738))
                if obs_canid in can_line:
                    obs_loc = int(can_line.index(obs_canid))
                    num_obs = int(can_line[obs_loc+2])
                    """实际的Obstacle的ID是0x739开始"""
                    if num_obs == 0:
                        obs_dates = [0]
                    else:
                        obs_dates = []
                        for i in range(0,num_obs,1):
                            obs_a_id = str(0x739+i*3)
                            obs_b_id = str(0x73A+i*3)
                            obs_c_id = str(0x73B+i*3)
                            if obs_a_id in can_line:
                                obs_a_loc = int(can_line.index(obs_a_id))
                                obs_a_date = can_line[obs_a_loc:obs_a_loc+10]
                            elif obs_a_id in n_can_line:
                                obs_a_loc = int(n_can_line.index(obs_a_id))
                                obs_a_date = n_can_line[obs_a_loc:obs_a_loc + 10]
                                del self.can_txt[loc+1].split()[obs_a_loc:obs_a_loc + 10]
                            else:
                                obs_a_date = [0]
                            if obs_b_id in can_line:
                                obs_b_loc = int(can_line.index(obs_b_id))
                                obs_b_date = can_line[obs_b_loc:obs_b_loc + 10]
                            elif obs_b_id in n_can_line:
                                obs_b_loc = int(n_can_line.index(obs_b_id))
                                obs_b_date = n_can_line[obs_b_loc:obs_b_loc + 10]
                                del self.can_txt[loc+1].split()[obs_b_loc:obs_b_loc + 10]
                            else:
                                obs_b_date = [0]
                            if obs_c_id in can_line:
                                obs_c_loc = int(can_line.index(obs_c_id))
                                obs_c_date = can_line[obs_c_loc:obs_c_loc + 10]
                            elif obs_c_id in n_can_line:
                                obs_c_loc = int(n_can_line.index(obs_c_id))
                                obs_c_date = n_can_line[obs_c_loc:obs_c_loc + 10]
                                del self.can_txt[loc+1].split()[obs_c_loc:obs_c_loc + 10]
                            else:
                                obs_c_date = [0]
                            if obs_a_date !=[0] or obs_b_date != [0] or obs_c_date != [0]:
                                obs_date = obs_a_date + obs_b_date + obs_c_date
                            obs_dates.append(obs_date)
                else: obs_dates = [0]
                mbl_can_line.append(obs_dates)
                """Lane的id是0x737和0x669"""
                lane1_canid = str(int(0x669))
                lane2_canid = str(int(0x737))
                if lane1_canid in can_line:
                    lane1_loc = int(can_line.index(lane1_canid))
                    lane1_date = can_line[lane1_loc:lane1_loc+10]
                else:
                    lane1_date = [0]
                if lane2_canid in can_line:
                    lane2_loc = int(can_line.index(lane2_canid))
                    lane2_date = can_line[lane2_loc:lane2_loc+10]
                elif lane2_canid in n_can_line:
                    lane2_loc = int(n_can_line.index(lane2_canid))
                    lane2_date = n_can_line[lane2_loc:lane2_loc+10]
                    del self.can_txt[loc + 1].split()[lane2_loc:lane2_loc+10]
                else:
                    lane2_date = [0]
                if lane1_date == [0] or lane2_date == [0]:
                    lane_date = [0]
                else:
                    lane_date = lane1_date+lane2_date
                mbl_can_line.append(lane_date)
                mbl_can.append(mbl_can_line)
                num +=2
                loc +=1
            else:
                mbl_can_line.append(str(num))
                mbl_can_line.append(aws_date)
                mbl_can_line.append(obs_dates)
                mbl_can_line.append(lane_date)
                mbl_can.append(mbl_can_line)
                num += 2
        return mbl_can
    """将can信息中ESR雷达信息提取出来"""
    def esr_pretreatment(self):
        esr_can_txt = []
        if self.start_frame != 0:
            start_frame = self.start_frame
            end_frame = int(self.can_txt[-1].split()[0])
        else:
            start_frame = int(self.can_txt[0].split()[0])
            end_frame = int(self.can_txt[-1].split()[0])
        num = start_frame
        loc = 0
        """这里需要处理丢帧和帧重复"""
        while num < end_frame:
            print ('%d%%'%(float(loc)/float(len(self.can_txt))*100))
            esr_canline = self.can_txt[loc].split()
            n_esr_canline = self.can_txt[loc+1].split()
            frame = int(self.can_txt[loc].split()[0])
            esr_can_line = []
            if frame < num:
                loc += 1
                continue
            elif frame == num:
                """雷达的can信息ID从0x500到0x53F"""
                esr_can_line.append(frame)
                can_id = int(0x500)
                can_date = []
                while can_id <= int(0x53F):
                    if str(can_id) in esr_canline:
                        esr_loc = int(esr_canline.index(str(can_id)))
                        can_date += esr_canline[esr_loc:esr_loc+10]
                        del self.can_txt[loc].split()[1:esr_loc+10]
                        can_id +=1
                    elif str(can_id) in n_esr_canline:
                        esr_loc = int(n_esr_canline.index(str(can_id)))
                        can_date += n_esr_canline[esr_loc:esr_loc + 10]
                        del self.can_txt[loc+1].split()[1:esr_loc + 10]
                        can_id += 1
                    else:
                        can_date += ['false']
                        break
                if 'false' in can_date:
                    esr_can_line +=[0]
                else:
                    esr_can_line +=can_date
                esr_can_txt.append(esr_can_line)
                num += 2
                loc += 1
            else:
                esr_can_line.append(num)
                if 'false' in can_date:
                    esr_can_line +=[0]
                else:
                    esr_can_line +=can_date
                esr_can_txt.append(esr_can_line)
                num += 2
        return  esr_can_txt
















