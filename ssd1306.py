import smbus,time

iChannel=1
iAddr= 0x3c
bus = smbus.SMBus(iChannel)
max_lines=0
max_columns=0
global_x=0
global_y=0
init_oled_type_file = "/tmp/.ssd1306_oled_type"

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
font5x7={' ': [0, 0, 0, 0, 0], '!': [0, 0, 95, 0, 0], '"': [0, 3, 0, 3, 0], '': [20, 62, 20, 62, 20], '$': [36, 42, 127, 42, 18], '%': [67, 51, 8, 102, 97], '&': [54, 73, 85, 34, 80], "'": [0, 5, 3, 0, 0], '(': [0, 28, 34, 65, 0], ')': [0, 65, 34, 28, 0], '*': [20, 8, 62, 8, 20], '+': [8, 8, 62, 8, 8], ',': [0, 80, 48, 0, 0], '-': [8, 8, 8, 8, 8], '.': [0, 96, 96, 0, 0], '/': [32, 16, 8, 4, 2], '0': [62, 81, 73, 69, 62], '1': [0, 4, 2, 127, 0], '2': [66, 97, 81, 73, 70], '3': [34, 65, 73, 73, 54], '4': [24, 20, 18, 127, 16], '5': [39, 69, 69, 69, 57], '6': [62, 73, 73, 73, 50], '7': [1, 1, 113, 9, 7], '8': [54, 73, 73, 73, 54], '9': [38, 73, 73, 73, 62], ':': [0, 54, 54, 0, 0], ';': [0, 86, 54, 0, 0], '<': [8, 20, 34, 65, 0], '=': [20, 20, 20, 20, 20], '>': [0, 65, 34, 20, 8], '?': [2, 1, 81, 9, 6], '@': [62, 65, 89, 85, 94], 'A': [126, 9, 9, 9, 126], 'B': [127, 73, 73, 73, 54], 'C': [62, 65, 65, 65, 34], 'D': [127, 65, 65, 65, 62], 'E': [127, 73, 73, 73, 65], 'F': [127, 9, 9, 9, 1], 'G': [62, 65, 65, 73, 58], 'H': [127, 8, 8, 8, 127], 'I': [0, 65, 127, 65, 0], 'J': [48, 64, 64, 64, 63], 'K': [127, 8, 20, 34, 65], 'L': [127, 64, 64, 64, 64], 'M': [127, 2, 12, 2, 127], 'N': [127, 2, 4, 8, 127], 'O': [62, 65, 65, 65, 62], 'P': [127, 9, 9, 9, 6], 'Q': [30, 33, 33, 33, 94], 'R': [127, 9, 9, 9, 118], 'S': [38, 73, 73, 73, 50], 'T': [1, 1, 127, 1, 1], 'U': [63, 64, 64, 64, 63], 'V': [31, 32, 64, 32, 31], 'W': [127, 32, 16, 32, 127], 'X': [65, 34, 28, 34, 65], 'Y': [7, 8, 112, 8, 7], 'Z': [97, 81, 73, 69, 67], '[': [0, 127, 65, 0, 0], '\\': [2, 4, 8, 16, 32], ']': [0, 0, 65, 127, 0], '^': [4, 2, 1, 2, 4], '_': [64, 64, 64, 64, 64], '`': [0, 1, 2, 4, 0], 'a': [32, 84, 84, 84, 120], 'b': [127, 68, 68, 68, 56], 'c': [56, 68, 68, 68, 68], 'd': [56, 68, 68, 68, 127], 'e': [56, 84, 84, 84, 24], 'f': [4, 4, 126, 5, 5], 'g': [8, 84, 84, 84, 60], 'h': [127, 8, 4, 4, 120], 'i': [0, 68, 125, 64, 0], 'j': [32, 64, 68, 61, 0], 'k': [127, 16, 40, 68, 0], 'l': [0, 65, 127, 64, 0], 'm': [124, 4, 120, 4, 120], 'n': [124, 8, 4, 4, 120], 'o': [56, 68, 68, 68, 56], 'p': [124, 20, 20, 20, 8], 'q': [8, 20, 20, 20, 124], 'r': [0, 124, 8, 4, 4], 's': [72, 84, 84, 84, 32], 't': [4, 4, 63, 68, 68], 'u': [60, 64, 64, 32, 124], 'v': [28, 32, 64, 32, 28], 'w': [60, 64, 48, 64, 60], 'x': [68, 40, 16, 40, 68], 'y': [12, 80, 80, 80, 60], 'z': [68, 100, 84, 76, 68], '{': [0, 8, 54, 65, 65], '|': [0, 0, 127, 0, 0], '}': [65, 65, 54, 8, 0], '~': [2, 1, 2, 4, 2]}
font16x16={'': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '!': [0, 0, 0, 0, 0, 0, 0, 0, 13311, 13311, 0, 0, 0, 0, 0, 0], '"': [0, 0, 0, 0, 0, 0, 15, 15, 0, 0, 15, 15, 0, 0, 0, 0], '': [0, 0, 3120, 3120, 16380, 16380, 3120, 3120, 3120, 3120, 16380, 16380, 3120, 3120, 0, 0], '$': [0, 0, 3324, 3324, 3276, 3276, 16383, 16383, 3276, 3276, 4044, 4044, 0, 0, 0, 0], '%': [0, 0, 12348, 12348, 3132, 3132, 768, 768, 192, 192, 15408, 15408, 15372, 15372, 0, 0], '&': [0, 0, 3072, 3072, 13104, 13104, 12492, 12492, 13104, 13104, 3072, 3072, 13056, 13056, 0, 0], "'": [0, 0, 0, 0, 0, 0, 48, 48, 12, 12, 0, 0, 0, 0, 0, 0], '(': [0, 0, 0, 0, 0, 0, 4080, 4080, 12300, 12300, 0, 0, 0, 0, 0, 0], ')': [0, 0, 0, 0, 0, 0, 12300, 12300, 4080, 4080, 0, 0, 0, 0, 0, 0], '*': [0, 0, 768, 768, 13104, 13104, 4032, 4032, 13104, 13104, 768, 768, 0, 0, 0, 0], '+': [0, 0, 768, 768, 768, 768, 16368, 16368, 768, 768, 768, 768, 0, 0, 0, 0], ',': [0, 0, 0, 0, 0, 0, 49152, 49152, 15360, 15360, 0, 0, 0, 0, 0, 0], '-': [0, 0, 768, 768, 768, 768, 768, 768, 768, 768, 768, 768, 0, 0, 0, 0], '.': [0, 0, 0, 0, 0, 0, 15360, 15360, 15360, 15360, 0, 0, 0, 0, 0, 0], '/': [0, 0, 12288, 12288, 3072, 3072, 768, 768, 192, 192, 48, 48, 0, 0, 0, 0], '0': [4080, 4080, 15372, 15372, 13068, 13068, 12492, 12492, 12348, 12348, 4080, 4080, 0, 0, 0, 0], '1': [12336, 12336, 12300, 12300, 16380, 16380, 12288, 12288, 12288, 12288, 0, 0, 0, 0, 0, 0], '2': [15408, 15408, 13068, 13068, 13068, 13068, 13068, 13068, 13068, 13068, 12528, 12528, 0, 0, 0, 0], '3': [3120, 3120, 12300, 12300, 12300, 12300, 12492, 12492, 12492, 12492, 3888, 3888, 0, 0, 0, 0], '4': [3840, 3840, 3264, 3264, 3120, 3120, 16380, 16380, 3072, 3072, 3072, 3072, 0, 0, 0, 0], '5': [3324, 3324, 12492, 12492, 12492, 12492, 12492, 12492, 12492, 12492, 3852, 3852, 0, 0, 0, 0], '6': [4080, 4080, 12492, 12492, 12492, 12492, 12492, 12492, 12492, 12492, 3840, 3840, 0, 0, 0, 0], '7': [12, 12, 12, 12, 15372, 15372, 780, 780, 204, 204, 60, 60, 0, 0, 0, 0], '8': [3888, 3888, 12492, 12492, 12492, 12492, 12492, 12492, 12492, 12492, 3888, 3888, 0, 0, 0, 0], '9': [240, 240, 13068, 13068, 13068, 13068, 13068, 13068, 13068, 13068, 4080, 4080, 0, 0, 0, 0], ':': [0, 0, 0, 0, 0, 0, 12480, 12480, 0, 0, 0, 0, 0, 0, 0, 0], ';': [0, 0, 0, 0, 49152, 49152, 15408, 15408, 0, 0, 0, 0, 0, 0, 0, 0], '<': [0, 0, 0, 0, 768, 768, 3264, 3264, 12336, 12336, 0, 0, 0, 0, 0, 0], '=': [0, 0, 3264, 3264, 3264, 3264, 3264, 3264, 3264, 3264, 3264, 3264, 0, 0, 0, 0], '>': [0, 0, 0, 0, 12336, 12336, 3264, 3264, 768, 768, 0, 0, 0, 0, 0, 0], '?': [0, 0, 48, 48, 12, 12, 12, 12, 13068, 13068, 204, 204, 48, 48, 0, 0], '@': [0, 0, 4080, 4080, 12300, 12300, 13260, 13260, 13116, 13116, 13260, 13260, 1008, 1008, 0, 0], 'A': [16368, 16368, 780, 780, 780, 780, 780, 780, 780, 780, 16368, 16368, 0, 0, 0, 0], 'B': [16380, 16380, 12492, 12492, 12492, 12492, 12492, 12492, 12492, 12492, 3888, 3888, 0, 0, 0, 0], 'C': [4080, 4080, 12300, 12300, 12300, 12300, 12300, 12300, 12300, 12300, 3120, 3120, 0, 0, 0, 0], 'D': [16380, 16380, 12300, 12300, 12300, 12300, 12300, 12300, 3120, 3120, 960, 960, 0, 0, 0, 0], 'E': [16380, 16380, 12492, 12492, 12492, 12492, 12492, 12492, 12492, 12492, 12300, 12300, 0, 0, 0, 0], 'F': [16380, 16380, 204, 204, 204, 204, 204, 204, 204, 204, 12, 12, 0, 0, 0, 0], 'G': [4080, 4080, 12300, 12300, 12300, 12300, 13068, 13068, 13068, 13068, 3888, 3888, 0, 0, 0, 0], 'H': [16380, 16380, 192, 192, 192, 192, 192, 192, 192, 192, 16380, 16380, 0, 0, 0, 0], 'I': [0, 0, 12300, 12300, 12300, 12300, 16380, 16380, 12300, 12300, 12300, 12300, 0, 0, 0, 0], 'J': [3840, 3840, 12288, 12288, 12288, 12288, 12288, 12288, 12288, 12288, 4092, 4092, 0, 0, 0, 0], 'K': [16380, 16380, 192, 192, 192, 192, 816, 816, 3084, 3084, 12288, 12288, 0, 0, 0, 0], 'L': [16380, 16380, 12288, 12288, 12288, 12288, 12288, 12288, 12288, 12288, 12288, 12288, 0, 0, 0, 0], 'M': [16380, 16380, 48, 48, 192, 192, 192, 192, 48, 48, 16380, 16380, 0, 0, 0, 0], 'N': [16380, 16380, 48, 48, 192, 192, 768, 768, 3072, 3072, 16380, 16380, 0, 0, 0, 0], 'O': [4080, 4080, 12300, 12300, 12300, 12300, 12300, 12300, 12300, 12300, 4080, 4080, 0, 0, 0, 0], 'P': [16380, 16380, 780, 780, 780, 780, 780, 780, 780, 780, 240, 240, 0, 0, 0, 0], 'Q': [4080, 4080, 12300, 12300, 13068, 13068, 15372, 15372, 12300, 12300, 4080, 4080, 0, 0, 0, 0], 'R': [16380, 16380, 780, 780, 780, 780, 780, 780, 3852, 3852, 12528, 12528, 0, 0, 0, 0], 'S': [3120, 3120, 12492, 12492, 12492, 12492, 12492, 12492, 12492, 12492, 3840, 3840, 0, 0, 0, 0], 'T': [12, 12, 12, 12, 12, 12, 16380, 16380, 12, 12, 12, 12, 12, 12, 0, 0], 'U': [4092, 4092, 12288, 12288, 12288, 12288, 12288, 12288, 12288, 12288, 4092, 4092, 0, 0, 0, 0], 'V': [1020, 1020, 3072, 3072, 12288, 12288, 12288, 12288, 3072, 3072, 1020, 1020, 0, 0, 0, 0], 'W': [4092, 4092, 12288, 12288, 3072, 3072, 3072, 3072, 12288, 12288, 4092, 4092, 0, 0, 0, 0], 'X': [12300, 12300, 3120, 3120, 960, 960, 960, 960, 3120, 3120, 12300, 12300, 0, 0, 0, 0], 'Y': [12, 12, 48, 48, 192, 192, 16128, 16128, 192, 192, 48, 48, 12, 12, 0, 0], 'Z': [12300, 12300, 15372, 15372, 13068, 13068, 12492, 12492, 12348, 12348, 12300, 12300, 0, 0, 0, 0], '[': [0, 0, 0, 0, 16380, 16380, 12300, 12300, 12300, 12300, 0, 0, 0, 0, 0, 0], '\\': [0, 0, 48, 48, 192, 192, 768, 768, 3072, 3072, 12288, 12288, 0, 0, 0, 0], ']': [0, 0, 0, 0, 12300, 12300, 12300, 12300, 16380, 16380, 0, 0, 0, 0, 0, 0], '^': [0, 0, 192, 192, 48, 48, 16380, 16380, 48, 48, 192, 192, 0, 0, 0, 0], '_': [49152, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 0, 0], '`': [4080, 4080, 12300, 12300, 50115, 50115, 52275, 52275, 52275, 52275, 49155, 49155, 12300, 12300, 4080, 4080], 'a': [0, 0, 3072, 3072, 13104, 13104, 13104, 13104, 13104, 13104, 16320, 16320, 0, 0, 0, 0], 'b': [0, 0, 16380, 16380, 12480, 12480, 12480, 12480, 12480, 12480, 3840, 3840, 0, 0, 0, 0], 'c': [0, 0, 0, 0, 4032, 4032, 12336, 12336, 12336, 12336, 12336, 12336, 0, 0, 0, 0], 'd': [0, 0, 3840, 3840, 12480, 12480, 12480, 12480, 12480, 12480, 16380, 16380, 0, 0, 0, 0], 'e': [0, 0, 4032, 4032, 13104, 13104, 13104, 13104, 13104, 13104, 12480, 12480, 0, 0, 0, 0], 'f': [0, 0, 0, 0, 0, 0, 16368, 16368, 204, 204, 12, 12, 0, 0, 0, 0], 'g': [0, 0, 960, 960, 52272, 52272, 52272, 52272, 52272, 52272, 52272, 52272, 16368, 16368, 0, 0], 'h': [0, 0, 16380, 16380, 192, 192, 192, 192, 192, 192, 16128, 16128, 0, 0, 0, 0], 'i': [0, 0, 0, 0, 0, 0, 12480, 12480, 16332, 16332, 12288, 12288, 0, 0, 0, 0], 'j': [0, 0, 0, 0, 12288, 12288, 49152, 49152, 49152, 49152, 16332, 16332, 0, 0, 0, 0], 'k': [0, 0, 16380, 16380, 960, 960, 3120, 3120, 12288, 12288, 0, 0, 0, 0, 0, 0], 'l': [0, 0, 0, 0, 0, 0, 4092, 4092, 12288, 12288, 12288, 12288, 0, 0, 0, 0], 'm': [0, 0, 16368, 16368, 48, 48, 16320, 16320, 48, 48, 16320, 16320, 0, 0, 0, 0], 'n': [0, 0, 16368, 16368, 48, 48, 48, 48, 48, 48, 16320, 16320, 0, 0, 0, 0], 'o': [0, 0, 4032, 4032, 12336, 12336, 12336, 12336, 12336, 12336, 4032, 4032, 0, 0, 0, 0], 'p': [0, 0, 65520, 65520, 3120, 3120, 3120, 3120, 3120, 3120, 960, 960, 0, 0, 0, 0], 'q': [0, 0, 960, 960, 3120, 3120, 3120, 3120, 3120, 3120, 65520, 65520, 49152, 49152, 0, 0], 'r': [0, 0, 0, 0, 16320, 16320, 48, 48, 48, 48, 48, 48, 0, 0, 0, 0], 's': [0, 0, 12480, 12480, 13104, 13104, 13104, 13104, 13104, 13104, 3072, 3072, 0, 0, 0, 0], 't': [0, 0, 0, 0, 48, 48, 4092, 4092, 12336, 12336, 12288, 12288, 0, 0, 0, 0], 'u': [0, 0, 4080, 4080, 12288, 12288, 12288, 12288, 12288, 12288, 4080, 4080, 0, 0, 0, 0], 'v': [0, 0, 240, 240, 3840, 3840, 12288, 12288, 3840, 3840, 240, 240, 0, 0, 0, 0], 'w': [0, 0, 4080, 4080, 12288, 12288, 4032, 4032, 12288, 12288, 4080, 4080, 0, 0, 0, 0], 'x': [0, 0, 12336, 12336, 3264, 3264, 768, 768, 3264, 3264, 12336, 12336, 0, 0, 0, 0], 'y': [0, 0, 1008, 1008, 52224, 52224, 52224, 52224, 52224, 52224, 16368, 16368, 0, 0, 0, 0], 'z': [0, 0, 12336, 12336, 15408, 15408, 13104, 13104, 12528, 12528, 12336, 12336, 0, 0, 0, 0], '{': [0, 0, 192, 192, 192, 192, 16188, 16188, 12300, 12300, 12300, 12300, 0, 0, 0, 0], '|': [0, 0, 0, 0, 0, 0, 16380, 16380, 0, 0, 0, 0, 0, 0, 0, 0], '}': [0, 0, 12300, 12300, 12300, 12300, 16188, 16188, 192, 192, 192, 192, 0, 0, 0, 0], '~': [0, 0, 0, 0, 48, 48, 12, 12, 48, 48, 12, 12, 0, 0, 0, 0]}
ftst={'L': [12, 30, 126, 228, 228, 126, 30, 12],'T': [0, 0, 96, 254, 255, 96, 0, 0],'X': [129, 66, 60, 60, 60, 60, 66, 129]}
ftst2={'L': [65535, 65535, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768], 'U': [65535, 65535, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 65535, 65535], 'O': [65535, 65535, 32769, 32769, 32769, 32769, 32769, 32769, 32769, 32769, 32769, 32769, 32769, 32769, 65535, 65535], 'M': [65535, 65535, 1, 1, 1, 1, 1, 255, 255, 1, 1, 1, 1, 1, 65535, 65535], 'N': [65535, 65535, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 65535, 65535], 'A': [65535, 65535, 387, 387, 387, 387, 387, 387, 387, 387, 387, 387, 387, 387, 65535, 65535], 'B': [65535, 65535, 33155, 33155, 33155, 33155, 33155, 33155, 33155, 33155, 33155, 33155, 49543, 57743, 65535, 65535]}
ftst3={'L': [4095, 2176, 2176, 2176, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048], 'U': [4095, 2176, 2176, 2176, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 4095]," ":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
ftst4={'L': [8188, 65535, 65535, 57344, 57344, 57344, 57344, 57344, 57344, 57344, 57344, 57344, 57344, 57344, 49152, 0], 'U': [65535, 65535, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 49152, 65535, 65535], 'O': [65535, 65535, 49153, 49153, 49153, 32769, 49153, 49153, 49153, 49153, 32769, 49153, 49153, 49153, 65535, 65535], 'M': [65535, 65535, 3, 3, 3, 3, 3, 255, 255, 3, 3, 3, 3, 3, 65535, 65535], 'N': [65535, 65535, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 65535, 65535], 'A': [65535, 65535, 387, 387, 387, 387, 387, 387, 387, 387, 387, 387, 387, 387, 65535, 65535], 'B': [65535, 65535, 33155, 33155, 33155, 33155, 33155, 33155, 33155, 33155, 33155, 33155, 49543, 57743, 65535, 65535]}
ftst5={'O': [0, 32766, 32766, 24582, 24582, 24582, 24582, 24582, 24582, 24582, 24582, 24582, 24582, 32766, 32766, 0], 'M': [0, 16382, 16382, 6, 6, 6, 6, 16382, 16382, 6, 6, 6, 6, 16382, 16382, 0], 'L': [0, 32766, 32766, 24576, 24576, 24576, 24576, 24576, 24576, 24576, 24576, 24576, 24576, 24576, 0, 0], 'A': [0, 32766, 32766, 774, 774, 774, 774, 966, 966, 774, 774, 774, 774, 32766, 32766, 0], 'P': [0, 32766, 32766, 198, 198, 198, 198, 198, 198, 254, 254, 254, 0, 0, 0, 0]}
#choose one to use , may be it should be an option
curfont=ftst5
curmsg="MOLL\nPOLL\nMOM"

def ssd1306_oled_onoff(onoff):
	if onoff == 0:
		cmd = SSD1306_COMM_DISPLAY_OFF;
	else:
		cmd = SSD1306_COMM_DISPLAY_ON
	bus.write_byte_data(iAddr,SSD1306_COMM_CONTROL_BYTE,cmd)

def ssd1306_oled_horizontal_flip(flip):
	if flip==0:
		cmd=SSD1306_COMM_HORIZ_NORM
	else:
		cmd=SSD1306_COMM_HORIZ_FLIP
	bus.write_byte_data(iAddr,SSD1306_COMM_CONTROL_BYTE,cmd)
	
def ssd1306_oled_display_flip(flip):
	if flip==0:
		cmd=SSD1306_COMM_DISP_NORM
	else:
		cmd=SSD1306_COMM_DISP_INVERSE
	bus.write_byte_data(iAddr,SSD1306_COMM_CONTROL_BYTE,cmd)

def ssd1306_oled_multiplex(row):
	databuf=[]
	data_buf.append(SSD1306_COMM_MULTIPLEX)
	data_buf.append(row - 1)
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)

