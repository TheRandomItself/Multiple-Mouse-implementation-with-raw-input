import ctypes as cts
import ctypes.wintypes as wts
from pickle import TRUE
import sys
import time
import pyautogui
import time
import mouse

import ctypes_wrappers as cws
import win32gui, win32ui

import win32api
import win32con
from win32api import GetSystemMetrics

dc = win32gui.GetDC(0)
dcObj = win32ui.CreateDCFromHandle(dc)

HWND_MESSAGE = -3

WM_QUIT = 0x0012
WM_INPUT = 0x00FF
WM_KEYUP = 0x0101
WM_CHAR = 0x0102

HID_USAGE_PAGE_GENERIC = 0x01

RIDEV_NOLEGACY = 0x00000030
RIDEV_INPUTSINK = 0x00000100
RIDEV_CAPTUREMOUSE = 0x00000200

RID_HEADER = 0x10000005
RID_INPUT = 0x10000003

RIM_TYPEMOUSE = 0
RIM_TYPEKEYBOARD = 1
RIM_TYPEHID = 2
HIDDEN_COORDINATES = (1175, 1056)

PM_NOREMOVE = 0x0000
MAX_FREQUENCY = 50
mouse_devices = []
mouse_devices_coordinates = []
keyboard_devices = []
is_clicked_device = []

curr_frequency = []
last_mouse = []
timeout = []
msg_frequency = []
changed = []
mouse_frequency = []

