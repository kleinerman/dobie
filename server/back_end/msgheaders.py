int_CON  = 0x01
int_RCON = 0x02
int_EVT  = 0x03
int_REVT = 0x04
int_EVS  = 0x05
int_REVS = 0x06
int_CUD  = 0x07
int_RCUD = 0x08
int_RRC  = 0x09 #Request Resend Curds
int_RRP  = 0x0A #Request Re Provision the entire controller
int_RRRE = 0x0B #Response to Request Resend Crud or Reprovision
int_END  = 0x1F


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
END  = bytes([int_END])
