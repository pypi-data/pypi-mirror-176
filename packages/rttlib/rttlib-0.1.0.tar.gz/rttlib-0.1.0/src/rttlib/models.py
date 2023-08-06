from pydantic import BaseModel, Field, validator
from enum     import Enum

class Display(Enum):
    """
    Represents states of a station with regards to a service
    CALL - service calls at this station
    PASS - service passes this station
    ORGN - service originated at this station
    DEST - service is destined for this station
    STRT - service begins at this station (non-origin, origin is CANC)
    TERM - service ends at this station (non-destination, destination is CANC)
    CANC - service was scheduled to call but was cancelled
    CANP - service was scheduled to pass but was cancelled
    """
    CALL = "CALL"
    PASS = "PASS"
    ORGN = "ORIGIN"
    DEST = "DESTINATION"
    STRT = "STARTS"
    TERM = "TERMINATES"
    CANC = "CANCELLED_CALL"
    CANP = "CANCELLED_PASS"

class ServiceLoc(Enum):
    """
    Represents states of a service with regards to a station
    APPS - approaching station
    ARRV - approaching platform (arriving)
    ATPL - at platform (standing)
    DPRP - preparing to depart
    DRDY - ready to depart
    """
    APPS = "APPR_STAT"
    ARRV = "APPR_PLAT"
    STND = "AT_PLAT"
    DPRP = "DEP_PREP"
    DRDY = "DEP_READY"

class StationLocation(BaseModel):
    """
    Represents location information about a station
    name    - name of the station
    crs     - CRS of the station
    tiploc  - TIPLOC of the station
    country - country of the station
    system  - rail system of the station
    """
    name: str
    crs: str
    tiploc: str
    country: str
    system: str

class Pair(BaseModel):
    """
    Represents an activity (usually an origin/destination)
    tiploc      - TIPLOC of the station
    name        - name of the station
    workingTime - working time for the activity
    publicTime  - public time for the activity
    """
    tiploc: str
    name: str = Field(alias="description")
    workingTime: str
    publicTime: str

class StationServiceDetail(BaseModel):
    """
    Represents information about a service which calls at a station
    realtimeActivated        - true if service is activated for realtime information
    tiploc                   - TIPLOC code of the station
    crs                      - CRS of the station
    name                     - name of the station
    bookedArrival            - public timetable arrival of the service
    bookedDeparture          - public timetable departure of the service
    origin                   - pair object representing the origin of the service
    destination              - pair object representing the destination of the service
    isCall                   - true if the service calls here
    isPublicCall             - true if the service publicly calls here
    realtimeArrival          - expected/actual arrival time
    realtimeArrivalActual    - true if the arrival time is actual
    realtimeDeparture        - expected/actual departure time
    realtimeDepartureArrival - true if the departure time is actual
    platform                 - expected platform the service will use
    platformConfirmed        - true if the platform is confirmed
    platformChanged          - true if the platform has been changed
    displayAs                - represents how the service should be displayed
    """
    realtimeActivated: bool | None
    tiploc: str
    crs: str
    name: str = Field(alias="description")
    bookedArrival: str = Field(alias="gbttBookedArrival")
    bookedDeparture: str = Field(alias="gbttBookedDeparture")
    origin: list[Pair]
    destination: list[Pair]
    isCall: bool
    isPublicCall: bool
    realtimeArrival: str | None
    realtimeArrivalActual: bool | None
    realtimeDeparture: str | None
    realtimeDepartureActual: bool | None
    platform: str | None
    platformConfirmed: bool | None
    platformChanged: bool | None
    displayAs: Display

class StationService(BaseModel):
    """
    Represents a service which calls at a station
    ld              - StationServiceDetail attached to this service
    serviceUid      - unique identifier of this service
    runDate         - date this service ran on
    trainIdentity   - identity of this service
    runningIdentity - running identity of this service
    atocCode        - two-letter identifier of service operator
    atocName        - name of service operator
    serviceType     - type of service (bus, ship or train)
    isPassenger     - true if the service is a passenger service
    """
    ld: StationServiceDetail = Field(alias="locationDetail")
    serviceUid: str
    runDate: str
    trainIdentity: str | None
    runningIdentity: str | None
    atocCode: str
    atocName: str
    serviceType: str
    isPassenger: bool

class StationSearchRes(BaseModel):
    """
    Repreents the result of searching for a station
    location - StationLocation representing location information
    services - list of StationService representing scheduled calls
    """
    location: StationLocation
    filter: None # seems to always be null...
    services: list[StationService]

class Stop(BaseModel):
    """
    Represents a station that a service calls at/passes through
    realtimeActivated        - true if service is activated for realtime information
    tiploc                   - TIPLOC code of the station
    crs                      - CRS of the station
    name                     - name of the station
    bookedArrival            - public timetable arrival of the service
    bookedDeparture          - public timetable departure of the service
    isCall                   - true if the service calls here
    isPublicCall             - true if the service publicly calls here
    realtimeArrival          - expected/actual arrival time
    realtimeArrivalActual    - true if the arrival time is actual
    realtimeDeparture        - expected/actual departure time
    realtimeDepartureArrival - true if the departure time is actual
    platform                 - expected platform the service will use
    platformConfirmed        - true if the platform is confirmed
    platformChanged          - true if the platform has been changed
    displayAs                - represents how the service should be displayed
    serviceLocation          - represents the service's location relative to the station
    """
    tiploc: str
    crs: str
    description: str
    bookedArrival: str | None = Field(alias="gbttBookedArrival")
    bookedDeparture: str | None = Field(alias="gbttBookedDeparture")
    isCall: bool
    isPublicCall: bool
    realtimeArrival: str | None
    realtimeArrivalActual: bool | None
    realtimeDeparture: str | None
    realtimeDepartureActual: bool | None
    platform: str | None
    platformConfirmed: bool | None
    platformChanged: bool | None
    displayAs: Display
    serviceLocation: ServiceLoc | None

class ServiceSearchRes(BaseModel):
    """
    Represents the result of searching for a service
    serviceUid           - unique identifier of this service
    runDate              - date this service ran on
    serviceType          - type of service (bus, ship or train)
    trainIdentity        - identity of this service
    runningIdentity      - running identity of this service
    powerType            - how the train is powered
    atocCode             - two-letter identifier of service operator
    atocName             - name of service operator
    performanceMonitored - true if service is monitored for performance
    origin               - pair object representing the origin of the service
    destination          - pair object representing the destination of the service
    locations            - list of stop objects representing the stations this service calls at
    realtimeActivated    - true if service is activated for realtime information
    """
    serviceUid: str
    runDate: str
    serviceType: str
    trainIdentity: str | None
    runningIdentity: str | None
    powerType: str | None
    atocCode: str
    atocName: str
    performanceMonitored: bool
    origin: list[Pair]
    destination: list[Pair]
    locations: list[Stop]
    realtimeActivated: bool | None
