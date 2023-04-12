all: doc-compile go-compile

doc-compile:
	go install github.com/swaggo/swag/cmd/swag@latest
	swag init -g cmd/go-nseapi/main.go --parseDependency --parseInternal

go-compile:
	echo "Compiling go"
	go get -u -v -f all
	go build -v -tags netgo -ldflags '-s -w' cmd/go-nseapi/main.go