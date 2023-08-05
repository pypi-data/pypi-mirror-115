import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import re
from struct import unpack,pack
import time
import ctypes
from typing import Tuple, Optional, Callable, Any
import asyncio

import snap7
import snap7.types
from snap7.common import check_error, load_library, ipv4

import threading
import numpy as np

# import logging
# logging.basicConfig(level = logging.INFO)
# logger = logging.getLogger(__name__)

def rotate(origin_pos,pos,degree):
    from math import pi,cos,sin
    a = pi / 180 * degree
    x2 = (pos[0] - origin_pos[0]) * cos(a) - (pos[1] - origin_pos[1]) * sin(a) + origin_pos[0]
    y2 = (pos[1] - origin_pos[1]) * cos(a) + (pos[0] - origin_pos[0]) * sin(a) + origin_pos[1]
    return x2,y2


class Truss():
    def __init__(self,name,port,area_x,area_y,area_z):
        self.area_x,self.area_y,self.area_z = area_x,area_y,area_z

        self.server = snap7.server.Server()
        self.dbs = dict()
        self.db0 = (snap7.types.wordlen_to_ctypes[snap7.types.S7WLByte] * 200)()
        self.db1 = (snap7.types.wordlen_to_ctypes[snap7.types.S7WLByte] * 200)()
        self.server.register_area(snap7.types.srvAreaDB, 0, self.db0)
        self.server.register_area(snap7.types.srvAreaDB, 1, self.db1)
        self.server.start(tcpport=port)

        self.name = name
        self.graph = plt.figure(name)
        self.view = self.graph.add_subplot(111,projection='3d')
        plt.show(block=False)
        plt.ion()

        self.loop = asyncio.get_event_loop()
        pass
    def __del__(self):
        plt.ioff()
        pass
    def power_on(self):
        self.db0[0] = 88 # A
        self.db0[1] = 88 # B
        self.db1[34] = 0b00000010 # fault,writeable,paused,safe_a,safe_b,finished_a,finished_b,synced
        
        self.x = [self.area_x[0],self.area_x[1]]
        self.y = [self.area_y[0],self.area_y[0]]
        self.z = [self.area_z[1],self.area_z[1]]
        self.r = [0,0]
        
        self.db1[2],self.db1[3],self.db1[4],self.db1[5] = pack('!f',self.x[0])
        self.db1[6],self.db1[7],self.db1[8],self.db1[9] = pack('!f',self.y[0])        
        self.db1[10],self.db1[11],self.db1[12],self.db1[13] = pack('!f',self.z[0])
        self.db1[18],self.db1[19],self.db1[20],self.db1[21] = pack('!f',self.x[1])
        self.db1[22],self.db1[23],self.db1[24],self.db1[25] = pack('!f',self.y[1])
        self.db1[26],self.db1[27],self.db1[28],self.db1[29] = pack('!f',self.z[1])
        pass
    def emergency_stop(self):
        self.db0[0] = 0 # A
        self.db0[1] = 0 # B
        pass
    def pause(self):
        pass
    def reset(self):
        pass
    def manual(self):
        pass
    async def moving_x(self,index):
        if index == 0:
            end = unpack('!f',pack('4b',self.db0[38],self.db0[39],self.db0[40],self.db0[41]))[0]
            start = unpack('!f',pack('4b',self.db1[2],self.db1[3],self.db1[4],self.db1[5]))[0]
        elif index == 1:
            end = unpack('!f',pack('4b',self.db0[70],self.db0[71],self.db0[72],self.db0[73]))[0]
            start = unpack('!f',pack('4b',self.db1[18],self.db1[19],self.db1[20],self.db1[21]))[0]

        for interval in np.linspace(start,end,int(abs(start - end) / 100)):
            if index == 0: self.db1[2],self.db1[3],self.db1[4],self.db1[5] = pack('!f',interval)
            elif index == 1: self.db1[18],self.db1[19],self.db1[20],self.db1[21] = pack('!f',interval)
            self.x[index] = interval
            await asyncio.sleep(0.01)
        pass
    async def moving_y(self,index):
        if index == 0:
            end = unpack('!f',pack('4b',self.db0[42],self.db0[43],self.db0[44],self.db0[45]))[0]
            start = unpack('!f',pack('4b',self.db1[6],self.db1[7],self.db1[8],self.db1[9]))[0]
        elif index == 1:
            end = unpack('!f',pack('4b',self.db0[74],self.db0[75],self.db0[76],self.db0[77]))[0]
            start = unpack('!f',pack('4b',self.db1[22],self.db1[23],self.db1[24],self.db1[25]))[0]
        for interval in np.linspace(start,end,int(abs(start - end) / 100)):
            if index == 0: self.db1[6],self.db1[7],self.db1[8],self.db1[9] = pack('!f',interval)
            elif index == 1: self.db1[22],self.db1[23],self.db1[24],self.db1[25] = pack('!f',interval)
            self.y[index] = interval
            await asyncio.sleep(0.01)
        pass
    async def moving_z(self,index):
        if index == 0:
            end = unpack('!f',pack('4b',self.db0[46],self.db0[47],self.db0[48],self.db0[49]))[0]
            start = unpack('!f',pack('4b',self.db1[10],self.db1[11],self.db1[12],self.db1[13]))[0]
        elif index == 1:
            end = unpack('!f',pack('4b',self.db0[78],self.db0[79],self.db0[80],self.db0[81]))[0]
            start = unpack('!f',pack('4b',self.db1[26],self.db1[27],self.db1[28],self.db1[29]))[0]
        for interval in np.linspace(start,end,int(abs(start - end) / 10)):
            if index == 0: self.db1[10],self.db1[11],self.db1[12],self.db1[13] = pack('!f',interval)
            elif index == 1: self.db1[26],self.db1[27],self.db1[28],self.db1[29] = pack('!f',interval)
            self.z[index] = interval
            await asyncio.sleep(0.001)
    async def moving_r(self,index):
        if index == 0:
            end = unpack('!f',pack('4b',self.db0[50],self.db0[51],self.db0[52],self.db0[53]))[0]
            start = unpack('!f',pack('4b',self.db1[14],self.db1[15],self.db1[16],self.db1[17]))[0]
        elif index == 1:
            end = unpack('!f',pack('4b',self.db0[82],self.db0[83],self.db0[84],self.db0[85]))[0]
            start = unpack('!f',pack('4b',self.db1[30],self.db1[31],self.db1[32],self.db1[33]))[0]
        for interval in np.linspace(start,end,int(abs(start - end) / 10)):
            if index == 0: self.db1[14],self.db1[15],self.db1[16],self.db1[17] = pack('!f',interval)
            elif index == 1: self.db1[30],self.db1[31],self.db1[32],self.db1[33] = pack('!f',interval)
            self.r[index] = interval
            await asyncio.sleep(0.001)
    async def picking(self,index,synced,index2):
        if index == 0:
            x_start = unpack('!f',pack('4b',self.db1[2],self.db1[3],self.db1[4],self.db1[5]))[0]
            y_start = unpack('!f',pack('4b',self.db1[6],self.db1[7],self.db1[8],self.db1[9]))[0]
            z_start = unpack('!f',pack('4b',self.db1[10],self.db1[11],self.db1[12],self.db1[13]))[0]
            r_start = unpack('!f',pack('4b',self.db1[14],self.db1[15],self.db1[16],self.db1[17]))[0]
            x_end = unpack('!f',pack('4b',self.db0[38],self.db0[39],self.db0[40],self.db0[41]))[0]
            y_end = unpack('!f',pack('4b',self.db0[42],self.db0[43],self.db0[44],self.db0[45]))[0]
            z_end = unpack('!f',pack('4b',self.db0[46],self.db0[47],self.db0[48],self.db0[49]))[0]
            r_end = unpack('!f',pack('4b',self.db0[50],self.db0[51],self.db0[52],self.db0[53]))[0]
            x2_end = unpack('!f',pack('4b',self.db0[54],self.db0[55],self.db0[56],self.db0[57]))[0]
            y2_end = unpack('!f',pack('4b',self.db0[58],self.db0[59],self.db0[60],self.db0[61]))[0]
            z2_end = unpack('!f',pack('4b',self.db0[62],self.db0[63],self.db0[64],self.db0[65]))[0]
            r2_end = unpack('!f',pack('4b',self.db0[66],self.db0[67],self.db0[68],self.db0[69]))[0]
        elif index == 1:
            x_start = unpack('!f',pack('4b',self.db1[18],self.db1[19],self.db1[20],self.db1[21]))[0]
            y_start = unpack('!f',pack('4b',self.db1[22],self.db1[23],self.db1[24],self.db1[25]))[0]
            z_start = unpack('!f',pack('4b',self.db1[26],self.db1[27],self.db1[28],self.db1[29]))[0]
            r_start = unpack('!f',pack('4b',self.db1[30],self.db1[31],self.db1[32],self.db1[33]))[0]
            x_end = unpack('!f',pack('4b',self.db0[70],self.db0[71],self.db0[72],self.db0[73]))[0]
            y_end = unpack('!f',pack('4b',self.db0[74],self.db0[75],self.db0[76],self.db0[77]))[0]
            z_end = unpack('!f',pack('4b',self.db0[78],self.db0[79],self.db0[80],self.db0[81]))[0]
            r_end = unpack('!f',pack('4b',self.db0[82],self.db0[83],self.db0[84],self.db0[85]))[0]
            x2_end = unpack('!f',pack('4b',self.db0[86],self.db0[87],self.db0[88],self.db0[89]))[0]
            y2_end = unpack('!f',pack('4b',self.db0[90],self.db0[91],self.db0[92],self.db0[93]))[0]
            z2_end = unpack('!f',pack('4b',self.db0[94],self.db0[95],self.db0[96],self.db0[97]))[0]
            r2_end = unpack('!f',pack('4b',self.db0[98],self.db0[99],self.db0[100],self.db0[101]))[0]

        async def x(self,start,end):
            for interval in np.linspace(start,end,int(abs(start - end) / 100)):
                if index == 0: self.db1[2],self.db1[3],self.db1[4],self.db1[5] = pack('!f',interval)
                elif index == 1: self.db1[18],self.db1[19],self.db1[20],self.db1[21] = pack('!f',interval)
                self.x[index] = interval
                await asyncio.sleep(0.01)
        async def y(self,start,end):
            for interval in np.linspace(start,end,int(abs(start - end) / 100)):
                if index == 0: self.db1[6],self.db1[7],self.db1[8],self.db1[9] = pack('!f',interval)
                elif index == 1: self.db1[22],self.db1[23],self.db1[24],self.db1[25] = pack('!f',interval)
                self.y[index] = interval
                await asyncio.sleep(0.01)
        async def z(self,start,end):
            for interval in np.linspace(start,end,int(abs(start - end) / 10)):
                if index == 0: self.db1[10],self.db1[11],self.db1[12],self.db1[13] = pack('!f',interval)
                elif index == 1: self.db1[26],self.db1[27],self.db1[28],self.db1[29] = pack('!f',interval)
                self.z[index] = interval
                await asyncio.sleep(0.001)
        async def r(self,start,end):
            for interval in np.linspace(start,end,int(abs(start - end) / 10)):
                if index == 0: self.db1[14],self.db1[15],self.db1[16],self.db1[17] = pack('!f',interval)
                elif index == 1: self.db1[30],self.db1[31],self.db1[32],self.db1[33] = pack('!f',interval)
                self.r[index] = interval
                await asyncio.sleep(0.001)

        await self.loop.create_task(asyncio.wait([x(self,x_start,x_end),y(self,y_start,y_end),r(self,r_start,r_end)]))
        if synced: 
            synced[index] = 1
            while synced[index] > synced[index2]: await asyncio.sleep(0.1)
        await self.loop.create_task(z(self,z_start,z_end))
        if synced: 
            synced[index] = 2
            while synced[index] > synced[index2]: await asyncio.sleep(0.1)
        await self.loop.create_task(z(self,z_end,self.area_z[1]))

        if synced: 
            synced[index]= 3
            while synced[index] > synced[index2]: await asyncio.sleep(0.1)
        await self.loop.create_task(asyncio.wait([x(self,x_end,x2_end),y(self,y_end,y2_end),r(self,r_end,r2_end)]))

        if synced: 
            synced[index] = 4
            while synced[index] > synced[index2]: await asyncio.sleep(0.1)
        await self.loop.create_task(z(self,self.area_z[1],z2_end))

        if synced: 
            synced[index] = 5
            while synced[index] > synced[index2]: await asyncio.sleep(0.1)
        await self.loop.create_task(z(self,z2_end,self.area_z[1]))

        if synced: 
            synced[index] = 6
            while synced[index] > synced[index2]: await asyncio.sleep(0.1)
        pass
    async def update(self):
        if not plt.fignum_exists(self.name):
            print('终止！')
            self.loop.stop()
            return
            
        while True:
            event = self.server.pick_event()
            if not event: break

            request = self.server.event_text(event)
            print(request)
            m = re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2} \[[\d]+\.[\d]+\.[\d]+.[\d]+\] (\w+) request, Area : DB(\d+), Start : (\d+), Size : (\d+) --> OK',request)
            if not m: continue
            command = m.group(1)
            area = int(m.group(2))
            index = int(m.group(3))
            size = int(m.group(4))
            if command != 'Write': continue
            if index > 1: continue
            action = self.db0[index]

            from functools import partial
            def finish(db,index,f):
                db[index] = 88

            if action == 12:
                print('升降指令')
                self.loop.create_task(self.moving_z(index)).add_done_callback(partial(finish,self.db0,index))
                pass
            elif action == 11:
                print('平移指令')
                self.loop.create_task(
                    asyncio.wait([
                            self.loop.create_task(self.moving_x(index)),
                            self.loop.create_task(self.moving_y(index)),
                            self.loop.create_task(self.moving_r(index))
                        ])).add_done_callback(partial(finish,self.db0,index))
                pass
            elif action == 1:
                print('单臂抓取指令')
                self.loop.create_task(self.picking(index,None,None)).add_done_callback(partial(finish,self.db0,index))
                pass
            elif action == 2:
                print('双臂抓取指令')
                synced = [0,0]
                self.loop.create_task(self.picking(0,synced,1)).add_done_callback(partial(finish,self.db0,0))
                self.loop.create_task(self.picking(1,synced,0)).add_done_callback(partial(finish,self.db0,1))
                pass
            elif action == 3:
                print('复位指令')
                if index == 0:
                    self.db0[38],self.db0[39],self.db0[40],self.db0[41] = pack('!f',3400)
                    self.db0[42],self.db0[43],self.db0[44],self.db0[45] = pack('!f',self.area_y[0])
                    self.db0[46],self.db0[47],self.db0[48],self.db0[49] = pack('!f',self.area_z[1])
                    self.db0[50],self.db0[51],self.db0[52],self.db0[53] = pack('!f',0)
                elif index == 1:
                    self.db0[70],self.db0[71],self.db0[72],self.db0[73] = pack('!f',3200)
                    self.db0[74],self.db0[75],self.db0[76],self.db0[77] = pack('!f',self.area_y[0])
                    self.db0[78],self.db0[79],self.db0[80],self.db0[81] = pack('!f',self.area_z[1])
                    self.db0[82],self.db0[83],self.db0[85],self.db0[85] = pack('!f',0)

                self.loop.create_task(
                    asyncio.wait([
                            self.loop.create_task(self.moving_x(index)),
                            self.loop.create_task(self.moving_y(index)),
                            self.loop.create_task(self.moving_z(index)),
                            self.loop.create_task(self.moving_r(index))
                        ])).add_done_callback(partial(finish,self.db0,index))
                pass
        self.view.cla()

        #区域
        self.view.text(self.area_x[1],0,0,'X')
        self.view.text(0,self.area_y[1],0,'Y')
        self.view.text(0,0,self.area_z[1],'Z')
        self.view.plot([self.area_x[0]-750,self.area_x[1]+750],[0,0],[0,0])
        self.view.plot([0,0],self.area_y,[0,0])
        self.view.plot([0,0],[0,0],[self.area_z[0],self.area_z[1]])

        #桁架
        self.view.plot([self.x[0],self.x[0]],[self.area_y[0],self.area_y[1]],[self.area_z[1],self.area_z[1]],c='red')
        self.view.plot([self.x[1],self.x[1]],[self.area_y[0],self.area_y[1]],[self.area_z[1],self.area_z[1]],c='red')

        #抓手
        self.view.plot([self.x[0],self.x[0]],[self.y[0],self.y[0]],[self.z[0],self.area_z[1]],c='red')
        self.view.plot([self.x[1],self.x[1]],[self.y[1],self.y[1]],[self.z[1],self.area_z[1]],c='red')
        
        x0,y0=rotate([self.x[0],self.y[0]],[self.x[0]-750,self.y[0]],-self.r[0])
        x1,y1=rotate([self.x[0],self.y[0]],[self.x[0]+750,self.y[0]],-self.r[0])
        self.view.plot([x0,x1],[y0,y1],[self.z[0],self.z[0]],c='blue')

        x0,y0=rotate([self.x[1],self.y[1]],[self.x[1]-750,self.y[1]],-self.r[1])
        x1,y1=rotate([self.x[1],self.y[1]],[self.x[1]+750,self.y[1]],-self.r[1])
        self.view.plot([x0,x1],[y0,y1],[self.z[1],self.z[1]],c='blue')

        self.view.text(self.x[0],self.y[0],self.z[0],str([int(self.x[0]),int(self.y[0]),int(self.z[0]),int(self.r[0])]))
        self.view.text(self.x[1],self.y[1],self.z[1],str([int(self.x[1]),int(self.y[1]),int(self.z[1]),int(self.r[1])]))

        self.graph.canvas.draw()
        self.graph.canvas.flush_events()
        await asyncio.sleep(0.001)
        
        self.loop.create_task(self.update())
    def show(self):
        self.loop.create_task(self.update())
        self.loop.run_forever()
        pass