def ssd1306_oled_vert_shift( offset):
	databuf=[]
	data_buf.append(SSD1306_COMM_VERT_OFFSET)
	data_buf.append(offset)
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)

    
def ssd1306_oled_set_clock(clk):
	databuf=[]
	data_buf.append(SSD1306_COMM_CLK_SET)
	data_buf.append(clk)
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)

def ssd1306_oled_set_precharge(precharge):
	data_buf=[]
	data_buf.append(SSD1306_COMM_PRECHARGE)
	data_buf.append(precharge)
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)

def ssd1306_oled_set_deselect(voltage):
	data_buf=[]
	data_buf.append(SSD1306_COMM_DESELECT_LV)
	data_buf.append(voltage)
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)

def ssd1306_oled_set_com_pin(value):
	data_buf=[]
	data_buf.append(SSD1306_COMM_COM_PIN)
	data_buf.append(value)
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)

def ssd1306_oled_set_mem_mode(mode):
	data_buf=[]
	data_buf.append(SSD1306_COMM_MEMORY_MODE)
	data_buf.append(mode)
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)

def ssd1306_oled_set_col(start, end):
	data_buf = []
	data_buf.append(SSD1306_COMM_SET_COL_ADDR)
	data_buf.append(start)
	data_buf.append(end) 
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)


