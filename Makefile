all: doc-compile go-compile

doc-compile:
	swag init -g cmd/go-nseapi/main.go --parseDependency --parseInternal

go-compile:
	echo "Compiling server"
	go build -tags netgo -ldflags '-s -w' cmd/go-nseapi/main.go