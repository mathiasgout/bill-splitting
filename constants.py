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
GW_MEMBER_LABEL_FONT_SIZE = 14


# pop up window
PUW_WIDTH, PUW_HEIGHT = 500, 70

# pop up window sizes
PUW_ENTRY_FONT_SIZE = 15
PUW_LABEL_FONT_SIZE = 14


# unvalid character entries
INVALID_CHAR = ("\\", " ", "/", ">", "<", ":", "|", "?", "*", "[", "]", "@", "!", "#", "$", "%", "^", "&", "(", ")", 
                '"', "'", "{", "}", "~", "°", "`", "ç", "à", "-", "=", "+", ".", ";", ",", "§", "£", "€")


# color
GREEN = "#D8EEED"

