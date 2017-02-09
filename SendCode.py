import sys
import re
import json
import requests

def hello(command):
    print("In SendCode")
    ACL_URL = '/sony/accessControl'
    CODE_URL = '/sony/system'
    IRCC_URL = '/sony/IRCC'
    PSK = '1234'
    TV_URL = 'http://192.168.2.137'
    FINAL_URL = TV_URL + ACL_URL
    #CommandMessage = 'volume down'
    CommandMessage=command
    print('Passed Command:' +command)
    IRCC_CODE_FILE = ''
    IRCC_CODE = ''
    IRCC_COMMAND = ''
    JSON_FileName = '/var/www/ircc/ircc/SonyXBR850DIRCCCodes.json'
    SOAPMessage_FileName = ''
    SOAPMessageHeader = {'content-type': 'text/xml', 'SOAPAction': '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"'}
    ACL_POST_DATA = '{"id":13,"method":"actRegister","version":"1.0","params":[{"clientid":"iRule:1","nickname":"iRule"},[{"clientid":"iRule:1","value":"yes","nickname":"iRule","function":"WOL"}]]}'
    IRCC_DATA = '{"method":"getRemoteControllerInfo","params":[],"id":10, "version":"1.0"}'
    SOAPMessageIRCCHeader = {'content-type': 'text/xml', 'X-Auth-PSK': PSK,
                             'SOAPAction': '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"'}

    # Command Dictionary. One to Many. Maps different phrases that can be used to achieve the same functionality
    # CommandMessageDict = {'PowerOff':['shutdown the tv','switch off the tv','power off the tv','power down the tv','shut down the tv'],
    #             'TvPower':['switch on the tv','power on the tv','start the tv','open the tv', 'power up the tv']}
    CommandMessageDict = {'Num1': ['One', 'Press Number One', 'Number One'],
                          'Num2': ['Two', 'Press Number Two', 'Number Two'],
                          'Num3': ['Three', 'Press Number Three', 'Number Three'],
                          'Num4': ['Four', 'Press Number Four', 'Number Four'],
                          'Num5': ['Five', 'Press Number Five', 'Number Five'],
                          'Num6': ['Six', 'Press Number Six', 'Number Six'],
                          'Num7': ['Seven', 'Press Number Seven', 'Number Seven'],
                          'Num8': ['Eight', 'Press Number Eight', 'Number Eight'],
                          'Num9': ['Nine', 'Press Number Nine', 'Number Nine'],
                          'Num0': ['Zero', 'Press Number Zero', 'Number Zero'],
                          'Num11': ['Eleven'], 'Num12': ['Twelve'], 'Enter': ['Enter', 'Press Enter', ],
                          'GGuide': ['Guide','Open Program Guide', 'ProgramGuide', 'ChannelGuide', 'ProgramList'],
                          'ChannelUp': ['ChannelUp', 'ChannelNext', 'ChannelPlusOne'],
                          'ChannelDown': ['ChannelDown', 'ChannelPrevious', 'ChannelMinusOne'],
                          'VolumeUp': ['Volume Up', 'VolumeUp', 'Volume Increase', 'Increase Volume', 'Up the Volume'],
                          'VolumeDown': ['Volume Down', 'VolumeDown', 'Volume Decrease', 'Decrease Volume', 'Down the volume',
                                         'Reduce the volume'], 'Mute': ['Mute'],
                          'TvPower': ['Power On', 'On', 'Switch On', 'Power up', 'Start'],
                          'Audio': ['Audio Settings', 'Audio Configuration'],
                          'MediaAudioTrack': ['Media Audio Track', 'Media Audio Info'],
                          'Tv': ['WatchTv', 'OpenTV', 'BrowseTV'],
                          'Input': ['Input', 'Input Previous', 'Input Minus One'],
                          'TvInput': ['TvInput', 'Tv Previous', 'Tv Minus One'],
                          'TvAntennaCable': ['TvCable', 'TvAntenna', 'Tv Minus One'], 'WakeUp': ['WakeUp'],
                          'PowerOff': ['PowerOff', 'PowerDown', 'Shutoff ', 'ShutDown', 'SwitchOff'],
                          'Sleep': ['Sleep'], 'Right': ['Right', 'Move Left'], 'Left': ['Left', 'Move Right'],
                          'SleepTimer': ['Sleep Timer', 'Set Sleep Timer', 'Timer'],
                          'Analog2': ['Analog Two', 'Input Analog 2'],
                          'TvAnalog': ['Tv Analog', 'Tv Analog Input', 'Select TV Analog'],
                          'Display': ['Display', 'Display Info', 'Info'], 'Jump': ['Jump', 'Jump Previous'],
                          'PicOff': ['Pic Off', 'Picture Off', 'Switch Off Display'],
                          'PictureOff': ['Pic Off', 'Picture Off', 'Switch Off Display'], 'Teletext': ['Teletext'],
                          'Video1': ['Select Video One', 'Input Video One', 'Video One'],
                          'Video2': ['Select Video Two', 'Input Video Two', 'Video Two'],
                          'AnalogRgb1': ['Analog Rgb One', 'Select Analog RGB One'],
                          'Home': ['Home', 'Go To Home', 'Open Home'],
                          'Exit': ['Exit'], 'PictureMode': ['Picture Mode', 'Open Picture Mode'],
                          'Confirm': ['Confirm', 'Select'], 'Up': ['Up'], 'Down': ['Down'],
                          'ClosedCaption': ['Closed Caption', 'Closed Caption Info'],
                          'Component1': ['Select Component One', 'Component One'],
                          'Component2': ['Select Component Two', 'Component Two'],
                          'Wide': ['Wide', 'Wide Screen', 'Wide Minus One'],
                          'EPG': [' EPG', ' Electronic Program Guide'],
                          'PAP': [' PAP'], 'TenKey': ['Ten Key'], 'BSCS': [' BSCS'],
                          'Ddata': ['Ddata', 'Ddata Previous', 'Ddata Minus One'], 'Stop': ['Stop'],
                          'Pause': ['Pause'], 'Play': ['Play'], 'Rewind': ['Rewind'], 'Forward': ['Forward'],
                          'DOT': [' DOT'], 'Rec': ['Rec', 'Record'], 'Return': ['Return'],
                          'Blue': ['Blue', 'Blue Button'],
                          'Red': ['Red', 'Red Button'], 'Green': ['Green', 'Green Button'],
                          'Yellow': ['Yellow', 'Yellow Button'], 'SubTitle': ['Sub Title', 'Subtitle', 'Sub Titles'],
                          'CS': [' CS'], 'BS': [' BS'],
                          'Digital': ['Digital', 'Digital Input', 'Select Digital', 'Select Digital Input'],
                          'Options': ['Options', 'Open Options', 'Show Options'],
                          'Media': ['Media', 'Media Info', 'Show Media'],
                          'Prev': ['Previous', 'Go To Previous', 'Prev'],
                          'Next': ['Next', 'Go To Next'],
                          'DpadCenter': ['Select', 'Center', 'Dpad Center'], 'CursorUp': ['CursorUp'],
                          'CursorDown': ['CursorDown'], 'CursorLeft': ['CursorLeft'],
                          'CursorRight': ['CursorRight'], 'ShopRemoteControlForcedDynamic': [],
                          'FlashPlus': ['Flash Plus'], 'FlashMinus': ['Flash Minus'],
                          'AudioQualityMode': ['Audio Mode', 'Audio Quality Mode'], 'DemoMode': ['Demo Mode'],
                          'Analog': ['Analog', 'Analog Input', 'Select Analog Input'],
                          'Mode3D': ['Mode Three D', 'Three D'],
                          'DigitalToggle': ['Digital Toggle', 'Digital Previous', 'Digital Next'],
                          'DemoSurround': ['Demo Surround', 'Surround'],
                          '*AD': ['AD'], 'AudioMixUp': ['Audio Up', 'Audio Mix Up'],
                          'AudioMixDown': ['Audio Down', 'Audio Mix Down'], 'PhotoFrame': ['Photo Frame'],
                          'Tv_Radio': ['Tv Radio'],
                          'SyncMenu': ['Sync Menu'], 'Hdmi1': ['Select Hdmi One', 'Hdmi One'],
                          'Hdmi2': ['Select Hdmi Two', 'Hdmi Two'], 'Hdmi3': ['Select Hdmi Three', 'Hdmi three'],
                          'Hdmi4': ['Select Hdmi Four', 'Hdmi Four'], 'TopMenu': ['Top Menu', 'Menu'],
                          'PopUpMenu': ['Pop Menu'], 'OneTouchTimeRec': ['One Rec', 'One Touch Recording'],
                          'OneTouchView': ['One View', 'One Touch View'], 'DUX': [' DUX'],
                          'FootballMode': ['Football Mode', 'Switch On Football Mode'],
                          'iManual': ['i Manual', 'Manual', 'i Minus One'],
                          'Netflix': ['Netflix', 'Launch Netflix', 'Start Netflix', 'Open Netflix'],
                          'Assists': ['Assists'],
                          'ActionMenu': ['Action Menu'], 'Help': ['Open Help', 'Help'],
                          'TvSatellite': ['Tv Satellite', 'Satellite'],
                          'WirelessSubwoofer': ['Wireless Subwoofer', 'Subwoofer']}

    # Update the SOAPBodyMessage
    SOAPMessageIRCCBODY = """<?xml version="1.0"?>
                                <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                                    <s:Body>
                                        <u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">
                                            <IRCCCode>TBDTBDTBD</IRCCCode>
                                        </u:X_SendIRCC>
                                    </s:Body>
                                </s:Envelope>"""
    # print("Before the replace: "+SOAPMessageIRCCBODY)
    # print("After the replace"+ str.replace( SOAPMessageIRCCBODY,'TBDTBDTBD',IRCC_CODE))

    # Fetch the IRCC_CODE for IRCC_Command
    for code, value in CommandMessageDict.items():
        TEMP_LIST = value
        for value2 in TEMP_LIST:
            if value2.capitalize() == CommandMessage.capitalize():
                print(code)
                IRCC_COMMAND = code
                print(IRCC_COMMAND)
                break
            else:
                print('Unable to search IRCC_CODE!!!')
                continue
    print(IRCC_COMMAND)

    # Reading data back
    with open(JSON_FileName) as f:
        text = f.read()
        jsonResponse = json.loads(text)
        print(jsonResponse['result'][1][0]["name"] + "---" + jsonResponse['result'][1][0]["value"])

    # Put the data in dictionary
    IRCC_Code_Dict = dict()
    i = 0
    for key, value in jsonResponse['result'][1]:
        IRCC_Code_Dict[jsonResponse['result'][1][i]["name"]] = jsonResponse['result'][1][i]["value"]
        i = i + 1

    # Fetch the IRCC Code For the IRCC Command
    IRCC_CODE = IRCC_Code_Dict.get(IRCC_COMMAND)
    print('Final IRCC Code: ' + IRCC_CODE)

    # Send SOAP Message
    FINAL_URL = TV_URL + IRCC_URL

    print(FINAL_URL)
    response = requests.post(FINAL_URL, headers=SOAPMessageIRCCHeader,
                             data=str.replace(SOAPMessageIRCCBODY, 'TBDTBDTBD', IRCC_CODE))
    # response = requests.post(FINAL_URL,data=SOAPMessageIRCCBODY,headers=SOAPMessageIRCCHeader)
    print(response.status_code)

    # GET ACCESS TO TV
    FINAL_ACL_URL = TV_URL + ACL_URL

    ENTER_LOGIN = ''
    ENTER_PIN = ''

    # Get available IRCC from the device
    FINAL_CODE_URL = TV_URL + CODE_URL


