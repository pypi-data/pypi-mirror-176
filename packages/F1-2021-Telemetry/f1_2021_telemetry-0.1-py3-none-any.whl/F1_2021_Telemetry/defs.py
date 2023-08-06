from enum import Enum
from F1_2021_Telemetry.translate import translate, Case

# Base class to define __str__() where a title case string should be returned
# e.g drivers' names, track names, etc
class TitleCase(Enum):
    def __str__(self) -> str:
        return translate(self.name, Case.TITLE)

# Base class to define __str__() where a sentence case string should be returned
# e.g infringement types
class SentenceCase(Enum):
    def __str__(self) -> str:
        return translate(self.name, Case.SENTENCE)   

class ZoneFlag(TitleCase):
    NOT_RECEIVED = None
    UNKNOWN = -1
    NONE = 0
    GREEN = 1
    BLUE = 2
    YELLOW = 3
    RED = 4

class SessionType(TitleCase):
    NOT_RECEIVED = None
    UNKNOWN = 0
    PRACTICE_1 = 1
    PRACTICE_2 = 2
    PRACTICE_3 = 3
    SHORT_PRACTICE = 4
    QUALIFYING_1 = 5
    QUALIFYING_2 = 6
    QUALIFYING_3 = 7
    SHORT_QUALIFYING = 8
    ONE_SHOT_QUALFYING = 9
    RACE = 10
    RACE_2 = 11
    RACE_3 = 12
    TIME_TRIAL = 13

class Weather(SentenceCase):
    NOT_RECEIVED = None
    CLEAR = 0
    LIGHT_CLOUD = 1
    OVERCAST = 2
    LIGHT_RAIN = 3 
    HEAVY_RAIN = 4
    STORM = 5

class Change(SentenceCase):
    NOT_RECEIVED = None
    UP = 0
    DOWN = 1
    NO_CHANGE = 2

TrackTemperatureChange = Change
AirTemperatureChange = Change

class Formula(TitleCase):
    NOT_RECEIVED = None
    F1_MODERN = 0
    F1_CLASSIC = 1
    F2 = 2
    F1  = 3
    F2_2020 = 7

class ActiveInactive(TitleCase):
    NOT_RECEIVED = None
    INACTIVE = 0
    ACTIVE = 1

SliProNativeSupport = ActiveInactive
    
class SafetyCarStatus(TitleCase):
    NOT_RECEIVED = None
    NO_SAFETY_CAR = 0
    FULL_SAFETY_CAR = 1
    VIRTUAL_SAFETY_CAR = 2
    FORMATION_LAP = 3

class NetworkGame(TitleCase):
    NOT_RECEIVED = None
    OFFLINE = 0
    ONLINE = 1

class ForecastAccuracy(TitleCase):
    NOT_RECEIVED = None
    PERFECT = 0
    APPROXIMATE = 1

class OnOff(TitleCase):
    NOT_RECEIVED = None
    OFF = 0
    ON = 1

SteeringAssist = OnOff
PitAssist = OnOff
PitReleaseAssist = OnOff
ERSAssist = OnOff
DRSAssist = OnOff

class BrakingAssist(TitleCase):
    NOT_RECEIVED = None
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class GearboxAssist(SentenceCase):
    NOT_RECEIVED = None
    MANUAL = 1
    MANUAL_WITH_SUGGESTED_GEAR = 2
    AUTO = 3

class DynamicRacingLine(SentenceCase):
    NOT_RECEIVED = None
    OFF = 0
    CORNERS_ONLY = 1
    FULL = 2

class DynamicRacingLineType(SentenceCase):
    NOT_RECEIVED = None
    TWO_D = 0
    THREE_D = 1

class PitStatus(TitleCase):
    NOT_RECEIVED = None
    NONE = 0
    PITTING = 1
    IN_PIT_AREA = 2

