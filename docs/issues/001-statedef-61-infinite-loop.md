# Issue 001: StateDef 61の無限ループ

## ステータス

open

## 症状

StateDef `61`が無限ループする。WinMUGENは`over 2500 loops`を検出し、強制終了する。

## 原因

未調査。

## 修正

未着手。

## 確認事項

- StateDef `61`へ遷移する条件
- StateDef `61`内の遷移先と復帰条件
- 同一フレーム内でStateDef `61`へ再遷移する経路
