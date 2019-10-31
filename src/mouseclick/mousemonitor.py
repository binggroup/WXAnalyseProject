# coding:utf-8

#    __author__ = 'Mark sinoberg'
#    __date__ = '2016/6/24'
#    __Desc__ = 简单的入门示例程序
import PyHook3
import pythoncom
from time import *
import os
import sys
import io
import win32api
import win32con
import win32gui
from ctypes import *
import time
# from threading import Thread
import _thread


#鼠标间隔时间
MOUSE_CLICK_SLEEP_TIME=0.5
MOUSE_X=0
MOUSE_Y=0

chartype = sys.getfilesystemencoding()  


VK_CODE = {
    'backspace':0x08,
    'tab':0x09,
    'clear':0x0C,
    'enter':0x0D,
    'shift':0x10,
    'ctrl':0x11,
    'alt':0x12,
    'pause':0x13,
    'caps_lock':0x14,
    'esc':0x1B,
    'spacebar':0x20,
    'page_up':0x21,
    'page_down':0x22,
    'end':0x23,
    'home':0x24,
    'left_arrow':0x25,
    'up_arrow':0x26,
    'right_arrow':0x27,
    'down_arrow':0x28,
    'select':0x29,
    'print':0x2A,
    'execute':0x2B,
    'print_screen':0x2C,
    'ins':0x2D,
    'del':0x2E,
    'help':0x2F,
    '0':0x30,
    '1':0x31,
    '2':0x32,
    '3':0x33,
    '4':0x34,
    '5':0x35,
    '6':0x36,
    '7':0x37,
    '8':0x38,
    '9':0x39,
    'a':0x41,
    'b':0x42,
    'c':0x43,
    'd':0x44,
    'e':0x45,
    'f':0x46,
    'g':0x47,
    'h':0x48,
    'i':0x49,
    'j':0x4A,
    'k':0x4B,
    'l':0x4C,
    'm':0x4D,
    'n':0x4E,
    'o':0x4F,
    'p':0x50,
    'q':0x51,
    'r':0x52,
    's':0x53,
    't':0x54,
    'u':0x55,
    'v':0x56,
    'w':0x57,
    'x':0x58,
    'y':0x59,
    'z':0x5A,
    'numpad_0':0x60,
    'numpad_1':0x61,
    'numpad_2':0x62,
    'numpad_3':0x63,
    'numpad_4':0x64,
    'numpad_5':0x65,
    'numpad_6':0x66,
    'numpad_7':0x67,
    'numpad_8':0x68,
    'numpad_9':0x69,
    'multiply_key':0x6A,
    'add_key':0x6B,
    'separator_key':0x6C,
    'subtract_key':0x6D,
    'decimal_key':0x6E,
    'divide_key':0x6F,
    'F1':0x70,
    'F2':0x71,
    'F3':0x72,
    'F4':0x73,
    'F5':0x74,
    'F6':0x75,
    'F7':0x76,
    'F8':0x77,
    'F9':0x78,
    'F10':0x79,
    'F11':0x7A,
    'F12':0x7B,
    'F13':0x7C,
    'F14':0x7D,
    'F15':0x7E,
    'F16':0x7F,
    'F17':0x80,
    'F18':0x81,
    'F19':0x82,
    'F20':0x83,
    'F21':0x84,
    'F22':0x85,
    'F23':0x86,
    'F24':0x87,
    'num_lock':0x90,
    'scroll_lock':0x91,
    'left_shift':0xA0,
    'right_shift ':0xA1,
    'left_control':0xA2,
    'right_control':0xA3,
    'left_menu':0xA4,
    'right_menu':0xA5,
    'browser_back':0xA6,
    'browser_forward':0xA7,
    'browser_refresh':0xA8,
    'browser_stop':0xA9,
    'browser_search':0xAA,
    'browser_favorites':0xAB,
    'browser_start_and_home':0xAC,
    'volume_mute':0xAD,
    'volume_Down':0xAE,
    'volume_up':0xAF,
    'next_track':0xB0,
    'previous_track':0xB1,
    'stop_media':0xB2,
    'play/pause_media':0xB3,
    'start_mail':0xB4,
    'select_media':0xB5,
    'start_application_1':0xB6,
    'start_application_2':0xB7,
    'attn_key':0xF6,
    'crsel_key':0xF7,
    'exsel_key':0xF8,
    'play_key':0xFA,
    'zoom_key':0xFB,
    'clear_key':0xFE,
    '+':0xBB,
    ',':0xBC,
    '-':0xBD,
    '.':0xBE,
    '/':0xBF,
    '`':0xC0,
    ';':0xBA,
    '[':0xDB,
    '\\':0xDC,
    ']':0xDD,
    "'":0xDE,
    '`':0xC0}
