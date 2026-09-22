# Helper参照と実行順

## 兄弟Helperの参照

Helperから同じRootに属する別のHelperを参照する場合は、`helper(ID),...`を使用する。Rootを起点とする別のHelper参照構文は存在しない。

## Helperの実行順

Helperの実行順は存在順に依存する。先に存在するHelperの挙動が完了した後に、後続のHelperが同tickで実行される。後続Helperから先行Helperの値を参照する場合は、先行Helperが同tickに更新した値となる。
