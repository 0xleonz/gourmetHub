// apiGateway/main.go
package main

import (
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
)

func main() {
	// Crear proxies para los servicios
	orderProxy := createProxy("http://order-service:8080")
	reservationProxy := createProxy("http://reservation-service:8080")

	// Configurar rutas
	http.Handle("/order", orderProxy)
	http.Handle("/reservation", reservationProxy)

	// Health Check
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("OK"))
	})

	log.Println(" running:8080")
	http.ListenAndServe(":8080", nil)
}

// Crea un proxy para un servicio
func createProxy(target string) *httputil.ReverseProxy {
	url, _ := url.Parse(target)
	return httputil.NewSingleHostReverseProxy(url)
}
