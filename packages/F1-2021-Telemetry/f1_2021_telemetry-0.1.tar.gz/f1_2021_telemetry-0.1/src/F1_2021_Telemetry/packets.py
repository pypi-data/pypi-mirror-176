import struct
from F1_2021_Telemetry import defs, utils

class Packet():
    def unpack(self, rawData):
        return struct.unpack('<' + self.formatString, rawData[:self.size])

    def __init__(self, data, bytes=False):
        if data is None:
            data = [None for _ in range(len(self.formatString))]
        elif bytes:
            data = self.unpack(data)
        return data

class WheelArray():
    def __init__(self, data: list):
        self.RL, self.RR, self.FL, self.FR = data
    def __str__(self):
        return f"FL: {self.FL}, FR: {self.FR}, RL: {self.RL}, RR: {self.RR}"

class PacketHeader(Packet):
    size = 24
    formatString = 'HBBBBQfIBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_packetFormat = data[0] # 2021
        self.m_gameMajorVersion = data[1] # Game major version - "X.00"
        self.m_gameMinorVersion = data[2] # Game minor version - "1.XX"
        self.m_packetVersion = data[3] # Version of this packet type, all start from 1
        self.m_packetId = defs.PacketIDs(data[4]) # Identifier for the packet type, see below
        self.m_sessionUID = data[5] # Unique identifier for the session
        self.m_sessionTime = data[6] # Session timestamp
        self.m_frameIdentifier = data[7] # Identifier for the frame the data was retrieved on
        self.m_playerCarIndex = data[8] # Index of player's car in the array
        self.m_secondaryPlayerCarIndex = data[9] # Index of secondary player's car in the array (splitscreen) 255 if no second player

class CarMotionData(Packet):
    size = 60
    formatString = 'ffffffhhhhhhffffff'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_worldPositionX = data[0] # World space X position
        self.m_worldPositionY = data[1] # World space Y position
        self.m_worldPositionZ = data[2] # World space Z position
        self.m_worldVelocityX = data[3] # Velocity in world space X
        self.m_worldVelocityY = data[4] # Velocity in world space Y
        self.m_worldVelocityZ = data[5] # Velocity in world space Z
        self.m_worldForwardDirX = utils.convToFloat(data[6]) # World space forward X direction (normalised)
        self.m_worldForwardDirY = utils.convToFloat(data[7]) # World space forward Y direction (normalised)
        self.m_worldForwardDirZ = utils.convToFloat(data[8]) # World space forward Z direction (normalised)
        self.m_worldRightDirX = utils.convToFloat(data[9]) # World space right X direction (normalised)
        self.m_worldRightDirY = utils.convToFloat(data[10]) # World space right Y direction (normalised)
        self.m_worldRightDirZ = utils.convToFloat(data[11]) # World space right Z direction (normalised)
        self.m_gForceLateral = data[12] # Lateral G-Force component
        self.m_gForceLongitudinal = data[13] # Longitudinal G-Force component
        self.m_gForceVertical = data[14] # Vertical G-Force component
        self.m_yawRadians = data[15] # Yaw angle in radians
        self.m_pitchRadians = data[16] # Pitch angle in radians
        self.m_rollRadians = data[17] # Roll angle in radians

class PacketMotionData(Packet):
    size = 1464
    formatString = 'HBBBBQfIBBffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffhhhhhhffffffffffffffffffffffffffffffffffff'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10]) # Header
        self.m_carMotionData = [CarMotionData(data[i:i + 18]) for i in range(10, 406, 18)] # Data for all cars on track Extra player car ONLY data
        self.m_suspensionPosition = WheelArray(data[406:410])# Note: All wheel arrays have the following order:
        self.m_suspensionVelocity = WheelArray(data[410:414]) # RL, RR, FL, FR
        self.m_suspensionAcceleration = WheelArray(data[414:418]) # RL, RR, FL, FR
        self.m_wheelSpeed = WheelArray(data[418:422]) # Speed of each wheel
        self.m_wheelSlip = WheelArray(data[422:426]) # Slip ratio for each wheel
        self.m_localVelocityX = data[426] # Velocity in local space
        self.m_localVelocityY = data[427] # Velocity in local space
        self.m_localVelocityZ = data[428] # Velocity in local space
        self.m_angularVelocityX = data[429] # Angular velocity x-component
        self.m_angularVelocityY = data[430] # Angular velocity y-component
        self.m_angularVelocityZ = data[431] # Angular velocity z-component
        self.m_angularAccelerationX = data[432] # Angular velocity x-component
        self.m_angularAccelerationY = data[433] # Angular velocity y-component
        self.m_angularAccelerationZ = data[434] # Angular velocity z-component
        self.m_frontWheelsAngleRadians = data[435] # Current front wheels angle in radians

