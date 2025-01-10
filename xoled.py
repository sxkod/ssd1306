import time

#from machine import I2C, Pin
#=I2C(scl=Pin(5),sda=Pin(4),freq=100000)
global bus

iChannel=1
iAddr= 0x3c
max_lines=0
max_columns=0
global_x=0
global_y=0


#defines
SSD1306_COMM_CONTROL_BYTE  = 0x00
SSD1306_DATA_CONTROL_BYTE  = 0x40

SSD1306_COMM_DISPLAY_OFF   = 0xae
SSD1306_COMM_DISPLAY_ON    = 0xaf
SSD1306_COMM_HORIZ_NORM    = 0xa0
SSD1306_COMM_HORIZ_FLIP    = 0xa1
SSD1306_COMM_RESUME_RAM    = 0xa4
SSD1306_COMM_IGNORE_RAM    = 0xa5
SSD1306_COMM_DISP_NORM     = 0xa6
SSD1306_COMM_DISP_INVERSE  = 0xa7
SSD1306_COMM_MULTIPLEX     = 0xa8
SSD1306_COMM_VERT_OFFSET   = 0xd3
SSD1306_COMM_CLK_SET       = 0xd5
SSD1306_COMM_PRECHARGE     = 0xd9
SSD1306_COMM_COM_PIN       = 0xda
SSD1306_COMM_DESELECT_LV   = 0xdb
SSD1306_COMM_CONTRAST      = 0x81
SSD1306_COMM_DISABLE_SCROLL= 0x2e
SSD1306_COMM_ENABLE_SCROLL = 0x2f
SSD1306_COMM_PAGE_NUMBER   = 0xb0
SSD1306_COMM_LOW_COLUMN    = 0x00
SSD1306_COMM_HIGH_COLUMN   = 0x10

SSD1306_COMM_START_LINE    = 0x40

SSD1306_COMM_CHARGE_PUMP   = 0x8d

SSD1306_COMM_SCAN_NORM     = 0xc0
SSD1306_COMM_SCAN_REVS     = 0xc8

SSD1306_COMM_MEMORY_MODE   = 0x20
SSD1306_COMM_SET_COL_ADDR  = 0x21
SSD1306_COMM_SET_PAGE_ADDR = 0x22

SSD1306_HORI_MODE          = 0x00
SSD1306_VERT_MODE          = 0x01
SSD1306_PAGE_MODE          = 0x02

SSD1306_FONT_SMALL         = 0x00
SSD1306_FONT_NORMAL        = 0x01

SSD1306_128_64_LINES       = 64
SSD1306_128_32_LINES       = 32
SSD1306_64_48_LINES        = 48

SSD1306_128_64_COLUMNS     = 128
SSD1306_128_32_COLUMNS     = 128
SSD1306_64_48_COLUMNS      = 64


#fonts
f12={'L': [4095, 4095, 3072, 3072, 3072, 3072, 3072, 3072, 3072, 3072, 3072, 3072], 'O': [4095, 4095, 3075, 3075, 3075, 3075, 3075, 3075, 3075, 3075, 4095, 4095], 'M': [4095, 4095, 3, 3, 3, 1023, 1023, 1023, 3, 3, 4095, 4095], 'P': [4095, 4095, 51, 51, 51, 51, 51, 51, 51, 51, 63, 63]}
ftst5={'O': [0, 32766, 32766, 24582, 24582, 24582, 24582, 24582, 24582, 24582, 24582, 24582, 24582, 32766, 32766, 0], 'M': [0, 16382, 16382, 6, 6, 6, 6, 16382, 16382, 6, 6, 6, 6, 16382, 16382, 0], 'L': [0, 32766, 32766, 24576, 24576, 24576, 24576, 24576, 24576, 24576, 24576, 24576, 24576, 24576, 0, 0], 'A': [0, 32766, 32766, 774, 774, 774, 774, 966, 966, 774, 774, 774, 774, 32766, 32766, 0], 'P': [0, 32766, 32766, 198, 198, 198, 198, 198, 198, 254, 254, 254, 0, 0, 0, 0]}
f88={'L': [255, 255, 192, 192, 192, 192, 192, 192], 'O': [255, 255, 195, 195, 195, 195, 255, 255], 'M': [255, 255, 3, 63, 63, 3, 255, 255], 'P': [255, 255, 27, 27, 27, 27, 31, 31]}
#choose one to use
curfont=f88

def help():
    print("""set_XY(2,2)\nwrite_string_tall(0,"LMO")""")

