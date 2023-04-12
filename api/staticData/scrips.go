package staticData

import (
	"github.com/gofiber/fiber/v2"
	"go-nseapi/database"
	"go-nseapi/models"
	"go-nseapi/utils"
)

// listAllScrips is a function to get all scrips from database
// @Summary Get all Scrips
// @Description Get all scrips listed on market. This is fetched via [https://archives.nseindia.com/content/equities/EQUITY_L.csv] from NSE website
// @Tags Static Data
// @Accept json
// @Produce json
// @Success 200 {object} utils.ResponseHTTP{data=[]models.Scrip}
// @Router /static_data/scrips [get]
func listAllScrips(ctx *fiber.Ctx) error {
	var scrips []models.Scrip
	tx := database.DB.Db.Find(&scrips)

	if tx.Error != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"err": tx.Error.Error(),
		})
	}

	return ctx.JSON(utils.ResponseHTTP{
		Data:    scrips,
		Message: "List of all scrips",
		Success: true,
	})
}
