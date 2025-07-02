// testing/back/test1.go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "log"
    "net/http"
    "sync"
    "time"
)

type Entity struct {
    ID     int    `json:"id"`
    Status string `json:"status"`
    ETA    *int   `json:"eta,omitempty"`
}

func createOrder(baseURL string, items []int) (int, error) {
    body, _ := json.Marshal(map[string]interface{}{"items": items})
    resp, err := http.Post(baseURL+"/orders", "application/json", bytes.NewBuffer(body))
    if err != nil {
        return 0, err
    }
    defer resp.Body.Close()
    if resp.StatusCode != 201 {
        data, _ := io.ReadAll(resp.Body)
        return 0, fmt.Errorf("bad status %d: %s", resp.StatusCode, string(data))
    }
    var e Entity
    if err := json.NewDecoder(resp.Body).Decode(&e); err != nil {
        return 0, err
    }
    return e.ID, nil
}

func createReservation(baseURL, name string, party int) (int, error) {
    body, _ := json.Marshal(map[string]interface{}{
        "name":       name,
        "party_size": party,
    })
    resp, err := http.Post(baseURL+"/reservations", "application/json", bytes.NewBuffer(body))
    if err != nil {
        return 0, err
    }
    defer resp.Body.Close()
    if resp.StatusCode != 201 {
        data, _ := io.ReadAll(resp.Body)
        return 0, fmt.Errorf("bad status %d: %s", resp.StatusCode, string(data))
    }
    var e Entity
    if err := json.NewDecoder(resp.Body).Decode(&e); err != nil {
        return 0, err
    }
    return e.ID, nil
}

func pollEntity(baseURL, path string, id int, wg *sync.WaitGroup) {
    defer wg.Done()
    url := fmt.Sprintf("%s%s/%d", baseURL, path, id)
    ticker := time.NewTicker(1 * time.Second)
    defer ticker.Stop()

    for range ticker.C {
        resp, err := http.Get(url)
        if err != nil {
            log.Printf("Error polling %s/%d: %v", path, id, err)
            return
        }
        var e Entity
        if resp.StatusCode == 404 {
            log.Printf("%s %d: not found", path, id)
            resp.Body.Close()
            return
        }
        if err := json.NewDecoder(resp.Body).Decode(&e); err != nil {
            log.Printf("Invalid JSON %s/%d: %v", path, id, err)
            resp.Body.Close()
            return
        }
        resp.Body.Close()

        fmt.Printf("%s %d: status=%s", path, id, e.Status)
        if e.ETA != nil {
            fmt.Printf(" eta=%ds", *e.ETA)
        }
        fmt.Println()

        if e.Status == "done" {
            return
        }
    }
}

func main() {
    baseURL := "http://localhost:8000"
    numOrders := 5
    numReservations := 3

    orderCh := make(chan int, numOrders)
    resCh   := make(chan int, numReservations)
    var wg sync.WaitGroup

    // 1) Crear órdenes concurrentemente
    for i := 0; i < numOrders; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            id, err := createOrder(baseURL, []int{1, 2})
            if err != nil {
                log.Printf("Error creando orden: %v", err)
                return
            }
            log.Printf("Orden creada: %d", id)
            orderCh <- id
        }()
    }

    // 2) Crear reservas concurrentemente
    for i := 0; i < numReservations; i++ {
        wg.Add(1)
        go func(i int) {
            defer wg.Done()
            id, err := createReservation(baseURL, fmt.Sprintf("User%d", i+1), i+2)
            if err != nil {
                log.Printf("Error creando reserva: %v", err)
                return
            }
            log.Printf("Reserva creada: %d", id)
            resCh <- id
        }(i)
    }

    // Esperamos a que terminen de crearse (pero no cerramos canales todavía)
    wg.Wait()
    close(orderCh)
    close(resCh)

    // Recopilamos IDs en slices
    var orderIDs, resIDs []int
    for id := range orderCh {
        orderIDs = append(orderIDs, id)
    }
    for id := range resCh {
        resIDs = append(resIDs, id)
    }

    // 3) Poll para órdenes y reservas
    fmt.Println("Comenzando polling de estado...")
    for _, id := range orderIDs {
        wg.Add(1)
        go pollEntity(baseURL, "/orders", id, &wg)
    }
    for _, id := range resIDs {
        wg.Add(1)
        go pollEntity(baseURL, "/reservations", id, &wg)
    }

    wg.Wait()
    fmt.Println("Todas las entidades completadas.")
}

