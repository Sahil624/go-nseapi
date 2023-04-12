package staticData

import "github.com/gofiber/fiber/v2"

func RegisterRoutes(route fiber.Router) {
	route.Get("/scrips", listAllScrips)
}
