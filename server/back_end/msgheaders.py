# The controller has a simlink to this file
# to avoid duplicating it

# Messages start with 0
# Responses start with 1

int_CON  = 0x01 # Connnect
int_RCON = 0x11 # Response to Connect
int_EVT  = 0x02 # Event
int_REVT = 0x12 # Response to Event
int_EVS  = 0x03 # Many Events
int_REVS = 0x13 # Response to Many Events
int_CUD  = 0x04 # Create Update Delete
int_RCUD = 0x14 # Response to Create Update Delete
int_RRC  = 0x05 # Request Resend Curds
int_RRRC = 0x15 # Response to Request Resend Crud
int_RRS  = 0x06 # Request Resync the entire controller
int_RRRS = 0x16 # Response to Request Resync
int_KAL  = 0x17 # Keep Alive
int_ROD  = 0x18 # Request Open Door
int_RPO  = 0x19 # Request Power Off
int_END  = 0xFF # End
int_RSPM = 0x10 # Response Mask (To check if server is sending a response)

CON  = bytes([int_CON])
RCON = bytes([int_RCON])
EVT  = bytes([int_EVT])
REVT = bytes([int_REVT])
EVS  = bytes([int_EVS])
REVS = bytes([int_REVS])
CUD  = bytes([int_CUD])
RCUD = bytes([int_RCUD])
RRC  = bytes([int_RRC])
RRRC = bytes([int_RRRC])
RRS  = bytes([int_RRS])
RRRS = bytes([int_RRRS])
KAL  = bytes([int_KAL])
ROD  = bytes([int_ROD])
RPO  = bytes([int_RPO])
END  = bytes([int_END])
