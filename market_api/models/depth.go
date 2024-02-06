package models

import (
	"github.com/lib/pq"
	"gorm.io/gorm"
)

type Depth struct {
	gorm.Model

	Symbol    Scrip
	SymbolID  int             `json:"symbol_id" gorm:"unique"`
	AskPrices pq.Float64Array `json:"ask_price" gorm:"type:float[]"`
	AskQty    pq.Int64Array   `json:"ask_qty" gorm:"type:integer[]"`
	BidPrices pq.Float64Array `json:"bid_prices" gorm:"type:float[]"`
	BidQty    pq.Int64Array   `json:"bid_qty" gorm:"type:integer[]"`
}