class Sector(TitleCase):
    NOT_RECEIVED = None
    SECTOR_1 = 0
    SECTOR_2 = 1
    SECTOR_3 = 2

class DriverStatus(SentenceCase):
    NOT_RECEIVED = None
    IN_GARAGE = 0
    FLYING_LAP = 1
    IN_LAP = 2
    OUT_LAP = 3
    ON_TRACK = 4

class ResultStatus(TitleCase):
    NOT_RECEIVED = None
    INVALID = 0
    INACTIVE = 1
    ACTIVE = 2
    FINISHED = 3
    DID_NOT_FINISH = 4
    DISQUALIFIED = 5
    NOT_CLASSIFIED = 6
    RETIRED = 7

class YourTelemetry(TitleCase):
    NOT_RECEIVED = None
    RESTRICTED = 0
    PUBLIC = 1

class Gear(TitleCase):
    NOT_RECEIVED = None
    REVERSE = -1
    NEUTRAL = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7
    EIGHTH = 8

Drs = OnOff

class MfdPanel(SentenceCase):
    # May vary depending on game mode, values given for race
    NOT_RECEIVED = None
    CAR_SETUP = 0
    PITS = 1
    DAMAGE = 2
    ENGINE = 3
    TEMPERATURES = 4
    MFD_CLOSED = 255

class TractionControl(TitleCase):
    NOT_RECEIVED = None
    OFF = 0
    MEDIUM = 1
    FULL = 2

AntiLockBrakes = OnOff

class FuelMix(TitleCase):
    NOT_RECEIVED = None
    LEAN = 0
    STANDARD = 1
    RICH = 2
    MAX = 3

PitLimiterStatus = OnOff

class ActualTyreCompound(TitleCase):
    NOT_RECEIVED = None
    UNKNOWN = 0
    C5 = 16
    C4 = 17
    C3 = 18
    C2 = 19
    C1 = 20
    INTER = 7
    WET = 8
    CLASSIC_DRY = 9
    CLASSIC_WET = 10
    F2_SUPERSOFT = 11
    F2_SOFT = 12
    F2_MEDIUM = 13
    F2_HARD = 14
    F2_WET = 15
    NO_TYRES = 25

class VisualTyreCompound(TitleCase):
    NOT_RECEIVED = None
    UNKNOWN = 0
    SOFT = 16
    MEDIUM = 17
    HARD = 18
    INTER = 7
    WET = 8
    CLASSIC_DRY = 9
    CLASSIC_WET = 10
    F2_SUPERSOFT = 11
    F2_SOFT = 12
    F2_MEDIUM = 13
    F2_HARD = 14
    F2_19_WET = 15
    F2_19_SUPERSOFT = 19
    F2_19_SOFT = 20
    F2_19_MEDIUM = 21
    F2_19_HARD = 22
    F2_ULTRASOFT = 23
    F2_2020_SOFT = 24
    NO_TYRES = 25

VehicleFiaFlags = ZoneFlag

class ReadyStatus(SentenceCase):
    NOT_RECEIVED = None
    NOT_READY = 0
    READY = 1
    SPECTATING = 2

class ErsDeployMode(TitleCase):
    NOT_RECEIVED = None
    NONE = 0
    MEDIUM = 1
    HOTLATP = 2
    OVERTAKE = 3

class DrsFault(TitleCase):
    NOT_RECEIVED = None
    OK = 0
    FAULT = 1

class PacketIDs(TitleCase):
    NOT_RECEIVED = None
    MOTION = 0 # Contains all motion data for player’s car – only sent while player is in control
    SESSION = 1 # Data about the session – track, time left
    LAP_DATA = 2 # Data about all the lap times of cars in the session
    EVENT = 3 # Various notable events that happen during a session
    PARTICIPANTS = 4 # List of participants in the session, mostly relevant for multiplayer
    CAR_SETUPS = 5 # Packet detailing car setups for cars in the race
    CAR_TELEMETRY = 6 # Telemetry data for all cars
    CAR_STATUS = 7 # Status data for all cars
    FINAL_CLASSIFICATION = 8 # Final classification confirmation at the end of a race
    LOBBY_INFO = 9 # Information about players in a multiplayer lobby
    CAR_DAMAGE = 10 # Damage status for all cars
    SESSION_HISTORY = 11 # Lap and tyre data for session

