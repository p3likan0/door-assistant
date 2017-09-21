# Door-assistant

### App for mongoose os.

### RFID and web controlled door.

### How to bootsrap:
```
mos build --arch esp8266

mos flash && mos console 
```
### How to open door: 
```
 mos call Door.Open

```
### How to disable door: 
```
mos config-set door.enable="false"
```
