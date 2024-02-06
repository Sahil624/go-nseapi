package api

import (
	"github.com/gofiber/fiber/v2"
	"go-nseapi/api/marketData"
	"go-nseapi/api/staticData"
)

func RegisterRoute(app *fiber.App) {
	api := app.Group("/api/v1")

	staticData.RegisterRoutes(api.Group("/static_data"))
	marketData.RegisterRoute(api.Group("/market_data"))
}
