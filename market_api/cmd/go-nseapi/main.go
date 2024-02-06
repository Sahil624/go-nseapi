package main

import (
	"github.com/gofiber/swagger"
	"github.com/joho/godotenv"
	"go-nseapi/database"
	_ "go-nseapi/docs"
	"go-nseapi/models"
	"go-nseapi/nseMarket"
	"go-nseapi/server"
	"log"
	"os"
)

//	@title			Go-NSEApi
//	@version		1.0
//	@description	Unofficial NSE APIs for snapshot market data and static Data

//	@contact.email	codingitperfect@protonmail.com

//	@license.name	Apache 2.0
//	@license.url	http://www.apache.org/licenses/LICENSE-2.0.html

//	@host		localhost:8080
//	@BasePath	/api/v1

// @externalDocs.description	OpenAPI
// @externalDocs.url			https://swagger.io/resources/open-api/
func main() {
	godotenv.Load()
	port := os.Getenv("PORT")

	database.ConnectDb()
	if !models.MigrateDB() {
		os.Exit(-1)
	}
	go nseMarket.RefreshSymbolList()

	if port == "" {
		port = "8080"
	}

	app := server.NewServer()

	app.Get("/*", swagger.HandlerDefault) // default

	app.Get("/*", swagger.New(swagger.Config{ // custom
		URL:         "index.html",
		DeepLinking: false,
	}))

	if err := app.Listen(":" + port); err != nil {
		log.Panicf("error in running server: %s", err)
	}
}
