# ADR 033: Helper Armor configと連続ダメージ減衰

## 状態

採用

## 背景

従来のHelper Armorは、`GetHitVar(damage)`をそのまま本体の削り値と無敵時間に使用し、最大Lifeの`1/4`以下で削り値を半減し、保留ダメージがないtickには本体Lifeを`1`回復していた。この構造では回復量、Damage減衰、低ライフ耐性、無敵時間を利用者が独立して調整できず、低ライフ境界で削り値が不連続に変化していた。

また、これらの設定値はすべて`the_controller`で同じ期間維持されるため、個別の通常変数へ分散させず、単一のconfigとして管理する必要がある。

## 決定

`the_controller`の`var(12)`をHelper Armor configビットフィールドとする。自動回復量をbit 0〜6、ダメージ減衰率configをbit 7〜11、被弾後無敵時間をbit 12〜18、極大Damage閾値configをbit 20〜31へ割り当てる。bit 19は未使用とする。

利用者が設定値を変更する場所は、特例としてRootとHelperの双方で実行されるStateDef `-2`先頭のAI設定欄へ置く。各Controllerは`IsHelper(99004)`で`the_controller`だけを対象とする。最初のControllerで`var(12)`を`0`へ初期化し、自動回復量、ダメージ減衰率、被弾後無敵時間、極大Damage閾値をそれぞれ独立したControllerからビットORで設定する。

通常Damageは、`GetHitVar(damage)`へダメージ減衰率configと、現在Life比率`r`から求める`2r-r²`を乗算して解決する。ダメージ減衰率configは`0`〜`25`とし、1段階を元Damageの4%とする。特定のLife以下で切り替わる低ライフ閾値と追加倍率は使用しない。WinMUGENの式パーサーへ長大な単一式を渡さないよう、Life比率と減衰後Damageを`fvar(20)`、`fvar(21)`へ順番に計算する。

極大Damage閾値configは`0`〜`32`とし、1段階を100Damageとする。configが正で、元Damageが閾値以上の場合はダメージ減衰率とLife補正を適用しない。configが`0`の場合は極大Damage判定を無効化する。

被弾後無敵時間は元Damageから算出せず、configの固定tickを登録する。自動回復量は`0`〜`127/tick`とし、`0`では本体を回復しない。

`var(11)`は解決済み保留ダメージと無敵残り時間を保持する実行状態として維持し、毎処理周期に再設定されるconfigとは混在させない。StateDef `-2`はHelper ID `99004`に対するconfig設定に加え、Rootに対する保留ダメージの減算と、configが有効な場合の自動回復を実行する。

## 結果

利用者は`the_controller`の一箇所から回復量、ダメージ減衰率、固定無敵時間、極大Damage閾値を変更できる。通常DamageはLifeの減少に応じて連続的に小さくなり、Life閾値による不連続な補正はなくなる。一方、設定閾値以上の極大Damageは外殻の減衰を迂回し、本体へ元Damageを反映する。
