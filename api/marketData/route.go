package marketData

import "github.com/gofiber/fiber/v2"

func RegisterRoute(route fiber.Router) {
	route.Get("/quote/:symbol", getSymbolQuote)
	route.Get("/depth/:symbol", getSymbolDepth)
}
