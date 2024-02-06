package nseMarket

type nseQuoteResponse struct {
	Info struct {
		Symbol              string   `json:"symbol"`
		CompanyName         string   `json:"companyName"`
		Industry            string   `json:"industry"`
		ActiveSeries        []string `json:"activeSeries"`
		DebtSeries          []any    `json:"debtSeries"`
		TempSuspendedSeries []any    `json:"tempSuspendedSeries"`
		IsFNOSec            bool     `json:"isFNOSec"`
		IsCASec             bool     `json:"isCASec"`
		IsSLBSec            bool     `json:"isSLBSec"`
		IsDebtSec           bool     `json:"isDebtSec"`
		IsSuspended         bool     `json:"isSuspended"`
		IsETFSec            bool     `json:"isETFSec"`
		IsDelisted          bool     `json:"isDelisted"`
		Isin                string   `json:"isin"`
		IsTop10             bool     `json:"isTop10"`
		Identifier          string   `json:"identifier"`
	} `json:"info"`
	Metadata struct {
		Series         string  `json:"series"`
		Symbol         string  `json:"symbol"`
		Isin           string  `json:"isin"`
		Status         string  `json:"status"`
		ListingDate    string  `json:"listingDate"`
		Industry       string  `json:"industry"`
		LastUpdateTime string  `json:"lastUpdateTime"`
		PdSectorPe     float64 `json:"pdSectorPe"`
		PdSymbolPe     float64 `json:"pdSymbolPe"`
		PdSectorInd    string  `json:"pdSectorInd"`
	} `json:"metadata"`
	SecurityInfo struct {
		BoardStatus    string `json:"boardStatus"`
		TradingStatus  string `json:"tradingStatus"`
		TradingSegment string `json:"tradingSegment"`
		SessionNo      string `json:"sessionNo"`
		Slb            string `json:"slb"`
		ClassOfShare   string `json:"classOfShare"`
		Derivatives    string `json:"derivatives"`
		Surveillance   struct {
			Surv any `json:"surv"`
			Desc any `json:"desc"`
		} `json:"surveillance"`
		FaceValue  float64 `json:"faceValue"`
		IssuedSize int64   `json:"issuedSize"`
	} `json:"securityInfo"`
	PriceInfo struct {
		LastPrice       float64 `json:"lastPrice"`
		Change          float64 `json:"change"`
		PChange         float64 `json:"pChange"`
		PreviousClose   float64 `json:"previousClose"`
		Open            float64 `json:"open"`
		Close           float64 `json:"close"`
		Vwap            float64 `json:"vwap"`
		LowerCP         string  `json:"lowerCP"`
		UpperCP         string  `json:"upperCP"`
		PPriceBand      string  `json:"pPriceBand"`
		BasePrice       float64 `json:"basePrice"`
		IntraDayHighLow struct {
			Min   float64 `json:"min"`
			Max   float64 `json:"max"`
			Value float64 `json:"value"`
		} `json:"intraDayHighLow"`
		WeekHighLow struct {
			Min     float64 `json:"min"`
			MinDate string  `json:"minDate"`
			Max     float64 `json:"max"`
			MaxDate string  `json:"maxDate"`
			Value   float64 `json:"value"`
		} `json:"weekHighLow"`
		INavValue any  `json:"iNavValue"`
		CheckINAV bool `json:"checkINAV"`
	} `json:"priceInfo"`
	IndustryInfo struct {
		Macro         string `json:"macro"`
		Sector        string `json:"sector"`
		Industry      string `json:"industry"`
		BasicIndustry string `json:"basicIndustry"`
	} `json:"industryInfo"`
	PreOpenMarket struct {
		Preopen []struct {
			Price   float64 `json:"price"`
			BuyQty  int     `json:"buyQty"`
			SellQty int     `json:"sellQty"`
			Iep     bool    `json:"iep,omitempty"`
		} `json:"preopen"`
		Ato struct {
			Buy  int `json:"buy"`
			Sell int `json:"sell"`
		} `json:"ato"`
		Iep               float64 `json:"IEP"`
		TotalTradedVolume int     `json:"totalTradedVolume"`
		FinalPrice        float64 `json:"finalPrice"`
		FinalQuantity     int     `json:"finalQuantity"`
		LastUpdateTime    string  `json:"lastUpdateTime"`
		TotalBuyQuantity  int     `json:"totalBuyQuantity"`
		TotalSellQuantity int     `json:"totalSellQuantity"`
		AtoBuyQty         int     `json:"atoBuyQty"`
		AtoSellQty        int     `json:"atoSellQty"`
	} `json:"preOpenMarket"`
}

type nseDepthResponse struct {
	NoBlockDeals   bool `json:"noBlockDeals"`
	BulkBlockDeals []struct {
		Name string `json:"name"`
	} `json:"bulkBlockDeals"`
	MarketDeptOrderBook struct {
		TotalBuyQuantity  int `json:"totalBuyQuantity"`
		TotalSellQuantity int `json:"totalSellQuantity"`
		Bid               []struct {
			Price    float64 `json:"price"`
			Quantity int64   `json:"quantity"`
		} `json:"bid"`
		Ask []struct {
			Price    float64 `json:"price"`
			Quantity int64   `json:"quantity"`
		} `json:"ask"`
		TradeInfo struct {
			TotalTradedVolume int     `json:"totalTradedVolume"`
			TotalTradedValue  float64 `json:"totalTradedValue"`
			TotalMarketCap    float64 `json:"totalMarketCap"`
			Ffmc              float64 `json:"ffmc"`
			ImpactCost        float64 `json:"impactCost"`
		} `json:"tradeInfo"`
		ValueAtRisk struct {
			SecurityVar       float64 `json:"securityVar"`
			IndexVar          int     `json:"indexVar"`
			VarMargin         float64 `json:"varMargin"`
			ExtremeLossMargin float64 `json:"extremeLossMargin"`
			AdhocMargin       int     `json:"adhocMargin"`
			ApplicableMargin  float64 `json:"applicableMargin"`
		} `json:"valueAtRisk"`
	} `json:"marketDeptOrderBook"`
	SecurityWiseDP struct {
		QuantityTraded           int     `json:"quantityTraded"`
		DeliveryQuantity         int     `json:"deliveryQuantity"`
		DeliveryToTradedQuantity float64 `json:"deliveryToTradedQuantity"`
		SeriesRemarks            any     `json:"seriesRemarks"`
		SecWiseDelPosDate        string  `json:"secWiseDelPosDate"`
	} `json:"securityWiseDP"`
}