class MarshalZone(Packet):
    size = 5
    formatString = 'fb'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_zoneStart = data[0] # Fraction (0..1) of way through the lap the marshal zone starts
        self.m_zoneFlag = defs.ZoneFlag(data[1]) # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red

class WeatherForecastSample(Packet):
    size = 8
    formatString = 'BBBbbbbB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_sessionType = defs.SessionType(data[0]) # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2 12 = Time Trial
        self.m_timeOffsetMinutes = data[1] # Time in minutes the forecast is for
        self.m_weather = defs.Weather(data[2]) # Weather - 0 = clear, 1 = light cloud, 2 = overcast 3 = light rain, 4 = heavy rain, 5 = storm
        self.m_trackTemperatureCelsius = data[3] # Track temp. in degrees Celsius
        self.m_trackTemperatureChange = defs.TrackTemperatureChange(data[4]) # Track temp. change – 0 = up, 1 = down, 2 = no change
        self.m_airTemperatureCelsius = data[5] # Air temp. in degrees celsius
        self.m_airTemperatureChange = defs.AirTemperatureChange(data[6]) # Air temp. change – 0 = up, 1 = down, 2 = no change
        self.m_rainPercentage = data[7] # Rain percentage (0-100)

class PacketSessionData(Packet):
    size = 625
    formatString = 'HBBBBQfIBBBbbBHBbBHHBBBBBBfbfbfbfbfbfbfbfbfbfbfbfbfbfbfbfbfbfbfbfbfbBBBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBBbbbbBBBIIIBBBBBBBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10]) # Header
        self.m_weather = defs.Weather(data[10]) # Weather - 0 = clear, 1 = light cloud, 2 = overcast 3 = light rain, 4 = heavy rain, 5 = storm
        self.m_trackTemperatureCelsius = data[11] # Track temp. in degrees celsius
        self.m_airTemperatureCelsius = data[12] # Air temp. in degrees celsius
        self.m_totalLaps = data[13] # Total number of laps in this race
        self.m_trackLengthMetres = data[14] # Track length in metres
        self.m_sessionType = defs.SessionType(data[15]) # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ 10 = R, 11 = R2, 12 = R3, 13 = Time Trial
        self.m_trackId = defs.TrackIDs(data[16]) # -1 for unknown, 0-21 for tracks, see appendix
        self.m_formula = defs.Formula(data[17]) # Formula, 0 = F1 Modern, 1 = F1 Classic, 2 = F2, 3 = F1 Generic
        self.m_sessionTimeLeftSeconds = data[18] # Time left in session in seconds
        self.m_sessionDurationSeconds = data[19] # Session duration in seconds
        self.m_pitSpeedLimitKMH = data[20] # Pit speed limit in kilometres per hour
        self.m_gamePaused = bool(data[21]) # Whether the game is paused
        self.m_isSpectating = bool(data[22]) # Whether the player is spectating
        self.m_spectatorCarIndex = data[23] # Index of the car being spectated
        self.m_sliProNativeSupport = defs.SliProNativeSupport(data[24]) # SLI Pro support, 0 = inactive, 1 = active
        self.m_numMarshalZones = data[25] # Number of marshal zones to follow
        self.m_marshalZones = [MarshalZone(data[i:i + 2]) for i in range(26, 68, 2)] # List of marshal zones – max 21
        self.m_safetyCarStatus = defs.SafetyCarStatus(data[68]) # 0 = no safety car, 1 = full 2 = virtual, 3 = formation lap
        self.m_networkGame = defs.NetworkGame(data[69]) # 0 = offline, 1 = online
        self.m_numWeatherForecastSamples = data[70] # Number of weather samples to follow
        self.m_weatherForecastSamples = [WeatherForecastSample(data[i:i + 8]) for i in range(71, 519, 8)] # Array of weather forecast samples
        self.m_forecastAccuracy = defs.ForecastAccuracy(data[519]) # 0 = Perfect, 1 = Approximate
        self.m_aiDifficulty = data[520] # AI Difficulty rating – 0-110
        self.m_seasonLinkIdentifier = data[521] # Identifier for season - persists across saves
        self.m_weekendLinkIdentifier = data[522] # Identifier for weekend - persists across saves
        self.m_sessionLinkIdentifier = data[523] # Identifier for session - persists across saves
        self.m_pitStopWindowIdealLap = data[524] # Ideal lap to pit on for current strategy (player)
        self.m_pitStopWindowLatestLap = data[525] # Latest lap to pit on for current strategy (player)
        self.m_pitStopRejoinPosition = data[526] # Predicted position to rejoin at (player)
        self.m_steeringAssist = defs.SteeringAssist(data[527]) # 0 = off, 1 = on
        self.m_brakingAssist = defs.BrakingAssist(data[528]) # 0 = off, 1 = low, 2 = medium, 3 = high
        self.m_gearboxAssist = defs.GearboxAssist(data[529]) # 1 = manual, 2 = manual & suggested gear, 3 = auto
        self.m_pitAssist = defs.PitAssist(data[530]) # 0 = off, 1 = on
        self.m_pitReleaseAssist = defs.PitReleaseAssist(data[531]) # 0 = off, 1 = on
        self.m_ERSAssist = defs.ERSAssist(data[532]) # 0 = off, 1 = on
        self.m_DRSAssist = defs.DRSAssist(data[533]) # 0 = off, 1 = on
        self.m_dynamicRacingLine = defs.DynamicRacingLine(data[534]) # 0 = off, 1 = corners only, 2 = full
        self.m_dynamicRacingLineType = defs.DynamicRacingLineType(data[535]) # 0 = 2D, 1 = 3D

