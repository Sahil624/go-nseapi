package models

import "gorm.io/gorm"

type Quote struct {
	gorm.Model
	Symbol         Scrip
	SymbolID       int     `json:"symbol_id" gorm:"unique"`
	LastTradePrice float64 `json:"last_trade_price"`
	Close          float64 `json:"close"`
	Open           float64 `json:"open"`
	High           float64 `json:"high"`
	Low            float64 `json:"low"`
}
