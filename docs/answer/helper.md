# Helper参照と実行順

## 兄弟Helperの参照

Helperから同じRootに属する別のHelperを参照する場合は、`helper(ID),...`を使用する。Rootを起点とする別のHelper参照構文は存在しない。

## Helperの実行順

Helperの実行順は存在順に依存する。先に存在するHelperの挙動が完了した後に、後続のHelperが同tickで実行される。後続Helperから先行Helperの値を参照する場合は、先行Helperが同tickに更新した値となる。

## RootとHelperの実行順

tick内部ではRootが先に処理され、その後にHelperが処理される。Rootが常駐Helperの完成値を参照する場合、そのtickの後段でHelperが更新する値ではなく、前tickまでに完成していた値を使用する。

本体自由傾斜では`the_controller`が更新した角度を、次tickのRoot StateDef `-2`がAngleDrawへ適用する。この1tickの遅延は許容する。

## Helper消滅後のBind先

WinMUGENのHelperは配列構造で配置される。HelperへBindしたExplodのBind先は、Helperの個体を永続的に識別するものではなく、そのHelperが配置された配列indexに依存する。

親Helperが消滅しても、`removetime=-1`のExplodは消滅せずに残る。その後、別のHelperが同じ配列indexへ配置されると、残存ExplodのBind先が新しいHelperへ移る。地面付近へ生成されるHelperが同じindexを再利用した場合、残存Explodも地面へ移動する。
