package nseMarket

import (
	"encoding/csv"
	"go-nseapi/database"
	"go-nseapi/models"
	"go-nseapi/utils"
	"gorm.io/gorm/clause"
	"log"
)

func RefreshSymbolList() {
	log.Println("===== Starting Script Master Update ====")
	defer log.Println("===== Completed Script Master Update ====")

	resp, err := nseHttpClient.Get(utils.NSE_SECURITY_LIST)

	if err != nil {
		log.Println("Error in updating security list", err)
		return
	}

	defer resp.Body.Close()
	reader := csv.NewReader(resp.Body)

	data, err := reader.ReadAll()
	if err != nil {
		log.Println("Error in reading security list csv", err)
		return
	}

	scrips := make([]*models.Scrip, len(data)-1)
	for i := range data[1:] {
		scrips[i] = &models.Scrip{
			Market:        utils.NSECM,
			Symbol:        data[i][0],
			CompanyName:   data[i][1],
			Series:        data[i][2],
			DateOfListing: data[i][3],
			PaidUpValue:   data[i][4],
			MarketLot:     data[i][5],
			ISINNumber:    data[i][6],
			FaceValue:     data[i][7],
		}
	}

	txn := database.DB.Db.Clauses(clause.OnConflict{
		DoNothing: true, // column needed to be updated
	}).CreateInBatches(&scrips, 100)

	if txn.Error != nil {
		log.Println("Error inserting ->", txn.Error)
		return
	}

	log.Printf("inserted %d scrips in DB", len(scrips))
}
