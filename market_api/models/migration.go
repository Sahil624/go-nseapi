package models

import (
	"go-nseapi/database"
	"log"
)

func MigrateDB() bool {

	err := database.DB.Db.AutoMigrate(&Scrip{})

	if err != nil {
		log.Println("error in auto migrate:", err)
		return false
	}

	err = database.DB.Db.AutoMigrate(&Quote{})

	if err != nil {
		log.Println("error in auto migrate:", err)
		return false
	}

	err = database.DB.Db.AutoMigrate(&Depth{})

	if err != nil {
		log.Println("error in auto migrate:", err)
		return false
	}

	return true
}