class LapData(Packet):
    size = 43
    formatString = 'IIHHfffBBBBBBBBBBBBBBHHB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_lastLapTimeInMS = data[0] # Last lap time in milliseconds
        self.m_currentLapTimeInMS = data[1] # Current time around the lap in milliseconds
        self.m_sector1TimeInMS = data[2] # Sector 1 time in milliseconds
        self.m_sector2TimeInMS = data[3] # Sector 2 time in milliseconds
        self.m_lapDistanceMetres = data[4] # Distance vehicle is around current lap in metres – could be negative if line hasn’t been crossed yet
        self.m_totalDistanceMetres = data[5] # Total distance travelled in session in metres – could be negative if line hasn’t been crossed yet
        self.m_safetyCarDeltaSeconds = data[6] # Delta in seconds for safety car
        self.m_carPosition = data[7] # Car race position
        self.m_currentLapNum = data[8] # Current lap number
        self.m_pitStatus = defs.PitStatus(data[9]) # 0 = none, 1 = pitting, 2 = in pit area
        self.m_numPitStops = data[10] # Number of pit stops taken in this race
        self.m_sector = defs.Sector(data[11]) # 0 = sector1, 1 = sector2, 2 = sector3
        self.m_currentLapInvalid = bool(data[12]) # Current lap invalid - False = valid, True = invalid
        self.m_penalties = data[13] # Accumulated time penalties in seconds to be added
        self.m_warnings = data[14] # Accumulated number of warnings issued
        self.m_numUnservedDriveThroughPens = data[15] # Num drive through pens left to serve
        self.m_numUnservedStopGoPens = data[16] # Num stop go pens left to serve
        self.m_gridPosition = data[17] # Grid position the vehicle started the race in
        self.m_driverStatus = defs.DriverStatus(data[18]) # Status of driver - 0 = in garage, 1 = flying lap 2 = in lap, 3 = out lap, 4 = on track
        self.m_resultStatus = defs.ResultStatus(data[19]) # Result status - 0 = invalid, 1 = inactive, 2 = active 3 = finished, 4 = didnotfinish, 5 = disqualified 6 = not classified, 7 = retired
        self.m_pitLaneTimerActive = bool(data[20]) # Pit lane timing, False = inactive, True = active
        self.m_pitLaneTimeInLaneInMS = data[21] # If active, the current time spent in the pit lane in ms
        self.m_pitStopTimerInMS = data[22] # Time of the actual pit stop in ms
        self.m_pitStopShouldServePen = bool(data[23]) # Whether the car should serve a penalty at this stop

class PacketLapData(Packet):
    size = 970
    formatString = 'HBBBBQfIBBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHBIIHHfffBBBBBBBBBBBBBBHHB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10]) # Header
        self.m_lapData = [LapData(data[i:i + 24]) for i in range(10, 538, 24)] # Lap data for all cars on track

class FastestLap(Packet):
    size = 5
    formatString = 'Bf'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.vehicleIdx = data[0] # Vehicle index of car achieving fastest lap
        self.lapTimeSeconds = data[1] # Lap time is in seconds

class PacketFastestLap(Packet):
    size = 28 + 5
    formatString = 'HBBBBQfIBBBBBB' + 'Bf'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10])
        self.m_eventStringCode = defs.EventStringCodes(utils.convToString(data[10:14]))
        self.m_eventDetails = FastestLap(data[14:16])

class Retirement(Packet):
    size = 1
    formatString = 'B'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.vehicleIdx = data[0] # Vehicle index of car retiring