class POINT(Structure):
    _fields_ = [("x", c_ulong),("y", c_ulong)]
def get_mouse_point():
    po = POINT()
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)
def mouse_click(x=None,y=None):
    if not x is None and not y is None:
        mouse_move(x,y)
        time.sleep(MOUSE_CLICK_SLEEP_TIME)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def mouse_dclick(x=None,y=None):
    if not x is None and not y is None:
        mouse_move(x,y)
        time.sleep(MOUSE_CLICK_SLEEP_TIME)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
def mouse_move(x,y):
    windll.user32.SetCursorPos(x, y)
def key_input(str=''):
    for c in str:
        win32api.keybd_event(VK_CODE[c],0,0,0)
        win32api.keybd_event(VK_CODE[c],0,win32con.KEYEVENTF_KEYUP,0)
        time.sleep(MOUSE_CLICK_SLEEP_TIME)











# result = ''

def onMouseEvent(event):
    # 监听鼠标事件
#     print "Message Name :", event.MessageName
#     print "Message:",event.Message
#     print "Time: " , event.Time
#     print "Window: ",event.Window
#     print "Window Name : " ,event.WindowName
#     print "Position : ",event.Position
#     print "Wheel : ",event.Wheel
#     print "Injected: ",event.Injected
    # 需要注意的是返回True，以便将事件传给其他的处理程序，如果返回False的话，鼠标事件在这里就会被拦截，即鼠标会僵在此处失去响应
    return True

def onKeyboardEvent(event):
    # 监听键盘事件
#     print "MessageName:", event.MessageName
#     print "Message:", event.Message
#     print "Time:", event.Time
#     print "Window:", event.Window
#     print "WindowName:", event.WindowName
#     print "Ascii:", event.Ascii, chr(event.Ascii)
    print ("Key:", event.Key)
    print ("KeyID:", event.KeyID)
#     print "ScanCode:", event.ScanCode
#     print "Extended:", event.Extended
#     print "Injected:", event.Injected
#     print "Alt", event.Alt
#     print "Transition", event.Transition
#     print "---"
    
    if( str(event.Key) == 'Lcontrol' or str(event.Key) == 'Rcontrol' ):
        sys.exit(0)
#         os._exit(0)
    
    # 同鼠标事件监听函数的返回值
    # 写一个保存到本地文件的方法,而且应该以写二进制的方式来写入,设置result为全局的，避免文件被覆盖
#     global result
#     file = open(r'd:/temp/log.txt','wb')
#     result = result + "Time : " + str(asctime())+"|:"+"WindowName:"+str( event.WindowName)+"|"+"Key:"+str( event.Key)+"|"+"MessageName:"+str( event.MessageName)
#     file.writelines(result)
#     if event.Key == "q":
#         file.close()
    return True

def monitor_keyboard(str):
    # 创建一个：钩子“管理对象
    hm = PyHook3.HookManager()
    # 监听所有的键盘事件
    hm.KeyDown = onKeyboardEvent
    #设置键盘”钩子“
    hm.HookKeyboard()
    # 监听鼠标事件
#     hm.mouseAll = onMouseEvent
    # 设置鼠标钩子
#     hm.HookMouse()
    # 进入循环侦听，需要手动进行关闭，否则程序将一直处于监听的状态。可以直接设置而空而使用默认值
    pythoncom.PumpMessages()
    # 我也不知道为什么直接放置到main函数中不管用
    
def simulate_mouse_click(str):
    global MOUSE_X,MOUSE_Y
    for num in range(1,40000):        
        mouse_click(MOUSE_X,MOUSE_Y)
#         pythoncom.PumpMessages()
        time.sleep(MOUSE_CLICK_SLEEP_TIME)
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"=====",num,str)
#         print num,str

if __name__ == "__main__":    
    MOUSE_X,MOUSE_Y = get_mouse_point()
    print('鼠标位置:')
    print(MOUSE_X,MOUSE_Y)
#     try:
    _thread.start_new_thread( simulate_mouse_click, ("鼠标点击",) )
    _thread.start_new_thread( monitor_keyboard, ("键盘", ) )
#     except:
#         print("error...")
    
    while 1:
        print(u"主线程...")
        time.sleep(150)
        pass
    
    
