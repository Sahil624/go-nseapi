package server

import (
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/fiber/v2/middleware/monitor"
	"github.com/gofiber/fiber/v2/middleware/recover"
)

func addMiddlewares(app *fiber.App) {
	app.Use(cors.New())
	//app.Use(limiter.New())
	app.Use(logger.New())

	app.Get("/server/metrics", monitor.New(monitor.Config{Title: "go-note Metrics Page"}))

	app.Use(recover.New())

	app.Use(func(c *fiber.Ctx) error {
		c.Locals("signature", c.Cookies("user-signature", "public"))
		return c.Next()
	})
}