class PacketRetirement(Packet):
    size = 28 + 1
    formatString = 'HBBBBQfIBBBBBB' + 'B'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10])
        self.m_eventStringCode = defs.EventStringCodes(utils.convToString(data[10:14]))
        self.m_eventDetails = Retirement(data[14:15])

class TeamMateInPits(Packet):
    size = 1
    formatString = 'B'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.vehicleIdx = data[0] # Vehicle index of team mate

class PacketTeamMateInPits(Packet):
    size = 28 + 1
    formatString = 'HBBBBQfIBBBBBB' + 'B'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10])
        self.m_eventStringCode = defs.EventStringCodes(utils.convToString(data[10:14]))
        self.m_eventDetails = TeamMateInPits(data[14:15])

class RaceWinner(Packet):
    size = 1
    formatString = 'B'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.vehicleIdx = data[0] # Vehicle index of the race winner

class PacketRaceWinner(Packet):
    size = 28 + 1
    formatString = 'HBBBBQfIBBBBBB' + 'B'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10])
        self.m_eventStringCode = defs.EventStringCodes(utils.convToString(data[10:14]))
        self.m_eventDetails = RaceWinner(data[14:15])

class Penalty(Packet):
    size = 7
    formatString = 'BBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.penaltyType = defs.PenaltyTypes(data[0]) # Penalty type – see Appendices
        self.infringementType = defs.InfringementTypes(data[1]) # Infringement type – see Appendices
        self.vehicleIdx = data[2] # Vehicle index of the car the penalty is applied to
        self.otherVehicleIdx = data[3] # Vehicle index of the other car involved
        self.timeSeconds = data[4] # Time gained, or time spent doing action in seconds
        self.lapNum = data[5] # Lap the penalty occurred on
        self.placesGained = data[6] # Number of places gained by this

class PacketPenalty(Packet):
    size = 28 + 7
    formatString = 'HBBBBQfIBBBBBB' + 'BBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10])
        self.m_eventStringCode = defs.EventStringCodes(utils.convToString(data[10:14]))
        self.m_eventDetails = Penalty(data[14:21])

class SpeedTrap(Packet):
    size = 7
    formatString = 'BfBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.vehicleIdx = data[0] # Vehicle index of the vehicle triggering speed trap
        self.speedKMH = data[1] # Top speed achieved in kilometres per hour
        self.overallFastestInSession = bool(data[2]) # Overall fastest speed in session = True, otherwise False
        self.driverFastestInSession = bool(data[3]) # Fastest speed for driver in session = True, otherwise False

class PacketSpeedTrap(Packet):
    size = 28 + 7
    formatString = 'HBBBBQfIBBBBBB' + 'BfBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10])
        self.m_eventStringCode = defs.EventStringCodes(utils.convToString(data[10:14]))
        self.m_eventDetails = SpeedTrap(data[14:18])

class StartLights(Packet):
    size = 1
    formatString = 'B'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.numLights = data[0] # Number of lights showing

class PacketStartLights(Packet):
    size = 28 + 1
    formatString = 'HBBBBQfIBBBBBB' + 'B'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10])
        self.m_eventStringCode = defs.EventStringCodes(utils.convToString(data[10:14]))
        self.m_eventDetails = StartLights(data[14:15])

class DriveThroughPenaltyServed(Packet):
    size = 1
    formatString = 'B'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.vehicleIdx = data[0] # Vehicle index of the vehicle serving drive through

class PacketDriveThroughPenaltyServed(Packet):
    size = 28 + 1
    formatString = 'HBBBBQfIBBBBBB' + 'B'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10])
        self.m_eventStringCode = defs.EventStringCodes(utils.convToString(data[10:14]))
        self.m_eventDetails = DriveThroughPenaltyServed(data[14:15])

class StopGoPenaltyServed(Packet):
    size = 1
    formatString = 'B'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.vehicleIdx = data[0] # Vehicle index of the vehicle serving stop go

class PacketStopGoPenaltyServed(Packet):
    size = 28 + 1
    formatString = 'HBBBBQfIBBBBBB' + 'B'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10])
        self.m_eventStringCode = defs.EventStringCodes(utils.convToString(data[10:14]))
        self.m_eventDetails = StopGoPenaltyServed(data[14:15])

class Flashback(Packet):
    size = 8
    formatString = 'If'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.flashbackFrameIdentifier = data[0] # Frame identifier flashed back to
        self.flashbackSessionTime = data[1] # Session time flashed back to

class PacketFlashback(Packet):
    size = 28 + 8
    formatString = 'HBBBBQfIBBBBBB' + 'If'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10])
        self.m_eventStringCode = defs.EventStringCodes(utils.convToString(data[10:14]))
        self.m_eventDetails = Flashback(data[14:16])