def onoff(onoff):
	if onoff == 0:
		cmd = SSD1306_COMM_DISPLAY_OFF;
	else:
		cmd = SSD1306_COMM_DISPLAY_ON
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE,bytearray(cmd))

def horizontal_flip(flip):
	if flip==0:
		cmd=SSD1306_COMM_HORIZ_NORM
	else:
		cmd=SSD1306_COMM_HORIZ_FLIP
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE,bytearray(cmd))
	
def display_flip(flip):
	if flip==0:
		cmd=SSD1306_COMM_DISP_NORM
	else:
		cmd=SSD1306_COMM_DISP_INVERSE
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE,bytearray(cmd))

def multiplex(row):
	databuf=[]
	data_buf.append(SSD1306_COMM_MULTIPLEX)
	data_buf.append(row - 1)
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))

def vert_shift( offset):
	databuf=[]
	data_buf.append(SSD1306_COMM_VERT_OFFSET)
	data_buf.append(offset)
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))

    
def set_clock(clk):
	databuf=[]
	data_buf.append(SSD1306_COMM_CLK_SET)
	data_buf.append(clk)
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))

def set_precharge(precharge):
	data_buf=[]
	data_buf.append(SSD1306_COMM_PRECHARGE)
	data_buf.append(precharge)
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))

def set_deselect(voltage):
	data_buf=[]
	data_buf.append(SSD1306_COMM_DESELECT_LV)
	data_buf.append(voltage)
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))

def set_com_pin(value):
	data_buf=[]
	data_buf.append(SSD1306_COMM_COM_PIN)
	data_buf.append(value)
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))

def set_mem_mode(mode):
	data_buf=[]
	data_buf.append(SSD1306_COMM_MEMORY_MODE)
	data_buf.append(mode)
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))

def set_col(start, end):
	data_buf = []
	data_buf.append(SSD1306_COMM_SET_COL_ADDR)
	data_buf.append(start)
	data_buf.append(end) 
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))


def set_page(start, end):
	data_buf=[]
	data_buf.append(SSD1306_COMM_SET_PAGE_ADDR)
	data_buf.append(start)
	data_buf.append(end)
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))


def set_constrast(value):
	data_buf=[]
	data_buf.append(SSD1306_COMM_CONTRAST)
	data_buf.append(value)
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))
    

def scroll_onoff(onoff):
	data_buf=[]
	if onoff == 0:
		data_buf.append(SSD1306_COMM_DISABLE_SCROLL)
	else:
		data_buf.append(SSD1306_COMM_ENABLE_SCROLL)
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))


def set_X(x):
	global global_x,global_y
	global max_lines,max_columns
	if x >= max_columns:return
	global_x = x    
	data_buf=[]
	data_buf.append(SSD1306_COMM_LOW_COLUMN | (x & 0x0f))
	data_buf.append(SSD1306_COMM_HIGH_COLUMN | ((x >> 4) & 0x0f))
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))
    
def set_Y(y):
	global global_x,global_y
	global max_lines,max_columns
	if y >= (max_lines / 8):return 1
	global_y = y    
	data_buf=[]
	data_buf.append(SSD1306_COMM_PAGE_NUMBER | (y & 0x0f))
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))

def set_XY(x, y):
	global global_x,global_y
	global max_lines,max_columns
	if x >= max_columns or y >= (max_lines / 8): return
	global_x = x
	global_y = y

	data_buf=[]
	data_buf.append(SSD1306_COMM_PAGE_NUMBER | (y & 0x0f))
	data_buf.append(SSD1306_COMM_LOW_COLUMN | (x & 0x0f))
	data_buf.append(SSD1306_COMM_HIGH_COLUMN | ((x >> 4) & 0x0f))
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))


def set_rotate(degree):
	data_buf=[]
	if degree == 0:
		data_buf.append(SSD1306_COMM_HORIZ_FLIP)
		data_buf.append(SSD1306_COMM_SCAN_REVS)
		bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))
	elif degree == 180:
		data_buf.append(SSD1306_COMM_HORIZ_NORM)
		data_buf.append(SSD1306_COMM_SCAN_NORM)
		bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))

