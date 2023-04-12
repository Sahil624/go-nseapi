package nseMarket

import (
	"go-nseapi/utils"
	"log"
	"net/http"
	"net/http/httputil"
	"strings"
)

var cookies []string
var nseHttpClient *http.Client

type transport struct {
	underlyingTransport http.RoundTripper
}

func (t *transport) RoundTrip(req *http.Request) (*http.Response, error) {
	req.Header.Add("authority", "www.nseindia.com")
	req.Header.Add("accept", "*/*")
	req.Header.Add("accept-language", "en-GB,en;q=0.8")
	req.Header.Add("referer", "https://www.nseindia.com/get-quotes/")
	req.Header.Add("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
	if len(cookies) > 0 {
		req.Header.Add("cookie", strings.Join(cookies, ";"))
	}
	reqDump, _ := httputil.DumpRequest(req, true)
	log.Println("========= REQUEST DUMP =========")
	log.Println(string(reqDump))
	resp, err := t.underlyingTransport.RoundTrip(req)

	if len(resp.Header.Values("set-cookies")) > 0 {
		cookies = resp.Header.Values("set-cookies")
	}

	return resp, err
}

func setCookie() {
	resp, err := nseHttpClient.Get(utils.NSE_EQUITY_HOME)

	if err != nil {
		log.Println("Error in getting NSE QUITY HOMEPAGE", err)
		return
	}

	respDump, _ := httputil.DumpResponse(resp, false)

	log.Println("========== DUMP COOKIE RESPONSE ========")
	log.Println(string(respDump))

	cookies = resp.Header.Values("set-cookies")
	cookies = append(cookies, resp.Header.Values("Set-Cookie")...)

	log.Println("NSE cookie updated", len(cookies))
}

func init() {
	nseHttpClient = &http.Client{
		Transport: &transport{underlyingTransport: http.DefaultTransport},
	}

	setCookie()
}
