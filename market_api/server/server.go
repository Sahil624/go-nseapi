package server

import (
	"github.com/gofiber/fiber/v2"
	"go-nseapi/api"
)

func NewServer() *fiber.App {
	app := fiber.New(fiber.Config{
		AppName: "go-note",
	})

	addMiddlewares(app)
	api.RegisterRoute(app)
	return app
}
