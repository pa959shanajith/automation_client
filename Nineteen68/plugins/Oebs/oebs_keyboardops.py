from ctypes import *
from ctypes.wintypes import *
from time import sleep
import win32ui
import oebs_constants
from oebs_msg import *

class KeywordOperations:
    # CONSTANTS
    KEYEVENTF_EXTENDEDKEY = 1
    KEYEVENTF_KEYUP = 2

    # VIRTUAL KEYCODES

    _key_names = [" ", "left_mouse_button", "right_mouse_button", "control-break_processing", "middle_mouse_button_(three-button_mouse)", "x1_mouse_button", "x2_mouse_button", "undefined", "backspace", "tab", "reserved", "clear", "enter", "undefined", "shift", "ctrl", "alt", "pause", "capslock", "ime_kana_mode", "ime_hanguel_mode_(maintained_for_compatibility;_use_vk_hangul)", "ime_hangul_mode", "undefined", "ime_junja_mode", "ime_final_mode", "ime_hanja_mode", "ime_kanji_mode", "undefined", "esc", "ime_convert", "ime_nonconvert", "ime_accept", "ime_mode_change_request", "spacebar", "pageup", "pagedown", "end", "home", "leftarrow", "uparrow", "rightarrow", "downarrow", "select", "print", "execute", "printscreen", "insert", "del", "help", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "undefined", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "windows", "right_windows__(natural_board)", "menu", "reserved", "computer_sleep", "num0", "num1", "num2", "num3", "num4", "num5", "num6", "num7", "num8", "num9", "multiply", "add", "separator", "subtract", "decimal", "divide", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20", "f21", "f22", "f23", "f24", "unassigned", "numlock", "scrolllock", "oem_specific", "unassigned", "left_shift", "right_shift", "left_control", "right_control", "left_menu", "right_menu", "browser_back", "browser_forward", "browser_refresh", "browser_stop", "browser_search", "browser_favorites", "browser_start_and_home", "volume_mute", "volume_down", "volume_up", "next_track", "previous_track", "stop_media", "play/pause_media", "start_mail", "select_media", "start_application_1", "start_application_2", "reserved", ";", "=", ",", "-",".","/","`", "reserved", "unassigned", "[", "\\", "]", "'", "used_for_miscellaneous_characters_it_can_vary_by_board.", "reserved", "oem_specific", "either_the_angle_bracket__or_the_backslash__on_the_rt_102-_board", "oem_specific", "ime_process", "oem_specific", "used_to_pass_unicode_characters_as_if_they_were_strokes._the_vk_packet__is_the_low_word_of_a_32-bit_virtual_key_value_used_for_non-board_input_methods._for_more_information,_see_remark_in_keybdinput,_sendinput,_wm_keydown,_and_wm_keyup", "unassigned", "oem_specific", "attn", "crsel", "exsel", "erase_eof", "play", "zoom", "reserved", "pa1", "clear", "delete"]
    _vk_codes = [0x20, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0C, 0x0D, 0x0E, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x15, 0x15, 0x16, 0x17, 0x18, 0x19, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A-40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x90, 0x91, 0x92, 0x97, 0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF, 0xC0, 0xC1, 0xD8, 0xDB, 0xDC, 0xDD, 0xDE, 0xDF, 0xE0, 0xE1, 0xE2, 0xE3, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9,0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0x2E]
    _shifted_keys = '~!@#$%^&*()_+|}{":?><'
    _unshifted_keys = "`1234567890-=\\][';/.,"

    special_map = {key: val for (key,val) in zip(_shifted_keys, _unshifted_keys)}

    key_mapping = {key: code for (key, code) in zip(_key_names, _vk_codes)}

    virtualkeycodes={
    'CONTROL' : 0xA2,
    'ENTER' : 0x0D,
    'CAPSLOCK' : 0x14,
    'SHIFT' : 0xA1,
    '*' : 0x6A,
    'A_UP' : 0x26,
    'HOME' : 0x24,
    'A_DOWN' : 0x28,
    'ALT' : 0x12,
    #keycodes for number
    '0' : 0x30,
    '1' : 0x31,
    '2' : 0x32,
    '3' : 0x33,
    '4' : 0x34,
    '5' : 0x35,
    '6' : 0x36,
    '7' : 0x37,
    '8' : 0x38,
    '9' : 0x39,

    'A' : 0x41,
    'B' : 0x42,
    'C' : 0x43,
    'D' : 0x44,
    'E' : 0x45,
    'F' : 0x46,
    'G' : 0x47,
    'H' : 0x48,
    'I' : 0x49,
    'J' : 0x4A,
    'K' : 0x4B,
    'L' : 0x4C,
    'M' : 0x4D,
    'N' : 0x4E,
    'O' : 0x4F,
    'P' : 0x50,
    'Q' : 0x51,
    'R' : 0x52,
    'S' : 0x53,
    'T' : 0x54,
    'U' : 0x55,
    'V' : 0x56,
    'W' : 0x57,
    'X' : 0x58,
    'Y' : 0x59,
    'Z' : 0x5A,
    '6' : 0x5B,
    '7' : 0x5C,
    '8' : 0x5D,
    '9' : 0x5E,
    '9' : 0x45F,

    }

    def find_key(self,key):
        if key.upper() in self.virtualkeycodes:
            key=self.virtualkeycodes.get(key.upper())
        elif key.lower() in self.key_mapping:
            key=self.key_mapping.get(key.lower())
        elif key in list(self.special_map.keys()):
            key = self.special_map[key]
        return key



    def __sendkeydown(self,key):
        windll.user32.keybd_event(key,0,0,0)

    def __sendkeyup(self,key):
        windll.user32.keybd_event(key,0,self.KEYEVENTF_KEYUP,0)

    def __sendkeypress(self,key):
        windll.user32.keybd_event(key, 0,0,0)
        windll.user32.keybd_event(key,0,self.KEYEVENTF_KEYUP,0)

    def keyboard_operation_sendfunctionkeys(self,action,key):
        key=self.find_key(key)
        if key != None:
            if(action == 'keydown'):
                self.__sendkeydown(key)
                return True
            elif(action == 'keyup'):
                self.__sendkeyup(key)
                return True
            elif(action == 'keypress'):
                self.__sendkeypress(key)
                return True
            else:
                return MSG_INVALID_ACTION_INFO
        else:
            return MSG_INVALID_ACTION_INFO

    def keyboard_operation(self,action,key):
        if(action == 'keydown'):
            self.sendkeydown(key)
            return True
        elif(action == 'keyup'):
            self.sendkeyup(key)
            return True
        elif(action == 'keypress'):
            self.sendkeypress(key)
            return True
        else:
            return False

    def sendkeydown(self,key):
        windll.user32.keybd_event(self.virtualkeycodes.get(key),0,0,0)

    def sendkeyup(self,key):
        windll.user32.keybd_event(self.virtualkeycodes.get(key),0,self.KEYEVENTF_KEYUP,0)

    def sendkeypress(self,key):
        windll.user32.keybd_event(self.virtualkeycodes.get(key), 0,0,0)
        windll.user32.keybd_event(self.virtualkeycodes.get(key),0,self.KEYEVENTF_KEYUP,0)

##obj=KeywordOperations()
##obj.keyboard_operation_sendfunctionkeys('keypress','backspace')
##print obj.key_mapping
