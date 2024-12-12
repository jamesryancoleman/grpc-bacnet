# create the device
DEVICE_ID=$(mkd -n home_iaq -t brick:IAQ_Sensor_Equipment -l SouthSt)
add -driver 2 $DEVICE_ID
# add -driver.name bacnet $DEVICE_ID
echo "created dev:$DEVICE_ID"

DEVICE_IP="192.168.1.177" # must be provided by user
BACNET_ID="9"

# add its points 
PT1=$(mkd -p -n pm2.5 -t brick:PM2.5_Sensor $DEVICE_ID)
PT2=$(mkd -p -n pm10 -t brick:PM10_Sensor $DEVICE_ID)
PT3=$(mkd -p -n tvoc -t brick:TVOC_Sensor $DEVICE_ID)
PT4=$(mkd -p -n temp -t brick:Air_Temperature_Sensor $DEVICE_ID)
PT5=$(mkd -p -n humid -t brick:Humidity_Sensor $DEVICE_ID)
PT6=$(mkd -p -n co2 -t brick:CO2_Sensor $DEVICE_ID)

# add xrefs
add -xref bos://$DEVICE_IP/$BACNET_ID/analog-input,1/present-value $PT1
add -xref bos://$DEVICE_IP/$BACNET_ID/analog-input,2/present-value $PT2
add -xref bos://$DEVICE_IP/$BACNET_ID/analog-input,3/present-value $PT3
add -xref bos://$DEVICE_IP/$BACNET_ID/analog-input,4/present-value $PT4
add -xref bos://$DEVICE_IP/$BACNET_ID/analog-input,5/present-value $PT5
add -xref bos://$DEVICE_IP/$BACNET_ID/analog-input,6/present-value $PT6

echo "created dev:$DEVICE_ID/pts/$PT1"
echo "created dev:$DEVICE_ID/pts/$PT2"
echo "created dev:$DEVICE_ID/pts/$PT3"
echo "created dev:$DEVICE_ID/pts/$PT4"
echo "created dev:$DEVICE_ID/pts/$PT5"
echo "created dev:$DEVICE_ID/pts/$PT6"