class Buttons(Packet):
    size = 4
    formatString = 'I'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_buttonStatus = data[0] # Bit flags specifying which buttons are being pressed currently - see appendices
        self.m_selectedButtons = [defs.Buttons[button.name] for button in defs.ButtonFlags if button.value is not None and button.value & self.m_buttonStatus]

class PacketButtons(Packet):
    size = 28 + 4
    formatString = 'HBBBBQfIBBBBBB' + 'I'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10])
        self.m_eventStringCode = defs.EventStringCodes(utils.convToString(data[10:14]))
        self.m_eventDetails = Buttons(data[14:15])

class PacketSimpleEvent(Packet):
    size = 28
    formatString = 'HBBBBQfIBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10])
        self.m_eventStringCode = defs.EventStringCodes(utils.convToString(data[10:14]))

class ParticipantData(Packet):
    size = 56
    formatString = 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_aiControlled = bool(data[0]) # Whether the vehicle is AI (1) or Human (0) controlled
        self.m_driverId = defs.DriverIDs(data[1]) # Driver id - see appendix, 255 if network human
        self.m_networkId = data[2] # Network id – unique identifier for network players
        self.m_teamId = data[3] # Team id - see appendix
        self.m_myTeam = bool(data[4]) # My team flag – 1 = My Team, 0 = otherwise
        self.m_raceNumber = data[5] # Race number of the car
        self.m_nationality = defs.NationalityIDs(data[6]) # Nationality of the driver
        self.m_name = utils.convToString(data[7:55]) #Name of participant in UTF-8 format – null terminated Will be truncated with … (U+2026) if too long
        self.m_yourTelemetry = defs.YourTelemetry(data[55]) # The player's UDP setting, 0 = restricted, 1 = public

class PacketParticipantsData(Packet):
    size = 1257
    formatString = 'HBBBBQfIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10]) # Header
        self.m_numActiveCars = data[10] # Number of active cars in the data – should match number of cars on HUD
        self.m_participants = [ParticipantData(data[i:i + 56]) for i in range(11, 1243, 56)] 

class CarSetupData(Packet):
    size = 49
    formatString = 'BBBBffffBBBBBBBBffffBf'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_frontWing = data[0] # Front wing aero
        self.m_rearWing = data[1] # Rear wing aero
        self.m_onThrottlePercent = data[2] # Differential adjustment on throttle (percentage)
        self.m_offThrottlePercent = data[3] # Differential adjustment off throttle (percentage)
        self.m_frontCamber = data[4] # Front camber angle (suspension geometry)
        self.m_rearCamber = data[5] # Rear camber angle (suspension geometry)
        self.m_frontToe = data[6] # Front toe angle (suspension geometry)
        self.m_rearToe = data[7] # Rear toe angle (suspension geometry)
        self.m_frontSuspension = data[8] # Front suspension
        self.m_rearSuspension = data[9] # Rear suspension
        self.m_frontAntiRollBar = data[10] # Front anti-roll bar
        self.m_rearAntiRollBar = data[11] # Front anti-roll bar
        self.m_frontSuspensionHeight = data[12] # Front ride height
        self.m_rearSuspensionHeight = data[13] # Rear ride height
        self.m_brakePressurePercent = data[14] # Brake pressure (percentage)
        self.m_brakeBiasPercent = data[15] # Brake bias (percentage)
        self.m_rearLeftTyrePressurePSI = data[16] # Rear left tyre pressure (PSI)
        self.m_rearRightTyrePressurePSI = data[17] # Rear right tyre pressure (PSI)
        self.m_frontLeftTyrePressurePSI = data[18] # Front left tyre pressure (PSI)
        self.m_frontRightTyrePressurePSI = data[19] # Front right tyre pressure (PSI)
        self.m_ballast = data[20] # Ballast
        self.m_fuelLoad = data[21] # Fuel load

class PacketCarSetupData(Packet):
    size = 1102
    formatString = 'HBBBBQfIBBBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBfBBBBffffBBBBBBBBffffBf'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10]) # Header
        self.m_carSetups = [CarSetupData(data[i:i + 22]) for i in range(10, 494, 22)] 

