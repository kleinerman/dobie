int_CON  = 0x01 #Connnect
int_RCON = 0x02 #Response to Connect
int_EVT  = 0x03 #Event
int_REVT = 0x04 #Response to Event
int_EVS  = 0x05 #Many Events
int_REVS = 0x06 #Response to Many Events
int_CUD  = 0x07 #Create Update Delete
int_RCUD = 0x08 #Response to Create Update Delete
int_RRC  = 0x09 #Request Resend Curds
int_RRP  = 0x0A #Request Re Provision the entire controller
int_RRRE = 0x0B #Response to Request Resend Crud or Reprovision
int_KAL  = 0x0C #Keep Alive
int_RPO  = 0x0D #Request Power Off
int_END  = 0x1F #End


CON  = bytes([int_CON])
RCON = bytes([int_RCON])
EVT  = bytes([int_EVT])
REVT = bytes([int_REVT])
EVS  = bytes([int_EVS])
REVS = bytes([int_REVS])
CUD  = bytes([int_CUD])
RCUD = bytes([int_RCUD])
RRC  = bytes([int_RRC])
RRP  = bytes([int_RRP])
RRRE = bytes([int_RRRE])
KAL  = bytes([int_KAL])
RPO  = bytes([int_RPO])
END  = bytes([int_END])