class EventStringCodes(SentenceCase):
    NOT_RECEIVED = None
    BUTTON_STATUS = 'BUTN' # Button status changed
    CHEQUERED_FLAG = 'CHQF' # The chequered flag has been waved
    DRS_DISABLED = 'DRSD' # Race control have disabled DRS
    DRS_ENABLED = 'DRSE' # Race control have enabled DRS
    DRIVE_THROUGH_SERVED = 'DTSV' # Drive through penalty served
    FLASHBACK = 'FLBK' # Flashback activated
    FASTEST_LAP = 'FTLP' # When a driver achieves the fastest lap
    LIGHTS_OUT = 'LGOT' # Lights out
    PENALTY_ISSUED = 'PENA' # A penalty has been issued – details in event
    RACE_WINNER = 'RCWN' # The race winner is announced
    RETIREMENT = 'RTMT' # When a driver retires
    SESSION_ENDED = 'SEND' # Sent when the session ends
    STOP_GO_SERVED = 'SGSV' # Stop go penalty served
    SPEED_TRAP_TRIGGERED = 'SPTP' # Speed trap has been triggered by fastest speed
    SESSION_STARTED = 'SSTA' # Sent when the session starts
    START_LIGHTS = 'STLG' # Start lights – number shown
    TEAM_MATE_IN_PITS = 'TMPT' # Your team mate has entered the pits

class TeamIDs(TitleCase):
    NOT_RECEIVED = None
    UNKNOWN = 255
    MERCEDES = 0
    FERRARI = 1
    RED_BULL_RACING = 2
    WILLIAMS = 3
    ASTON_MARTIN = 4
    ALPINE = 5
    ALPHA_TAURI = 6
    HAAS = 7
    MCLAREN = 8
    ALFA_ROMEO = 9
    ART_GP_2019 = 42
    CAMPOS_2019 = 43
    CARLIN_2019 = 44
    SAUBER_JUNIOR_CHAROUZ_2019 = 45
    DAMS_2019 = 46
    UNI_VIRTUOSI_2019 = 47
    MP_MOTORSPORT_2019 = 48
    PREMA_2019 = 49
    TRIDENT_2019 = 50
    ARDEN_2019 = 51
    ART_GP_2020 = 70
    CAMPOS_2020 = 71
    CARLIN_2020 = 72
    CHAROUZ_2020 = 73
    DAMS_2020 = 74
    UNI_VIRTUOSI_2020 = 75
    MP_MOTORSPORT_2020 = 76
    PREMA_2020 = 77
    TRIDENT_2020 = 78
    BWT_2020 = 79
    HITECH_2020 = 80
    MERCEDES_2020 = 85
    FERRARI_2020 = 86
    RED_BULL_2020 = 87
    WILLIAMS_2020 = 88
    RACING_POINT_2020 = 89
    RENAULT_2020 = 90
    ALPHA_TAURI_2020 = 91
    HAAS_2020 = 92
    MCLAREN_2020 = 93
    ALFA_ROMEO_2020 = 94
    PREMA_2021 = 106
    UNI_VIRTUOSI_2021 = 107
    CARLIN_2021 = 108
    HITECH_2021 = 109
    ART_GP_2021 = 110
    MP_MOTORSPORT_2021 = 111
    CHAROUZ_2021 = 112
    DAMS_2021 = 113
    CAMPOS_2021 = 114
    BWT_2021 = 115
    TRIDENT_2021 = 116

