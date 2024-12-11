# create the device
DEVICE_ID=$(mkd -n bacpi -t brick:Equipment -l SouthSt)
# add -driver.name bacnet $DEVICE_ID # use only if driver doesn't exist
add -driver 2 $DEVICE_ID
echo "created dev:$DEVICE_ID"

DEVICE_IP="192.168.1.197" # must be provided by user
BACNET_ID="123"

# add its points 
PT1=$(mkd -p -n temp -t brick:Air_Temperature_Sensor $DEVICE_ID)

# add xrefs
add -xref bos://$DEVICE_IP/$BACNET_ID/analog-value,1/present-value $PT1

echo "created dev:$DEVICE_ID/pts/$PT1"

# BACnet point list:
#     device,9:
#         description: Smart Air Quality Monitor
#     analog-input,0:
#         description: Sec
#         present-value: 7231141.0
#         units: seconds
#     analog-input,1:
#         description: PM2.5
#         present-value: 43.0
#         units: micrograms-per-cubic-meter
#     analog-input,2:
#         description: PM10
#         present-value: 45.0
#         units: micrograms-per-cubic-meter
#     analog-input,3:
#         description: TVOC
#         present-value: 243.0
#         units: parts-per-billion
#     analog-input,4:
#         description: Temperature
#         present-value: 23.343000411987305
#         units: degrees-celsius
#     analog-input,5:
#         description: Humidity
#         present-value: 30.138999938964844
#         units: percent
#     analog-input,6:
#         description: CO2
#         present-value: 558.0
#         units: parts-per-million
#     analog-input,8:
#         description: KM200 Module Lifespan
#         present-value: 58.0
#         units: percent
#     analog-input,9:
#         description: KM203 Module Lifespan
#         present-value: 24.0
#         units: percent