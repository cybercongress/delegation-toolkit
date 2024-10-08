from cyber_sdk.client.lcd import LCDClient

LCD_API = 'https://lcd.bostrom.cybernode.ai'
LCD_CLIENT = LCDClient(LCD_API)
PASSPORT_CONTRACT = 'bostrom1xut80d09q0tgtch8p0z4k5f88d3uvt8cvtzm5h3tu3tsy4jk9xlsfzhxel'

VALIDATOR_SET = 92
REDELEGATION_NUMBER = 32

JAILED_WINDOW = 200_000
NUMBER_OF_JAILS_FOR_KICKOFF = 2

MSGS_IN_TX = 8
GAS_LIMIT = 4_000_000
INITIAL_SEQUENCE = None

ALLOCATION = 137_420_000_000_000
# stake coins to heroes when allocation increased
NEW_STAKE_HERO_DICT = {}

COST_OPTIMIZATION = 0.20
DECENTRALIZATION = 0.20
CONFIDENCE = 0.20
RELIABILITY = 0.15
SUPERINTELLIGENCE = 0.15
PUBLIC_ACTIVITY = 0.10

DELEGATOR_ADDRESS = 'bostrom1xszmhkfjs3s00z2nvtn7evqxw3dtus6yr8e4pw'
MEMO = 'cyber~congress delegation strategy program https://github.com/cybercongress/delegation-toolkit'

BLACK_LIST = [
        'bostromvaloper1hmkqhy8ygl6tnl5g8tc503rwrmmrkjcqf92r73',  # sta
        'bostromvaloper152m9xcx0ht7yxr5834ju7qjcyvetw8am44jz3d',  # redelegation request 0base
        'bostromvaloper1nvr4qa7szsd3e7xfysn946gcqv5wyemlquue3d',  # redelegate ForTheFuture
        'bostromvaloper10g2lz3kf6p4jaumktxeezese3p8hkrj75wssa3'   # redelegate to weiss
]
