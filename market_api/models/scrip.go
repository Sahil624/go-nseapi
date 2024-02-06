package models

import (
	"go-nseapi/database"
	"go-nseapi/utils"
	"gorm.io/gorm"
)

// Scrip is a model for scrip listed on Market
type Scrip struct {
	gorm.Model
	Market        utils.MARKET `json:"market" gorm:"index:unique_IDX,unique"`
	Symbol        string       `json:"symbol"`
	CompanyName   string       `json:"company_name"`
	Series        string       `json:"series"`
	DateOfListing string       `json:"date_of_listing"`
	PaidUpValue   string       `json:"paid_up_value"`
	MarketLot     string       `json:"market_lot"`
	ISINNumber    string       `json:"isin_number" gorm:"index:unique_IDX,unique"`
	FaceValue     string       `json:"face_value"`
}

func GetSymbolByName(market utils.MARKET, symbolName string) (scrip *Scrip) {
	database.DB.Db.Where("market = ? AND symbol = ?", market, symbolName).First(&scrip)
	return
}