def wnd_proc(hwnd, msg, wparam, lparam):
    if msg_frequency[0] >= 0:
        
        #msg_frequency[0] = 0
    #print(f"Handle message - hwnd: 0x{hwnd:016X} msg: 0x{msg:08X} wp: 0x{wparam:016X} lp: 0x{lparam:016X}")
        if msg == WM_INPUT:
            coordinates = mouse.get_position()
            if mouse_frequency[0] >= 1000:
                
                if len(mouse_devices_coordinates) > 0:
                    coorx = mouse_devices_coordinates[0]["x"]
                    coory = mouse_devices_coordinates[0]["y"]
                    mouse.move(coorx, coory)
                #if coordinates[0] != HIDDEN_COORDINATES[0] or coordinates[1] != HIDDEN_COORDINATES[1]:
                #    mouse.move(HIDDEN_COORDINATES[0], HIDDEN_COORDINATES[1])
                mouse_frequency[0] = 0

            if len(changed) > 0:
                changed[0] = 1
            size = wts.UINT(0)
            res = cws.GetRawInputData(cts.cast(lparam, cws.PRAWINPUT), RID_INPUT, None, cts.byref(size), cts.sizeof(cws.RAWINPUTHEADER))
            if res == wts.UINT(-1) or size == 0:
                #print_error(text="GetRawInputData 0")
                return 0
            buf = cts.create_string_buffer(size.value)
            res = cws.GetRawInputData(cts.cast(lparam, cws.PRAWINPUT), RID_INPUT, buf, cts.byref(size), cts.sizeof(cws.RAWINPUTHEADER))
            if res != size.value:
                #print_error(text="GetRawInputData 1")
                return 0
            #print("kkt: ", cts.cast(lparam, cws.PRAWINPUT).contents.to_string())
            ri = cts.cast(buf, cws.PRAWINPUT).contents
            #print(ri.to_string())
            head = ri.header
            print(head.to_string())
            print(head.hDevice) #works for some reason
        
            print(ri.data.mouse.to_string())
            #print(ri.data.keyboard.to_string())
            #print(ri.data.hid.to_string())

            #print(mouse_devices)
            #print(keyboard_devices)
            #print(mouse_devices_coordinates)
            device_index = 0
            if head.dwType == RIM_TYPEMOUSE:
                
                if head.hDevice != None:
                    if len(last_mouse) == 0:
                        last_mouse.append(head.hDevice)
                    if len(curr_frequency) == 0:
                        curr_frequency.append(0)
                    curr_frequency[0] += 1
                    data = ri.data.mouse

                    #------------------------------------------------------------------
                    #------------------------------------------------------------------
                    #coordinates = pyautogui.position()
                    #print(coordinates[0])
                    #print(coordinates[1])
                    #print(data.lLastX)
                    #print(data.lLastY)
                    i = 0
                    found = False
                    print(mouse_devices)
                    while i < len(mouse_devices):
                        if mouse_devices[i] == head.hDevice:
                            found = True
                            device_index = i
                        
                        i = i + 1
                    if found == False:
                        mouse_devices.append(head.hDevice)
                        device_index = len(mouse_devices) - 1
                        changed.append(1)
                        is_clicked_device.append(False)
                        mouse_devices_coordinates.append({"x" : coordinates[0], "y" : coordinates[1]})
                    else:
                        if data.ulButtons == 2:
                            coord_x = mouse_devices_coordinates[device_index]["x"]
                            coord_y = mouse_devices_coordinates[device_index]["y"]
                            if not ((coord_x >= coordinates[0] - 5 and coord_x <= coordinates[0] + 5) and (coord_y >= coordinates[1] - 5 and coord_y <= coordinates[1] + 5)):
                                mouse.move(coord_x, coord_y)
                                mouse.click()
                            #mouse.move(HIDDEN_COORDINATES[0], HIDDEN_COORDINATES[1])
                            #mouse.click()
                            #win32api.SetCursorPos((coord_x,coord_y))
                            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,coord_x,coord_y,0,0)
                            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,coord_x,coord_y,0,0)
                            #print(data.lLastX)
                            #print(data.lLastY)
                        changed[device_index] = 1
                        mouse_devices_coordinates[device_index]["x"] = mouse_devices_coordinates[device_index]["x"] + data.lLastX
                        mouse_devices_coordinates[device_index]["y"] = mouse_devices_coordinates[device_index]["y"] + data.lLastY
                    
                    print(mouse_devices_coordinates[device_index])

                    #if curr_frequency[0] >= MAX_FREQUENCY:
                    #    pyautogui.moveTo(mouse_devices_coordinates[device_index]["x"], mouse_devices_coordinates[device_index]["y"])
                    #    curr_frequency[0] = 0
                    '''
                    if last_mouse[0] != head.hDevice and time.time() - timeout[0] >= 1:
                        pyautogui.moveTo(mouse_devices_coordinates[device_index]["x"], mouse_devices_coordinates[device_index]["y"])
                        timeout[0] = time.time()
                        last_mouse[0] = head.hDevice
                    '''
                    #m = win32gui.GetCursorPos()
                    '''
                    x_coord = mouse_devices_coordinates[device_index]["x"]
                    y_coord = mouse_devices_coordinates[device_index]["y"]
                    dcObj.Rectangle((x_coord, y_coord, x_coord+30, y_coord+10))
                    hwnd2 = win32gui.WindowFromPoint((0,0))
                    monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))
                    win32gui.InvalidateRect(hwnd2, monitor, True) # Refresh the entire monitor
                    '''
                #------------------------------------------------------------------
                #------------------------------------------------------------------

            
            
            
            elif head.dwType == RIM_TYPEKEYBOARD:
                #------------------------------------------------------------------
                #------------------------------------------------------------------
                i = 0
                found = False
                while i < len(keyboard_devices):
                    if keyboard_devices[i] == head.hDevice:
                        found = True
                        device_index = i
                    i = i + 1
                if found == False:
                    keyboard_devices.append(head.hDevice)
                    device_index = len(keyboard_devices) - 1
                #------------------------------------------------------------------
                #------------------------------------------------------------------
                data = ri.data.keyboard
                if data.VKey == 0x1B:
                    cws.PostQuitMessage(0)

            
            elif head.dwType == RIM_TYPEHID:
                data = ri.data.hid
            else:
                print("Wrong raw input type!!!")
                return 0
            #print(data.to_string())
        
        
    #msg_frequency[0] = msg_frequency[0] + 1   
    return cws.DefWindowProc(hwnd, msg, wparam, lparam)


def print_error(code=None, text=None):
    text = text + " - e" if text else "E"
    code = cws.GetLastError() if code is None else code
    #print(f"{text}rror code: {code}")


