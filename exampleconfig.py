from sample_config import Config

class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = 21623560
    API_HASH = "8c448c687d43262833a0ab100255fb43"
    # the name to display in your alive message
    ALIVE_NAME = "K"
    # create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
    DB_URI = "رابط قاعدة البيانات"
    # After cloning the repo and installing requirements do python3 telesetup.py an fill that value with this
    STRING_SESSION = "كود التيرمكس"
    # create a new bot in @botfather and fill the following vales with bottoken and username respectively
    TG_BOT_TOKEN = "توكن البوت"
    # command handler
    COMMAND_HAND_LER = "."
    # sudo enter the id of sudo users userid's in that array
    SUDO_USERS = []
    # command hanler for sudo
    SUDO_COMMAND_HAND_LER = "."
