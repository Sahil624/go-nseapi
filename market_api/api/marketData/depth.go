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

// getSymbolDepth is a function to get depth of scrips from database
// @Summary Get depth of specific symbols
// @Description Get depth of requested symbol on market. This is fetched via [https://www.nseindia.com/api/quote-equity?symbol=INFY&section=trade_info] from NSE website
// @Tags Market Data
// @Param symbolName path string true "Symbol Name"
// @Accept json
// @Produce json
// @Success 200 {object} utils.ResponseHTTP{data=models.Depth}
// @Router /market_data/depth/{symbolName} [get]
func getSymbolDepth(ctx *fiber.Ctx) error {
	symbolName := ctx.Params("symbol")

	if symbolName == "" {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "invalid symbol name",
		})
	}

	var depth models.Depth
	tx := database.DB.Db.Joins("JOIN scrips as symb ON symb.id=depths.symbol_id").First(&depth, "symb.symbol = ? AND symb.market = ?", symbolName, utils.NSECM)

	if tx.Error != nil && !errors.Is(tx.Error, gorm.ErrRecordNotFound) {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": tx.Error.Error(),
		})
	}

	if time.Now().Sub(depth.UpdatedAt).Minutes() > utils.QUOTE_EXPIRY_TIME {
		log.Println("Update depth for", symbolName)
		depth = *nseMarket.RefreshOrderDepth(symbolName)
	}

	return ctx.JSON(utils.ResponseHTTP{
		Success: true,
		Message: "Quote Data",
		Data:    depth,
	})
}
