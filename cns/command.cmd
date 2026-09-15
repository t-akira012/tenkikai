;-------------------------------------------------
[Remap]
x=x
y=y
z=z
a=a
b=b
c=c
s=s

;-------------------------------------------------
[Defaults]
command.time=15

command.buffer.time=1

;-------------------------------------------------
[Command]
name="FF"
command=F,F
time=10

[Command]
name="BB"
command=B,B
time=10

;-------------------------------------------------
[Command]
name="recovery"
command=x+y
time=1

;-------------------------------------------------
[Command]
name="holdfwd"
command=/$F
time=1

[Command]
name="holdback"
command=/$B
time=1

[Command]
name="holdup"
command=/$U
time=1

[Command]
name="holddown"
command=/$D
time=1

;-------------------------------------------------

[statedef -1]

;-------------------------------------------------

[state ]
type=changestate
value=100
trigger1=command="FF"
trigger1=statetype=S
trigger1=ctrl

;-------------------------------------------------

[state ]
type=changestate
value=105
trigger1=command="BB"
trigger1=statetype=S
trigger1=ctrl