class DriverIDs(TitleCase):
    NOT_RECEIVED = None
    CARLOS_SAINZ = 0
    DANIIL_KVYAT = 1
    DANIEL_RICCIARDO = 2
    FERNANDO_ALONSO = 3
    FELIPE_MASSA = 4
    KIMI_RAIKKONEN = 6
    LEWIS_HAMILTON = 7
    MAX_VERSTAPPEN = 9
    NICO_HULKENBURG = 10
    KEVIN_MAGNUSSEN = 11
    ROMAIN_GROSJEAN = 12
    SEBASTIAN_VETTEL = 13
    SERGIO_PEREZ = 14
    VALTTERI_BOTTAS = 15
    ESTEBAN_OCON = 17
    LANCE_STROLL = 19
    ARRON_BARNES = 20
    MARTIN_GILES = 21
    ALEX_MURRAY = 22
    LUCAS_ROTH = 23
    IGOR_CORREIA = 24
    SOPHIE_LEVASSEUR = 25
    JONAS_SCHIFFER = 26
    ALAIN_FOREST = 27
    JAY_LETOURNEAU = 28
    ESTO_SAARI = 29
    YASAR_ATIYEH = 30
    CALLISTO_CALABRESI = 31
    NAOTA_IZUM = 32
    HOWARD_CLARKE = 33
    WILHEIM_KAUFMANN = 34
    MARIE_LAURSEN = 35
    FLAVIO_NIEVES = 36
    PETER_BELOUSOV = 37
    KLIMEK_MICHALSKI = 38
    SANTIAGO_MORENO = 39
    BENJAMIN_COPPENS = 40
    NOAH_VISSER = 41
    GERT_WALDMULLER = 42
    JULIAN_QUESADA = 43
    DANIEL_JONES = 44
    ARTEM_MARKELOV = 45
    TADASUKE_MAKINO = 46
    SEAN_GELAEL = 47
    NYCK_DE_VRIES = 48
    JACK_AITKEN = 49
    GEORGE_RUSSELL = 50
    MAXIMILIAN_GUNTHER = 51
    NIREI_FUKUZUMI = 52
    LUCA_GHIOTTO = 53
    LANDO_NORRIS = 54
    SERGIO_SETTE_CAMARA = 55
    LOUIS_DELETRAZ = 56
    ANTONIO_FUOCO = 57
    CHARLES_LECLERC = 58
    PIERRE_GASLY = 59
    ALEXANDER_ALBON = 62
    NICHOLAS_LATIFI = 63
    DORIAN_BOCCOLACCI = 64
    NIKO_KARI = 65
    ROBERTO_MERHI = 66
    ARJUN_MAINI = 67
    ALESSIO_LORANDI = 68
    RUBEN_MEIJER = 69
    RASHID_NAIR = 70
    JACK_TREMBLAY = 71
    DEVON_BUTLER = 72
    LUKAS_WEBER = 73
    ANTONIO_GIOVINAZZI = 74
    ROBERT_KUBICA = 75
    ALAIN_PROST = 76
    AYRTON_SENNA = 77
    NOBUHARU_MATSUSHITA = 78
    NIKITA_MAZEPIN = 79
    GUANYA_ZHOU = 80
    MICK_SCHUMACHER = 81
    CALLUM_ILOTT = 82
    JUAN_MANUEL_CORREA = 83
    JORDAN_KING = 84
    MAHAVEER_RAGHUNATHAN = 85
    TATIANA_CALDERON = 86
    ANTHOINE_HUBERT = 87
    GUILIANO_ALESI = 88
    RALPH_BOSCHUNG = 89
    MICHAEL_SCHUMACHER = 90
    DAN_TICKTUM = 91
    MARCUS_ARMSTRONG = 92
    CHRISTIAN_LUNDGAARD = 93
    YUKI_TSUNODA = 94
    JEHAN_DARUVALA = 95
    GULHERME_SAMAIA = 96
    PEDRO_PIQUET = 97
    FELIPE_DRUGOVICH = 98
    ROBERT_SCHWARTZMAN = 99
    ROY_NISSANY = 100
    MARINO_SATO = 101
    AIDAN_JACKSON = 102
    CASPER_AKKERMAN = 103
    JENSON_BUTTON = 109
    DAVID_COULTHARD = 110
    NICO_ROSBERG = 111
    OSCAR_PIASTRI = 112
    LIAM_LAWSON = 113
    JURI_VIPS = 114
    THEO_POURCHAIRE = 115
    RICHARD_VERSCHOOR = 116
    LIRIM_ZENDELI = 117
    DAVID_BECKMANN = 118
    GIANLUCA_PETECOF = 119
    MATTEO_NANNINI = 120
    ALESSIO_DELEDDA = 121
    BENT_VISCAAL = 122
    ENZO_FITTIPALDI = 123
    UNKNOWN_PLAYER_NETWORK = 255