def ssd1306_oled_set_page(start, end):
	data_buf=[]
	data_buf.append(SSD1306_COMM_SET_PAGE_ADDR)
	data_buf.append(start)
	data_buf.append(end)
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)


def ssd1306_oled_set_constrast(value):
	data_buf=[]
	data_buf.append(SSD1306_COMM_CONTRAST)
	data_buf.append(value)
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)
    

def ssd1306_oled_scroll_onoff(onoff):
	data_buf=[]
	if onoff == 0:
		data_buf.append(SSD1306_COMM_DISABLE_SCROLL)
	else:
		data_buf.append(SSD1306_COMM_ENABLE_SCROLL)
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)


def ssd1306_oled_set_X(x):
	global global_x,global_y
	global max_lines,max_columns
	if x >= max_columns:return
	global_x = x    
	data_buf=[]
	data_buf.append(SSD1306_COMM_LOW_COLUMN | (x & 0x0f))
	data_buf.append(SSD1306_COMM_HIGH_COLUMN | ((x >> 4) & 0x0f))
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)
    
def ssd1306_oled_set_Y(y):
	global global_x,global_y
	global max_lines,max_columns
	if y >= (max_lines / 8):return 1
	global_y = y    
	data_buf=[]
	data_buf.append(SSD1306_COMM_PAGE_NUMBER | (y & 0x0f))
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)