def register_devices(hwnd=None):
    flags = RIDEV_INPUTSINK  # @TODO - cfati: If setting to 0, GetMessage hangs
    generic_usage_ids = (0x01, 0x02, 0x04, 0x05, 0x06, 0x07, 0x08)
    devices = (cws.RawInputDevice * len(generic_usage_ids))(
        *(cws.RawInputDevice(HID_USAGE_PAGE_GENERIC, uid, flags, hwnd) for uid in generic_usage_ids)
    )
    #for d in devices: print(d.usUsagePage, d.usUsage, d.dwFlags, d.hwndTarget)
    if cws.RegisterRawInputDevices(devices, len(generic_usage_ids), cts.sizeof(cws.RawInputDevice)):
        print("Successfully registered input device(s)!")
        return True
    else:
        print_error(text="RegisterRawInputDevices")
        return False


def main(*argv):
    mouse_frequency.append(0)
    msg_frequency.append(0)
    timeout.append(0)
    wnd_cls = "SO049572093_RawInputWndClass"
    wcx = cws.WNDCLASSEX()
    wcx.cbSize = cts.sizeof(cws.WNDCLASSEX)
    #wcx.lpfnWndProc = cts.cast(cws.DefWindowProc, cts.c_void_p)
    wcx.lpfnWndProc = cws.WNDPROC(wnd_proc)
    wcx.hInstance = cws.GetModuleHandle(None)
    wcx.lpszClassName = wnd_cls
    #print(dir(wcx))
    res = cws.RegisterClassEx(cts.byref(wcx))
    if not res:
        print_error(text="RegisterClass")
        return 0
    hwnd = cws.CreateWindowEx(0, wnd_cls, None, 0, 0, 0, 0, 0, 0, None, wcx.hInstance, None)
    if not hwnd:
        print_error(text="CreateWindowEx")
        return 0
    #print("hwnd:", hwnd)
    if not register_devices(hwnd):
        return 0
    msg = wts.MSG()
    pmsg = cts.byref(msg)
    print("Start loop (press <ESC> to exit)...")
    drawing_frequency = 0
    drawing_ligher_frequency = 0
    while 1==1:
        #print("yo wassup")
        if mouse_frequency[0] >= 1000:
            coordinates = mouse.get_position()
            if len(mouse_devices_coordinates) > 0:
                coorx = mouse_devices_coordinates[0]["x"]
                coory = mouse_devices_coordinates[0]["y"]
                mouse.move(coorx, coory)
            #if coordinates[0] != HIDDEN_COORDINATES[0] or coordinates[1] != HIDDEN_COORDINATES[1]:
             #   mouse.move(HIDDEN_COORDINATES[0], HIDDEN_COORDINATES[1])
            mouse_frequency[0] = 0

        if drawing_frequency >= 100:
            
            drawing_frequency = 0
            refresh = False
            index = 0
            while index < len(changed):
                if changed[index] == 1:
                    changed[index] = 0
                    refresh = True
                index += 1
            
            #refresh = True
            if refresh or drawing_ligher_frequency >= 1000:
                drawing_ligher_frequency = 0
                hwnd2 = win32gui.WindowFromPoint((0,0))
                monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))
                win32gui.InvalidateRect(hwnd2, monitor, True) # Refresh the entire monitor

                index = 0
                while index < len(mouse_devices): #drawing the rectangles again
                    #print("changed device")
                    x_coord = mouse_devices_coordinates[index]["x"]
                    y_coord = mouse_devices_coordinates[index]["y"]
                    dcObj.Rectangle((x_coord, y_coord, x_coord+20, y_coord+20))
                    
                    index = index + 1
                

            
        drawing_frequency += 1
        mouse_frequency[0] += 1
        drawing_ligher_frequency += 1

        if res := cws.PeekMessage(pmsg, None, 0, 0, 0x0001):
            if res < 0:
                print_error(text="GetMessage")
                break
            cws.TranslateMessage(pmsg)
            cws.DispatchMessage(pmsg)
        
        


if __name__ == "__main__":
    print("Python {:s} {:03d}bit on {:s}\n".format(" ".join(elem.strip() for elem in sys.version.split("\n")),
                                                    64 if sys.maxsize > 0x100000000 else 32, sys.platform))
    rc = main(*sys.argv[1:])
    print("\nDone.\n")
    sys.exit(rc)