class CarTelemetryData(Packet):
    size = 60
    formatString = 'HfffBbHBBHHHHHBBBBBBBBHffffBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_speedKMH = data[0] # Speed of car in kilometres per hour
        self.m_throttle = data[1] # Amount of throttle applied (0.0 to 1.0)
        self.m_steer = data[2] # Steering (-1.0 (full lock left) to 1.0 (full lock right))
        self.m_brake = data[3] # Amount of brake applied (0.0 to 1.0)
        self.m_clutchPercent = data[4] # Amount of clutch applied (0 to 100)
        self.m_gear = defs.Gear(data[5]) # Gear selected (1-8, N=0, R=-1)
        self.m_engineRPM = data[6] # Engine RPM
        self.m_drs = defs.Drs(data[7]) # 0 = off, 1 = on
        self.m_revLightsPercent = data[8] # Rev lights indicator (percentage)
        self.m_revLightsList = utils.bitsToList(data[9], length=15, descending=False) # Rev lights (index 0 = leftmost LED, index 14 = rightmost LED)
        self.m_brakesTemperatureCelsius = data[10:14] # Brakes temperature (celsius)
        self.m_tyresSurfaceTemperature = WheelArray(data[14:18]) # Tyres surface temperature (celsius)
        self.m_tyresInnerTemperature = WheelArray(data[18:22]) # Tyres inner temperature (celsius)
        self.m_engineTemperatureCelsius = data[22] # Engine temperature (celsius)
        self.m_tyresPressurePSI = data[23:27] # Tyres pressure (PSI)
        self.m_surfaceType = WheelArray([defs.SurfaceTypes(surface) for surface in data[27:31]]) # Driving surface, see appendices

class PacketCarTelemetryData(Packet):
    size = 1347
    formatString = 'HBBBBQfIBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBHfffBbHBBHHHHHBBBBBBBBHffffBBBBBBb'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10]) # Header
        self.m_carTelemetryData = [CarTelemetryData(data[i:i + 31]) for i in range(10, 692, 31)] 
        self.m_mfdPanel = defs.MfdPanel(data[692]) # Index of MFD panel open - 255 = MFD closed Single player, race – 0 = Car setup, 1 = Pits 2 = Damage, 3 = Engine, 4 = Temperatures May vary depending on game mode
        self.m_mfdPanelSecondaryPlayer = defs.MfdPanel(data[693]) # See above
        self.m_suggestedGear = data[694] # Suggested gear for the player (1-8) 0 if no gear suggested

class CarStatusData(Packet):
    size = 47
    formatString = 'BBBBBfffHHBBHBBBbfBfffB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_tractionControl = defs.TractionControl(data[0]) # Traction control - 0 = off, 1 = medium, 2 = full
        self.m_antiLockBrakes = defs.AntiLockBrakes(data[1]) # 0 (off) - 1 (on)
        self.m_fuelMix = defs.FuelMix(data[2]) # Fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
        self.m_frontBrakeBiasPercent = data[3] # Front brake bias (percentage)
        self.m_pitLimiterStatus = defs.PitLimiterStatus(data[4]) # Pit limiter status - 0 = off, 1 = on
        self.m_fuelInTank = data[5] # Current fuel mass
        self.m_fuelCapacity = data[6] # Fuel capacity
        self.m_fuelRemainingLaps = data[7] # Fuel remaining in terms of laps (value on MFD)
        self.m_maxRPM = data[8] # Cars max RPM, point of rev limiter
        self.m_idleRPM = data[9] # Cars idle RPM
        self.m_maxGears = data[10] # Maximum number of gears
        self.m_drsAllowed = bool(data[11]) # 0 = not allowed, 1 = allowed
        self.m_drsActivationDistance = data[12] # 0 = DRS not available, non-zero - DRS will be available in [X] metres
        self.m_actualTyreCompound = defs.ActualTyreCompound(data[13]) # F1 Modern - 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1 7 = inter, 8 = wet F1 Classic - 9 = dry, 10 = wet F2 – 11 = super soft, 12 = soft, 13 = medium, 14 = hard 15 = wet
        self.m_visualTyreCompound = defs.VisualTyreCompound(data[14]) # F1 visual (can be different from actual compound) 16 = soft, 17 = medium, 18 = hard, 7 = inter, 8 = wet F1 Classic – same as above F2 ‘19, 15 = wet, 19 – super soft, 20 = soft 21 = medium , 22 = hard
        self.m_tyresAgeLaps = data[15] # Age in laps of the current set of tyres
        self.m_vehicleFiaFlags = defs.VehicleFiaFlags(data[16]) # -1 = invalid/unknown, 0 = none, 1 = green 2 = blue, 3 = yellow, 4 = red
        self.m_ersStoreEnergyJoules = data[17] # ERS energy store in Joules
        self.m_ersDeployMode = defs.ErsDeployMode(data[18]) # ERS deployment mode, 0 = none, 1 = medium 2 = hotlap, 3 = overtake
        self.m_ersHarvestedThisLapMGUK = data[19] # ERS energy harvested this lap by MGU-K
        self.m_ersHarvestedThisLapMGUH = data[20] # ERS energy harvested this lap by MGU-H
        self.m_ersDeployedThisLap = data[21] # ERS energy deployed this lap
        self.m_networkPaused = bool(data[22]) # Whether the car is paused in a network game