def ssd1306_oled_set_XY(x, y):
	global global_x,global_y
	global max_lines,max_columns
	if x >= max_columns or y >= (max_lines / 8): return
	global_x = x
	global_y = y

	data_buf=[]
	data_buf.append(SSD1306_COMM_PAGE_NUMBER | (y & 0x0f))
	data_buf.append(SSD1306_COMM_LOW_COLUMN | (x & 0x0f))
	data_buf.append(SSD1306_COMM_HIGH_COLUMN | ((x >> 4) & 0x0f))
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)


def ssd1306_oled_set_rotate(degree):
	data_buf=[]
	if degree == 0:
		data_buf.append(SSD1306_COMM_HORIZ_FLIP)
		data_buf.append(SSD1306_COMM_SCAN_REVS)
		bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)
	elif degree == 180:
		data_buf.append(SSD1306_COMM_HORIZ_NORM)
		data_buf.append(SSD1306_COMM_SCAN_NORM)
		bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)

def ssd1306_oled_default_config(oled_lines, oled_columns):
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
    
	ssd1306_oled_save_resolution(max_columns, max_lines)

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
	bus.write_i2c_block_data(iAddr,SSD1306_COMM_CONTROL_BYTE, data_buf)



def ssd1306_oled_write_line(lsize, lstx,top=True):
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
		bus.write_i2c_block_data(iAddr,SSD1306_DATA_CONTROL_BYTE, data_buf[i:i+32])
		data_buf[i:i+32]
		i+=32


