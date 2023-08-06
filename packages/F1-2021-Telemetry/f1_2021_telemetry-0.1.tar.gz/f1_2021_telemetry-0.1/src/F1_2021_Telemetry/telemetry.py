import socket
import struct
from threading import Thread
from F1_2021_Telemetry import defs, packets, utils

IP = "127.0.0.1"
PORT = 20777

# Use UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind((IP, PORT))

simpleEvents = {
    defs.EventStringCodes.SESSION_STARTED,
    defs.EventStringCodes.SESSION_ENDED,
    defs.EventStringCodes.DRS_ENABLED,
    defs.EventStringCodes.DRS_DISABLED,
    defs.EventStringCodes.CHEQUERED_FLAG,
    defs.EventStringCodes.LIGHTS_OUT
}

class Event():
    FastestLap = [] # type: list[packets.PacketFastestLap]
    Retirement= [] # type: list[packets.PacketRetirement]
    TeamMateInPits= [] # type: list[packets.PacketTeamMateInPits]
    RaceWinner= [] # type: list[packets.PacketRaceWinner]
    Penalty= [] # type: list[packets.PacketPenalty]
    SpeedTrap= [] # type: list[packets.PacketSpeedTrap]
    StartLights= [] # type: list[packets.PacketStartLights]
    DriveThroughPenaltyServed= [] # type: list[packets.PacketDriveThroughPenaltyServed]
    StopGoPenaltyServed= [] # type: list[packets.PacketStopGoPenaltyServed]
    Flashback= [] # type: list[packets.PacketFlashback]
    Buttons= [] # type: list[packets.PacketButtons]

class State():
    def __init__(self):
        self.Motion = packets.PacketMotionData(None)
        self.Session = packets.PacketSessionData(None)
        self.LapData = packets.PacketLapData(None)
        self.Participants = packets.PacketParticipantsData(None)
        self.CarSetups = packets.PacketCarSetupData(None)
        self.CarTelemetry = packets.PacketCarTelemetryData(None)
        self.CarStatus = packets.PacketCarStatusData(None)
        self.FinalClassification = packets.PacketFinalClassificationData(None)
        self.LobbyInfo = packets.PacketLobbyInfoData(None)
        self.CarDamage = packets.PacketCarDamageData(None)
        self.SessionHistory = [packets.PacketSessionHistoryData(None) for _ in range(22)]
        self.SimpleEvents = [] # type: list[packets.PacketSimpleEvent]
        self.Events = Event()

    def update(self, data):
        packetType = peepType(data)

        if packetType is defs.PacketIDs.MOTION:
            self.Motion = packets.packetIDs[packetType](data, bytes=True)
            return

        elif packetType is defs.PacketIDs.SESSION:
            self.Session = packets.packetIDs[packetType](data, bytes=True)
            return

        elif packetType is defs.PacketIDs.LAP_DATA:
            self.LapData = packets.packetIDs[packetType](data, bytes=True)
            return

        elif packetType is defs.PacketIDs.PARTICIPANTS:
            self.Participants = packets.packetIDs[packetType](data, bytes=True)
            return

        elif packetType is defs.PacketIDs.CAR_SETUPS:
            self.CarSetups = packets.packetIDs[packetType](data, bytes=True)
            return

        elif packetType is defs.PacketIDs.CAR_TELEMETRY:
            self.CarTelemetry = packets.packetIDs[packetType](data, bytes=True)
            return

        elif packetType is defs.PacketIDs.CAR_STATUS:
            self.CarStatus = packets.packetIDs[packetType](data, bytes=True)
            return

        elif packetType is defs.PacketIDs.FINAL_CLASSIFICATION: 
            self.FinalClassification = packets.packetIDs[packetType](data, bytes=True)
            return

        elif packetType is defs.PacketIDs.LOBBY_INFO:
            self.LobbyInfo = packets.packetIDs[packetType](data, bytes=True)
            return

        elif packetType is defs.PacketIDs.CAR_DAMAGE:
            self.CarDamage = packets.packetIDs[packetType](data, bytes=True)
            return

        elif packetType is defs.PacketIDs.SESSION_HISTORY:
            packet = packets.PacketSessionHistoryData(data, bytes=True)
            self.SessionHistory[packet.m_carIdx] = packet
            return
        
        eventType = peepEvent(data)


        if eventType in simpleEvents:
            self.SimpleEvents.append(packets.PacketSimpleEvent(data, bytes=True))
            return
        
        detailEvents = {
            defs.EventStringCodes.FASTEST_LAP: self.Events.FastestLap,
            defs.EventStringCodes.RETIREMENT: self.Events.Retirement,
            defs.EventStringCodes.TEAM_MATE_IN_PITS: self.Events.TeamMateInPits,
            defs.EventStringCodes.RACE_WINNER: self.Events.RaceWinner,
            defs.EventStringCodes.PENALTY_ISSUED: self.Events.Penalty,
            defs.EventStringCodes.SPEED_TRAP_TRIGGERED: self.Events.SpeedTrap,
            defs.EventStringCodes.START_LIGHTS: self.Events.StartLights,
            defs.EventStringCodes.DRIVE_THROUGH_SERVED: self.Events.DriveThroughPenaltyServed,
            defs.EventStringCodes.STOP_GO_SERVED: self.Events.StopGoPenaltyServed,
            defs.EventStringCodes.FLASHBACK: self.Events.Flashback,
            defs.EventStringCodes.BUTTON_STATUS: self.Events.Buttons
        }

        packet = packets.eventPackets[eventType](data, bytes=True)
        detailEvents[eventType].append(packet)

        if len(self.Events.Buttons) > 100:
            self.Events.Buttons.pop(0)

currentState = State()

def peepType(packetBinary):
    # Return the type of a packet
    packetID = struct.unpack("<B", packetBinary[5:6])[0]
    return defs.PacketIDs(packetID)

def peepEvent(packetBinary):
    # Return the event type of an event packet
    stringCode = utils.convToString(struct.unpack("<BBBB", packetBinary[24:28]))
    return defs.EventStringCodes(stringCode)

def stateUpdater():
    while True:
        try:
            data = sock.recvfrom(1464)[0] # max possible size is 1464 bytes
        except socket.error:
            pass
        else:
            currentState.update(data)
            
stateUpdaterThread = Thread(target=stateUpdater, daemon=True)
stateUpdaterThread.start()
