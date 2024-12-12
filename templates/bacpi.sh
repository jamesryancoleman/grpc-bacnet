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
