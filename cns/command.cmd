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

[Command]
name="x"
command=x
time=1

[Command]
name="y"
command=y
time=1

[Command]
name="z"
command=z
time=1

[Command]
name="a"
command=a
time=1

[Command]
name="b"
command=b
time=1

[Command]
name="c"
command=c
time=1

[Command]
name="s"
command=s
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

;; 入力ビット変換

[state ]
type=varset
trigger1=1
var(2)=var(2)&-2147483648

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="holdfwd"
var(2)=var(2)|1

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="holdback"
var(2)=var(2)|2

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="holdup"
var(2)=var(2)|4

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="holddown"
var(2)=var(2)|8

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="x"
var(2)=var(2)|16

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="y"
var(2)=var(2)|32

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="z"
var(2)=var(2)|64

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="a"
var(2)=var(2)|128

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="b"
var(2)=var(2)|256

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="c"
var(2)=var(2)|512

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="s"
var(2)=var(2)|1024

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="recovery"
var(2)=var(2)|2048

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="FF"
var(2)=var(2)|4096

[state ]
type=varset
trigger1=(var(2)&-2147483648)=0
trigger1=command="BB"
var(2)=var(2)|8192

;; 入力ビットによる状態遷移

;; 異形回避

[state ]
type=changestate
value=300
triggerall=(var(2)&2048)!=0
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

;; 前方高速ダッシュ

[state ]
type=changestate
value=110
triggerall=(var(2)&4096)!=0
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

;; 後方高速ダッシュ

[state ]
type=changestate
value=111
triggerall=(var(2)&8192)!=0
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

;; 前方近距離ワープ

[state ]
type=changestate
value=100
triggerall=stateno=0
triggerall=pos y>=0
triggerall=(numhelper(509000)=0)||(helper(509000),var(7)=0)
triggerall=(var(2)&512)!=0
triggerall=((var(2)&1)!=0)||(((var(2)&1)=0)&&((var(2)&2)=0)&&(vel x>0))
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

[state ]
type=changestate
value=100
triggerall=stateno=20
triggerall=(numhelper(509000)=0)||(helper(509000),var(7)=0)
triggerall=(var(2)&512)!=0
triggerall=((var(2)&1)!=0)||(((var(2)&1)=0)&&((var(2)&2)=0)&&(vel x>0))
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

[state ]
type=changestate
value=100
triggerall=stateno=60
triggerall=(numhelper(509000)=0)||(helper(509000),var(7)=0)
triggerall=(var(2)&512)!=0
triggerall=((var(2)&1)!=0)||(((var(2)&1)=0)&&((var(2)&2)=0)&&(vel x>0))
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

[state ]
type=changestate
value=100
triggerall=stateno=61
triggerall=(numhelper(509000)=0)||(helper(509000),var(7)=0)
triggerall=(var(2)&512)!=0
triggerall=((var(2)&1)!=0)||(((var(2)&1)=0)&&((var(2)&2)=0)&&(vel x>0))
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

[state ]
type=changestate
value=100
triggerall=stateno=0
triggerall=pos y<0
triggerall=(numhelper(509000)=0)||(helper(509000),var(7)=0)
triggerall=(var(2)&512)!=0
triggerall=((var(2)&1)!=0)||(((var(2)&1)=0)&&((var(2)&2)=0)&&(vel x>0))
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

;; 後方近距離ワープ

[state ]
type=changestate
value=105
triggerall=stateno=0
triggerall=pos y>=0
triggerall=(numhelper(509000)=0)||(helper(509000),var(7)=0)
triggerall=(var(2)&512)!=0
triggerall=((var(2)&2)!=0)||(((var(2)&1)=0)&&((var(2)&2)=0)&&(vel x<0))
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

[state ]
type=changestate
value=105
triggerall=stateno=20
triggerall=(numhelper(509000)=0)||(helper(509000),var(7)=0)
triggerall=(var(2)&512)!=0
triggerall=((var(2)&2)!=0)||(((var(2)&1)=0)&&((var(2)&2)=0)&&(vel x<0))
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

[state ]
type=changestate
value=105
triggerall=stateno=60
triggerall=(numhelper(509000)=0)||(helper(509000),var(7)=0)
triggerall=(var(2)&512)!=0
triggerall=((var(2)&2)!=0)||(((var(2)&1)=0)&&((var(2)&2)=0)&&(vel x<0))
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

[state ]
type=changestate
value=105
triggerall=stateno=61
triggerall=(numhelper(509000)=0)||(helper(509000),var(7)=0)
triggerall=(var(2)&512)!=0
triggerall=((var(2)&2)!=0)||(((var(2)&1)=0)&&((var(2)&2)=0)&&(vel x<0))
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

[state ]
type=changestate
value=105
triggerall=stateno=0
triggerall=pos y<0
triggerall=(numhelper(509000)=0)||(helper(509000),var(7)=0)
triggerall=(var(2)&512)!=0
triggerall=((var(2)&2)!=0)||(((var(2)&1)=0)&&((var(2)&2)=0)&&(vel x<0))
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

;; 画面横断突進

[state ]
type=changestate
value=1200
triggerall=(var(2)&16)!=0
triggerall=(var(2)&1)=0
triggerall=(var(2)&2)=0
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

;; オーラバウンド保持確認

[state ]
type=changestate
value=4002
triggerall=(var(2)&32)!=0
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

;; オーラバウンド倍率確認

[state ]
type=changestate
value=4003
triggerall=(var(2)&64)!=0
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

;; 汎用両手光弾発出

[state ]
type=changestate
value=1000
triggerall=(var(2)&128)!=0
triggerall=!numhelper(509000)
triggerall=!numhelper(506000)
triggerall=!numhelper(506001)
triggerall=!numhelper(506002)
triggerall=!numhelper(506003)
triggerall=!numhelper(506004)
triggerall=!numhelper(506005)
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

;; 汎用片手光弾発出

[state ]
type=changestate
value=1100
triggerall=(numhelper(509000)=0)||(helper(509000),var(7)=0)
triggerall=(var(2)&256)!=0
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

;; 空中歩行

[state ]
type=changestate
value=60
triggerall=pos y<0
triggerall=stateno!=60
triggerall=stateno!=110
triggerall=stateno!=111
triggerall=(var(2)&1)!=0
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl

[state ]
type=changestate
value=61
triggerall=pos y<0
triggerall=stateno!=61
triggerall=stateno!=110
triggerall=stateno!=111
triggerall=(var(2)&2)!=0
trigger1=(var(2)&-2147483648)!=0
trigger2=(var(2)&-2147483648)=0
trigger2=ctrl
