# Issue 002: StateDef 111の無限ループ

## ステータス

open

## 症状

StateDef `111`が無限ループする。WinMUGENは`over 2500 loops`を検出し、強制終了する。

## 原因

未調査。

## 修正

未着手。

## 確認事項

- StateDef `111`へ遷移する条件
- StateDef `111`内の遷移先と復帰条件
- 同一フレーム内でStateDef `111`へ再遷移する経路
