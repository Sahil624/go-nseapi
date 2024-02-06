package nseMarket

import (
	"encoding/json"
	"go-nseapi/database"
	"go-nseapi/models"
	"go-nseapi/utils"
	"gorm.io/gorm/clause"
	"log"
	"net/http/httputil"
	"net/url"
)

func RefreshMarketData(symbolName string) *models.Quote {
	uri, err := url.Parse(utils.NSE_EQUITY_QUOTE)
	if err != nil {
		log.Println("Error in parsing market data url", err)
	}
	q := uri.Query()
	q.Set("symbol", symbolName)
	uri.RawQuery = q.Encode()

	resp, err := nseHttpClient.Get(uri.String())
	if err != nil {
		log.Println("Error in refreshing market data", err)
		return nil
	}

	dump, err := httputil.DumpResponse(resp, true)
	defer resp.Body.Close()

	var responseJson nseQuoteResponse
	err = json.NewDecoder(resp.Body).Decode(&responseJson)

	if err != nil {
		log.Println("Error in decoding quote response", err)

		log.Println("==== BODy RESPONSE ====")
		log.Println(string(dump))
		return nil
	}

	quote := models.Quote{
		Symbol:         *models.GetSymbolByName(utils.NSECM, symbolName),
		Close:          responseJson.PriceInfo.PreviousClose,
		High:           responseJson.PriceInfo.IntraDayHighLow.Max,
		Low:            responseJson.PriceInfo.IntraDayHighLow.Min,
		Open:           responseJson.PriceInfo.Open,
		LastTradePrice: responseJson.PriceInfo.LastPrice,
	}

	tx := database.DB.Db.Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "symbol_id"}},
		UpdateAll: true,
	}).Create(&quote)

	if tx.Error != nil {
		log.Println("Error in updating quote data", tx.Error)
		return nil
	}
	log.Println("Quote updated for NSE ", symbolName)

	return &quote
}

func RefreshOrderDepth(symbolName string) *models.Depth {
	uri, err := url.Parse(utils.NSE_EQUITY_QUOTE)
	if err != nil {
		log.Println("Error in parsing market data url", err)
	}
	q := uri.Query()
	q.Set("symbol", symbolName)
	q.Set("section", "trade_info")
	uri.RawQuery = q.Encode()

	resp, err := nseHttpClient.Get(uri.String())
	if err != nil {
		log.Println("Error in refreshing market data", err)
		return nil
	}
	dump, err := httputil.DumpResponse(resp, true)
	defer resp.Body.Close()

	var responseJson nseDepthResponse
	err = json.NewDecoder(resp.Body).Decode(&responseJson)

	if err != nil {
		log.Println("Error in decoding depth response", err)

		log.Println("==== BODy RESPONSE ====")
		log.Println(string(dump))
		return nil
	}

	depth := models.Depth{
		Symbol:    *models.GetSymbolByName(utils.NSECM, symbolName),
		AskPrices: make([]float64, len(responseJson.MarketDeptOrderBook.Ask)),
		AskQty:    make([]int64, len(responseJson.MarketDeptOrderBook.Ask)),
		BidPrices: make([]float64, len(responseJson.MarketDeptOrderBook.Bid)),
		BidQty:    make([]int64, len(responseJson.MarketDeptOrderBook.Bid)),
	}

	for i, s := range responseJson.MarketDeptOrderBook.Ask {
		depth.AskPrices[i] = s.Price
		depth.AskQty[i] = s.Quantity
	}

	for i, s := range responseJson.MarketDeptOrderBook.Bid {
		depth.BidPrices[i] = s.Price
		depth.BidQty[i] = s.Quantity
	}

	tx := database.DB.Db.Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "symbol_id"}},
		UpdateAll: true,
	}).Create(&depth)

	if tx.Error != nil {
		log.Println("Error in updating depth data", tx.Error)
		return nil
	}
	log.Println("depth updated for NSE ", symbolName)

	return &depth
}
