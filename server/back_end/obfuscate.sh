#Is not possible to obfuscate largest files for license reasons
#for this reason database.py and crud.py were excluded.
#"config.py" were excluded to keep it understandable.
#"main.py" and "purgeevents.py" should have bootstrap code
#since they are executed independently.
#"run time" is only generated when obfuscating "main.py"

pyarmor obfuscate  --exact main.py
pyarmor obfuscate  --no-runtime --exact purgeevents.py
pyarmor obfuscate  --no-runtime --no-bootstrap --exact crudresndr.py
pyarmor obfuscate  --no-runtime --no-bootstrap --exact ctrllermsger.py
pyarmor obfuscate  --no-runtime --no-bootstrap --exact lifechecker.py
pyarmor obfuscate  --no-runtime --no-bootstrap --exact msgheaders.py
pyarmor obfuscate  --no-runtime --no-bootstrap --exact msgreceiver.py
pyarmor obfuscate  --no-runtime --no-bootstrap --exact network.py
pyarmor obfuscate  --no-runtime --no-bootstrap --exact rtevent.py
