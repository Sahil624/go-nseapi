package marketData

import (
	"errors"
	"github.com/gofiber/fiber/v2"
	"go-nseapi/database"
	"go-nseapi/models"
	"go-nseapi/nseMarket"
	"go-nseapi/utils"
	"gorm.io/gorm"
	"log"
	"time"
)

// getSymbolQuote is a function to get quote of scrips from database
// @Summary Get quote of specific symbols
// @Description Get quote of requested symbol on market. This is fetched via [https://www.nseindia.com/api/quote-equity?symbol=INFY] from NSE website
// @Tags Market Data
// @Param symbolName path string true "Symbol Name"
// @Accept json
// @Produce json
// @Success 200 {object} utils.ResponseHTTP{data=models.Quote}
// @Router /market_data/quote/{symbolName} [get]
func getSymbolQuote(ctx *fiber.Ctx) error {
	symbolName := ctx.Params("symbol")

	if symbolName == "" {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "invalid symbol name",
		})
	}

	var quote models.Quote
	tx := database.DB.Db.Joins("JOIN scrips as symb ON symb.id=quotes.symbol_id").First(&quote, "symb.symbol = ? AND symb.market = ?", symbolName, utils.NSECM)

	if tx.Error != nil && !errors.Is(tx.Error, gorm.ErrRecordNotFound) {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": tx.Error.Error(),
		})
	}

	if time.Now().Sub(quote.UpdatedAt).Minutes() > utils.QUOTE_EXPIRY_TIME {
		log.Println("Update quote for", symbolName)
		quote = *nseMarket.RefreshMarketData(symbolName)
	}

	return ctx.JSON(utils.ResponseHTTP{
		Success: true,
		Message: "Quote Data",
		Data:    quote,
	})
}