class PacketCarStatusData(Packet):
    size = 1058
    formatString = 'HBBBBQfIBBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffBBBBBBfffHHBBHBBBbfBfffB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10]) # Header
        self.m_carStatusData = [CarStatusData(data[i:i + 23]) for i in range(10, 516, 23)] 

class FinalClassificationData(Packet):
    size = 37
    formatString = 'BBBBBBIdBBBBBBBBBBBBBBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_position = data[0] # Finishing position
        self.m_numLaps = data[1] # Number of laps completed
        self.m_gridPosition = data[2] # Grid position of the car
        self.m_points = data[3] # Number of points scored
        self.m_numPitStops = data[4] # Number of pit stops made
        self.m_resultStatus = defs.ResultStatus(data[5]) # Result status - 0 = invalid, 1 = inactive, 2 = active 3 = finished, 4 = didnotfinish, 5 = disqualified 6 = not classified, 7 = retired
        self.m_bestLapTimeInMS = data[6] # Best lap time of the session in milliseconds
        self.m_totalRaceTimeSeconds = data[7] # Total race time in seconds without penalties
        self.m_penaltiesTimeSeconds = data[8] # Total penalties accumulated in seconds
        self.m_numPenalties = data[9] # Number of penalties applied to this driver
        self.m_numTyreStints = data[10] # Number of tyres stints up to maximum
        self.m_tyreStintsActual = [defs.ActualTyreCompound(tyre) for tyre in data[11:19]] # Actual tyres used by this driver
        self.m_tyreStintsVisual = [defs.VisualTyreCompound(tyre) for tyre in data[19:27]] # Visual tyres used by this driver

class PacketFinalClassificationData(Packet):
    size = 839
    formatString = 'HBBBBQfIBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBBBBBBBBIdBBBBBBBBBBBBBBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10]) # Header
        self.m_numCars = data[10] # Number of cars in the final classification
        self.m_classificationData = [FinalClassificationData(data[i:i + 27]) for i in range(11, 605, 27)] 

class LobbyInfoData(Packet):
    size = 53
    formatString = 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_aiControlled = bool(data[0]) # Whether the vehicle is AI (1) or Human (0) controlled
        self.m_teamId = defs.TeamIDs(data[1]) # Team id - see appendix (255 if no team currently selected)
        self.m_nationality = defs.NationalityIDs(data[2]) # Nationality of the driver
        self.m_name = utils.convToString(data[3:51]) # Name of participant in UTF-8 format – null terminated Will be truncated with ... (U+2026) if too long
        self.m_carNumber = data[51] # Car number of the player
        self.m_readyStatus = defs.ReadyStatus(data[52]) # 0 = not ready, 1 = ready, 2 = spectating

class PacketLobbyInfoData(Packet):
    size = 1191
    formatString = 'HBBBBQfIBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10]) # Header Packet specific data
        self.m_numPlayers = data[10] # Number of players in the lobby data
        self.m_lobbyPlayers = [LobbyInfoData(data[i:i + 53]) for i in range(11, 1177, 53)] 

class CarDamageData(Packet):
    size = 39
    formatString = 'ffffBBBBBBBBBBBBBBBBBBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_tyresWearPercent = WheelArray(data[0:4]) # Tyre wear (percentage)
        self.m_tyresDamagePercent = WheelArray(data[4:8]) # Tyre damage (percentage)
        self.m_brakesDamagePercent = WheelArray(data[8:12]) # Brakes damage (percentage)
        self.m_frontLeftWingDamagePercent = data[12] # Front left wing damage (percentage)
        self.m_frontRightWingDamagePercent = data[13] # Front right wing damage (percentage)
        self.m_rearWingDamagePercent = data[14] # Rear wing damage (percentage)
        self.m_floorDamagePercent = data[15] # Floor damage (percentage)
        self.m_diffuserDamagePercent = data[16] # Diffuser damage (percentage)
        self.m_sidepodDamagePercent = data[17] # Sidepod damage (percentage)
        self.m_drsFault = defs.DrsFault(data[18]) # Indicator for DRS fault, 0 = OK, 1 = fault
        self.m_gearBoxDamagePercent = data[19] # Gear box damage (percentage)
        self.m_engineDamagePercent = data[20] # Engine damage (percentage)
        self.m_engineMGUHWearPercent = data[21] # Engine wear MGU-H (percentage)
        self.m_engineESWearPercent = data[22] # Engine wear ES (percentage)
        self.m_engineCEWearPercent = data[23] # Engine wear CE (percentage)
        self.m_engineICEWearPercent = data[24] # Engine wear ICE (percentage)
        self.m_engineMGUKWearPercent = data[25] # Engine wear MGU-K (percentage)
        self.m_engineTCWearPercent = data[26] # Engine wear TC (percentage)

