from screeninfo import get_monitors

monitor = get_monitors()[0]

# screen resolution
SCREEN_HEIGHT = monitor.height
SCREEN_WIDTH = monitor.width


# menu window width and height + menu window positioning
MW_WIDTH, MW_HEIGHT = 430, 430
MW_POS_X = int((SCREEN_WIDTH - MW_WIDTH)/2)
MW_POS_Y = int((SCREEN_HEIGHT - 1.5*MW_HEIGHT)/2)

# menu window sizes
MW_BUTTON_FONT_SIZE = 15


# group window
GW_WIDTH, GW_HEIGHT = 860, 650
GW_POS_X = int((SCREEN_WIDTH - GW_WIDTH)/2)
GW_POS_Y = int((SCREEN_HEIGHT - GW_HEIGHT)/2)

# group window sizes
GW_LEFT_FRAME_SIZE = GW_WIDTH * 0.25
GW_RIGHT_FRAME_SIZE = GW_WIDTH - GW_LEFT_FRAME_SIZE
GW_MEMBER_ROW_HEIGHT = GW_HEIGHT * 0.05
GW_CALCULATE_PART_HEIGHT = GW_HEIGHT * 0.15
GW_MEMBER_LABEL_FONT_SIZE = 16
GW_POURCENT_LABEL_FONT_SIZE = 13
GW_END_START_LABEL_FONT_SIZE = 13
GW_CALCULATE_BUTTON_FONT_SIZE = 14
GW_RIGHT_FRAME_BUTTON_FONT_SIZE = 14


# pop up window
PUW_WIDTH, PUW_HEIGHT = 500, 70
PUW_WIDTH_BIG, PUW_HEIGHT_BIG = 400, 220
PUW_WIDTH_EDIT_EXPENSES, PUW_HEIGHT_EDIT_EXPENSES = 700, 300
PUW_EDIT_EXPENSES_ROW_HEIGHT_HEADER = int(PUW_HEIGHT_EDIT_EXPENSES/8)
PUW_EDIT_EXPENSES_ROW_HEIGHT = int(PUW_HEIGHT_EDIT_EXPENSES/10)
PUW_EDIT_EXPENSES_HEADER_FONT_SIZE = 12


# pop up window sizes
PUW_ENTRY_FONT_SIZE = 15
PUW_LABEL_FONT_SIZE = 14
PUW_BIG_ENTRY_FONT_SIZE = 12

# unvalid character entries
INVALID_CHAR = ("\\", " ", "/", ">", "<", ":", "|", "?", "*", "[", "]", "@", "!", "#", "$", "%", "^", "&", "(", ")", 
                '"', "'", "{", "}", "~", "°", "`", "ç", "à", "-", "=", "+", ".", ";", ",", "§", "£", "€")

# type expense
TYPE_LIST = ["<AUTRE>", "COURSE", "VOITURE", "SOIN", "LOISIR", "RESTAURANT"]

# color
GREEN = "#D8EEED"