def default_config(oled_lines, oled_columns):
	global global_x,global_y
	global max_lines,max_columns
	if oled_lines != SSD1306_128_64_LINES and oled_lines != SSD1306_128_32_LINES and SSD1306_64_48_LINES:
		oled_lines = SSD1306_128_64_LINES

	if oled_columns != SSD1306_128_64_COLUMNS and oled_lines != SSD1306_128_32_COLUMNS and SSD1306_64_48_COLUMNS:
		oled_columns = SSD1306_128_64_COLUMNS

	max_lines = oled_lines
	max_columns = oled_columns
	global_x = 0
	global_y = 0
    
	i = 0
	#data_buf[i++] = SSD1306_COMM_CONTROL_BYTE;  //command control byte
	data_buf=[]
	data_buf.append(SSD1306_COMM_DISPLAY_OFF)   #display off
	data_buf.append(SSD1306_COMM_DISP_NORM)     #Set Normal Display (default)
	data_buf.append(SSD1306_COMM_CLK_SET)       #SETDISPLAYCLOCKDIV
	data_buf.append(0x80)                       # the suggested ratio 0x80
	data_buf.append(SSD1306_COMM_MULTIPLEX)     #SSD1306_SETMULTIPLEX
	data_buf.append(oled_lines - 1)             # height is 32 or 64 (always -1)
	data_buf.append(SSD1306_COMM_VERT_OFFSET)   #SETDISPLAYOFFSET
	data_buf.append(0)                          #no offset
	data_buf.append(SSD1306_COMM_START_LINE)    #SETSTARTLINE
	data_buf.append(SSD1306_COMM_CHARGE_PUMP)   #CHARGEPUMP
	data_buf.append(0x14)                       #turn on charge pump
	data_buf.append(SSD1306_COMM_MEMORY_MODE)   #MEMORYMODE
	data_buf.append(SSD1306_PAGE_MODE)          # page mode
	data_buf.append(SSD1306_COMM_HORIZ_NORM)    #SEGREMAP  Mirror screen horizontally (A0)
	data_buf.append(SSD1306_COMM_SCAN_NORM)     #COMSCANDEC Rotate screen vertically (C0)
	data_buf.append(SSD1306_COMM_COM_PIN)       #HARDWARE PIN 
	if oled_lines == 32:data_buf.append(0x02)                       # for 32 lines
	else:data_buf.append(0x12)                       # for 64 lines or 48 lines

	data_buf.append(SSD1306_COMM_CONTRAST)      #SETCONTRAST
	data_buf.append(0x7f)                       # default contract value
	data_buf.append(SSD1306_COMM_PRECHARGE)     #SETPRECHARGE
	data_buf.append(0xf1)                       # default precharge value
	data_buf.append(SSD1306_COMM_DESELECT_LV)   #SETVCOMDETECT                
	data_buf.append(0x40)                       # default deselect value
	data_buf.append(SSD1306_COMM_RESUME_RAM)    #DISPLAYALLON_RESUME
	data_buf.append(SSD1306_COMM_DISP_NORM)     #NORMALDISPLAY
	data_buf.append(SSD1306_COMM_DISPLAY_ON)    #DISPLAY ON             
	data_buf.append(SSD1306_COMM_DISABLE_SCROLL)#Stop scroll
	bus.writeto_mem(iAddr,SSD1306_COMM_CONTROL_BYTE, bytearray(data_buf))



def write_line(lstx,top=True):
	data_buf=[]
	for n in lstx:
		for m in curfont[n]:
			if top:
				data_buf.append(m & 0xff)
			else:
				data_buf.append(m >> 8)
		
	write_dbuf(data_buf)

def write_dbuf(data_buf):
	i=0
	while i<len(data_buf):
		bus.writeto_mem(iAddr,SSD1306_DATA_CONTROL_BYTE, bytearray(data_buf[i:i+32]))
		data_buf[i:i+32]
		i+=32


def write_string_tall(lstx):
	global global_x,global_y
	global max_lines,max_columns

	for n in lstx.split("\n"):
		set_XY(global_x, global_y)
		write_line(n.strip())
		if global_y+1 < max_lines/8:
			set_XY(global_x,global_y+1)
			write_line(n.strip(),top=False)
		global_x = 0
		global_y+=2
		if global_y >= max_lines / 8:
			global_y = 0


def write_string(lstx):
	global global_x,global_y
	global max_lines,max_columns

	for n in lstx.split("\n"):
		set_XY(global_x, global_y)
		write_line(n.strip())
		global_x = 0
		global_y+=1
		if global_y >= max_lines / 8:
			global_y = 0


def clear_line(row):
	global max_lines,max_columns
	if row >= (max_lines / 8):return 

	set_XY(0, row)
	data_buf=[]

	for n in range(max_columns):
		data_buf.append(0x00)
	write_dbuf(data_buf)

def clear_screen():
	global max_lines
	for n in range(int(max_lines/8)):
		clear_line(n)


def init(xbus):
    global bus
    bus=xbus
    default_config(64, 128)
    clear_screen()
    set_rotate(0)
    onoff(1)
    set_XY(0,0)