class TrackIDs(TitleCase):
    NOT_RECEIVED = None
    UNKNOWN = -1
    MELBOURNE = 0
    PAUL_RICARD = 1
    SHANGHAI = 2
    SAKHIR_BAHRAIN = 3
    CATALUNYA = 4
    MONACO = 5
    MONTREAL = 6
    SILVERSTONE = 7
    HOCKENHEIM = 8
    HUNGARORING = 9
    SPA = 10
    MONZA = 11
    SINGAPORE = 12
    SUZUKA = 13
    ABU_DHABI = 14
    TEXAS = 15
    BRAZIL = 16
    AUSTRIA = 17
    SOCHI = 18
    MEXICO = 19
    BAKU_AZERBAIJAN = 20
    SAKHIR_SHORT = 21
    SILVERSTONE_SHORT = 22
    TEXAS_SHORT = 23
    SUZUKA_SHORT = 24
    HANOI = 25
    ZANDVOORT = 26
    IMOLA = 27
    PORTIMAO = 28
    JEDDAH = 29

class NationalityIDs(TitleCase):
    NONE = 0
    NOT_RECEIVED = None
    AMERICAN = 1
    ARGENTINEAN = 2
    AUSTRALIAN = 3
    AUSTRIAN = 4
    AZERBAIJANI = 5
    BAHRAINI = 6
    BELGIAN = 7
    BOLIVIAN = 8
    BRAZILIAN = 9
    BRITISH = 10
    BULGARIAN = 11
    CAMEROONIAN = 12
    CANADIAN = 13
    CHILEAN = 14
    CHINESE = 15
    COLOMBIAN = 16
    COSTA_RICAN = 17
    CROATIAN = 18
    CYPRIOT = 19
    CZECH = 20
    DANISH = 21
    DUTCH = 22
    ECUADORIAN = 23
    ENGLISH = 24
    EMIRIAN = 25
    ESTONIAN = 26
    FINNISH = 27
    FRENCH = 28
    GERMAN = 29
    GHANAIAN = 30
    GREEK = 31
    GUATEMALAN = 32
    HONDURAN = 33
    HONG_KONGER = 34
    HUNGARIAN = 35
    ICELANDER = 36
    INDIAN = 37
    INDONESIAN = 38
    IRISH = 39
    ISRAELI = 40
    ITALIAN = 41
    JAMAICAN = 42
    JAPANESE = 43
    JORDANIAN = 44
    KUWAITI = 45
    LATVIAN = 46
    LEBANESE = 47
    LITHUANIAN = 48
    LUXEMBOURGER = 49
    MALAYSIAN = 50
    MALTESE = 51
    MEXICAN = 52
    MONEGASQUE = 53
    NEW_ZEALANDER = 54
    NICARAGUAN = 55
    NORTHERN_IRISH = 56
    NORWEGIAN = 57
    OMANI = 58
    PAKISTANI = 59
    PANAMANIAN = 60
    PARAGUAYAN = 61
    PERUVIAN = 62
    POLISH = 63
    PORTUGUESE = 64
    QATARI = 65
    ROMANIAN = 66
    RUSSIAN = 67
    SALVADORAN = 68
    SAUDI = 69
    SCOTTISH = 70
    SERBIAN = 71
    SINGAPOREAN = 72
    SLOVAKIAN = 73
    SLOVENIAN = 74
    SOUTH_KOREAN = 75
    SOUTH_AFRICAN = 76
    SPANISH = 77
    SWEDISH = 78
    SWISS = 79
    THAI = 80
    TURKISH = 81
    URUGUAYAN = 82
    UKRAINIAN = 83
    VENEZUELAN = 84
    BARBADIAN = 85
    WELSH = 86
    VIETNAMESE = 87
    UNKNOWN = 255