class PacketCarDamageData(Packet):
    size = 882
    formatString = 'HBBBBQfIBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBBffffBBBBBBBBBBBBBBBBBBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10]) # Header
        self.m_carDamageData = [CarDamageData(data[i:i + 27]) for i in range(10, 604, 27)] 

class LapHistoryData(Packet):
    size = 11
    formatString = 'IHHHB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_lapTimeInMS = data[0] # Lap time in milliseconds
        self.m_sector1TimeInMS = data[1] # Sector 1 time in milliseconds
        self.m_sector2TimeInMS = data[2] # Sector 2 time in milliseconds
        self.m_sector3TimeInMS = data[3] # Sector 3 time in milliseconds
        bitsList = utils.bitsToList(data[4], 4, descending=False)
        self.m_lapValid = bool(bitsList[0])
        self.m_validSectorsList = [bool(bit) for bit in bitsList[1:4]] # [True, False, False] means first sector valid, second sector invalid, third sector invalid (due to second sector invalid)

class TyreStintHistoryData(Packet):
    size = 3
    formatString = 'BBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_endLap = data[0] # Lap the tyre usage ends on (255 of current tyre)
        self.m_tyreActualCompound = defs.ActualTyreCompound(data[1]) # Actual tyres used by this driver
        self.m_tyreVisualCompound = defs.VisualTyreCompound(data[2]) # Visual tyres used by this driver

class PacketSessionHistoryData(Packet):
    size = 1155
    formatString = 'HBBBBQfIBBBBBBBBBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBIHHHBBBBBBBBBBBBBBBBBBBBBBBBB'

    def __init__(self, data, bytes=False):
        data = super().__init__(data, bytes)
        self.m_header = PacketHeader(data[0:10]) # Header
        self.m_carIdx = data[10] # Index of the car this lap data relates to
        self.m_numLapsIncCurrent = data[11] # Num laps in the data (including current partial lap)
        self.m_numTyreStints = data[12] # Number of tyre stints in the data
        self.m_bestLapTimeLapNum = data[13] # Lap the best lap time was achieved on
        self.m_bestSector1LapNum = data[14] # Lap the best Sector 1 time was achieved on
        self.m_bestSector2LapNum = data[15] # Lap the best Sector 2 time was achieved on
        self.m_bestSector3LapNum = data[16] # Lap the best Sector 3 time was achieved on
        self.m_lapHistoryData = [LapHistoryData(data[i:i + 5]) for i in range(17, 517, 5)] # 100 laps of data max
        self.m_tyreStintsHistoryData = [TyreStintHistoryData(data[i:i + 3]) for i in range(517, 541, 3)] 

packetIDs = {
    defs.PacketIDs.MOTION: PacketMotionData,
    defs.PacketIDs.SESSION: PacketSessionData,
    defs.PacketIDs.LAP_DATA: PacketLapData,
    #defs.PacketIDs.EVENT: PacketEventData,
    defs.PacketIDs.PARTICIPANTS: PacketParticipantsData,
    defs.PacketIDs.CAR_SETUPS: PacketCarSetupData,
    defs.PacketIDs.CAR_TELEMETRY: PacketCarTelemetryData,
    defs.PacketIDs.CAR_STATUS: PacketCarStatusData,
    defs.PacketIDs.FINAL_CLASSIFICATION: PacketFinalClassificationData,
    defs.PacketIDs.LOBBY_INFO: PacketLobbyInfoData,
    defs.PacketIDs.CAR_DAMAGE: PacketCarDamageData,
    defs.PacketIDs.SESSION_HISTORY: PacketSessionHistoryData
}

eventPackets = {
    defs.EventStringCodes.FASTEST_LAP: PacketFastestLap,
    defs.EventStringCodes.RETIREMENT: PacketRetirement,
    defs.EventStringCodes.TEAM_MATE_IN_PITS: PacketTeamMateInPits,
    defs.EventStringCodes.RACE_WINNER: PacketRaceWinner,
    defs.EventStringCodes.PENALTY_ISSUED: PacketPenalty,
    defs.EventStringCodes.SPEED_TRAP_TRIGGERED: PacketSpeedTrap,
    defs.EventStringCodes.START_LIGHTS: PacketStartLights,
    defs.EventStringCodes.DRIVE_THROUGH_SERVED: PacketDriveThroughPenaltyServed,
    defs.EventStringCodes.STOP_GO_SERVED: PacketStopGoPenaltyServed,
    defs.EventStringCodes.FLASHBACK: PacketFlashback,
    defs.EventStringCodes.BUTTON_STATUS: PacketButtons
}