def ssd1306_oled_write_string_tall(lsize, lstx):
	global global_x,global_y
	global max_lines,max_columns

	for n in lstx.split("\n"):
		ssd1306_oled_set_XY(global_x, global_y)
		ssd1306_oled_write_line(lsize, n.strip())
		if global_y+1 < max_lines/8:
			ssd1306_oled_set_XY(global_x,global_y+1)
			ssd1306_oled_write_line(lsize,n.strip(),top=False)
		global_x = 0
		global_y+=2
		if global_y >= max_lines / 8:
			global_y = 0


def ssd1306_oled_write_string(lsize, lstx):
	global global_x,global_y
	global max_lines,max_columns

	for n in lstx.split("\n"):
		ssd1306_oled_set_XY(global_x, global_y)
		ssd1306_oled_write_line(lsize, n.strip())
		global_x = 0
		global_y+=1
		if global_y >= max_lines / 8:
			global_y = 0


def ssd1306_oled_clear_line(row):
	global max_lines,max_columns
	if row >= (max_lines / 8):return 

	ssd1306_oled_set_XY(0, row)
	data_buf=[]

	for n in range(max_columns):
		data_buf.append(0x00)
	write_dbuf(data_buf)

def ssd1306_oled_clear_screen():
	global max_lines
	for n in range(int(max_lines/8)):
		ssd1306_oled_clear_line(n)


def ssd1306_oled_save_resolution(column, row):
	fp = open(init_oled_type_file, "w")
	if fp:
		fp.write(str(column)+","+str(row))
		fp.close()


def ssd1306_oled_load_resolution():
	global max_lines,max_columns
	fp = open(init_oled_type_file, "r")
	if fp:
		t=fp.read().split(',')
		max_columns=int(t[0])
		max_lines=int(t[1])
	fclose(fp);

ssd1306_oled_default_config(64, 128)
ssd1306_oled_clear_screen()
ssd1306_oled_set_rotate(0)
ssd1306_oled_onoff(1)
ssd1306_oled_set_XY(2,2)
ssd1306_oled_write_string_tall(0,curmsg)