class SurfaceTypes(SentenceCase):
    NOT_RECEIVED = None
    TARMAC = 0
    RUMBLE_STRIP = 1
    CONCRETE = 2
    ROCK = 3
    GRAVEL = 4
    MUD = 5
    SAND = 6
    GRASS = 7
    WATER = 8
    COBBLESTONE = 9
    METAL = 10
    RIDGED = 11

class ButtonFlags(TitleCase):
    NOT_RECEIVED = None
    CROSS_OR_A = 0x00000001
    TRIANGLE_OR_Y = 0x00000002
    CIRCLE_OR_B = 0x00000004
    SQUARE_OR_X = 0x00000008
    D_PAD_LEFT = 0x00000010
    D_PAD_RIGHT = 0x00000020
    D_PAD_UP = 0x00000040
    D_PAD_DOWN = 0x00000080
    OPTIONS_OR_MENU = 0x00000100
    L1_OR_LB = 0x00000200
    R1_OR_RB = 0x00000400
    L2_OR_LT = 0x00000800
    R2_OR_RT = 0x00001000
    LEFT_STICK_CLICK = 0x00002000
    RIGHT_STICK_CLICK = 0x00004000
    RIGHT_STICK_LEFT = 0x00008000
    RIGHT_STICK_RIGHT = 0x00010000
    RIGHT_STICK_UP = 0x00020000
    RIGHT_STICK_DOWN = 0x00040000
    SPECIAL = 0x00080000

class Buttons(TitleCase):
    NOT_RECEIVED = None
    NONE = 0
    CROSS_OR_A = 1
    TRIANGLE_OR_Y = 2 
    CIRCLE_OR_B = 3
    SQUARE_OR_X = 4
    D_PAD_LEFT = 5
    D_PAD_RIGHT = 6
    D_PAD_UP = 7
    D_PAD_DOWN = 8 
    OPTIONS_OR_MENU = 9
    L1_OR_LB = 10
    R1_OR_RB = 11
    L2_OR_LT = 12
    R2_OR_RT = 13
    LEFT_STICK_CLICK = 14
    RIGHT_STICK_CLICK = 15
    RIGHT_STICK_LEFT = 16
    RIGHT_STICK_RIGHT = 17
    RIGHT_STICK_UP = 18
    RIGHT_STICK_DOWN = 19
    SPECIAL = 20

class PenaltyTypes(SentenceCase):
    NOT_RECEIVED = None
    DRIVE_THROUGH_PENALTY = 0
    STOP_GO_PENALTY = 1
    GRID_PENALTY = 2
    PENALTY_REMINDER = 3
    TIME_PENALTY = 4
    WARNING = 5
    DISQUALIFIED = 6
    REMOVED_FROM_FORMATION_LAP = 7
    PARKED_TOO_LONG_TIMER = 8
    TYRE_REGULATIONS = 9
    THIS_LAP_INVALIDATED = 10
    THIS_AND_NEXT_LAP_INVALIDATED = 11
    THIS_LAP_INVALIDATED_WITHOUT_REASON = 12
    THIS_AND_NEXT_LAP_INVALIDATED_WITHOUT_REASON = 13
    THIS_AND_PREVIOUS_LAP_INVALIDATED = 14
    THIS_AND_PREVIOUS_LAP_INVALIDATED_WITHOUT_REASON = 15
    RETIRED = 16
    BLACK_FLAG_TIMER = 17

class InfringementTypes(SentenceCase):
    NOT_RECEIVED = None
    BLOCKING_BY_SLOW_DRIVING = 0
    BLOCKING_BY_WRONG_WAY_DRIVING = 1
    REVERSING_OFF_THE_START_LINE = 2
    BIG_COLLISION = 3
    SMALL_COLLISION = 4
    COLLISION_FAILED_TO_HAND_BACK_POSITION_SINGLE = 5
    COLLISION_FAILED_TO_HAND_BACK_POSITION_MULTIPLE = 6
    CORNER_CUTTING_GAINED_TIME = 7
    CORNER_CUTTING_OVERTAKE_SINGLE = 8
    CORNER_CUTTING_OVERTAKE_MULTIPLE = 9
    CROSSED_PIT_EXIT_LANE = 10
    IGNORING_BLUE_FLAGS = 11
    IGNORING_YELLOW_FLAGS = 12
    IGNORING_DRIVE_THROUGH = 13
    TOO_MANY_DRIVE_THROUGHS = 14
    DRIVE_THROUGH_REMINDER_SERVE_WITHIN_N_LAPS = 15
    DRIVE_THROUGH_REMINDER_SERVE_THIS_LAP = 16
    PIT_LANE_SPEEDING = 17
    PARKED_FOR_TOO_LONG = 18
    IGNORING_TYRE_REGULATIONS = 19
    TOO_MANY_PENALTIES = 20
    MULTIPLE_WARNINGS = 21
    APPROACHING_DISQUALIFICATION = 22
    TYRE_REGULATIONS_SELECT_SINGLE = 23
    TYRE_REGULATIONS_SELECT_MULTIPLE = 24
    LAP_INVALIDATED_CORNER_CUTTING = 25
    LAP_INVALIDATED_RUNNING_WIDE = 26
    CORNER_CUTTING_RAN_WIDE_GAINED_TIME_MINOR = 27
    CORNER_CUTTING_RAN_WIDE_GAINED_TIME_SIGNIFICANT = 28
    CORNER_CUTTING_RAN_WIDE_GAINED_TIME_EXTREME = 29
    LAP_INVALIDATED_WALL_RIDING = 30
    LAP_INVALIDATED_FLASHBACK_USED = 31
    LAP_INVALIDATED_RESET_TO_TRACK = 32
    BLOCKING_THE_PITLANE = 33
    JUMP_START = 34
    SAFETY_CAR_TO_CAR_COLLISION = 35
    SAFETY_CAR_ILLEGAL_OVERTAKE = 36
    SAFETY_CAR_EXCEEDING_ALLOWED_PACE = 37
    VIRTUAL_SAFETY_CAR_EXCEEDING_ALLOWED_PACE = 38
    FORMATION_LAP_BELOW_ALLOWED_SPEED = 39
    RETIRED_MECHANICAL_FAILURE = 40
    RETIRED_TERMINALLY_DAMAGED = 41
    SAFETY_CAR_FALLING_TOO_FAR_BACK = 42
    BLACK_FLAG_TIMER = 43
    UNSERVED_STOP_GO_PENALTY = 44
    UNSERVED_DRIVE_THROUGH_PENALTY = 45
    ENGINE_COMPONENT_CHANGE = 46
    GEARBOX_CHANGE = 47
    LEAGUE_GRID_PENALTY = 48
    RETRY_PENALTY = 49
    ILLEGAL_TIME_GAIN = 50
    MANDATORY_PITSTOP = 51

