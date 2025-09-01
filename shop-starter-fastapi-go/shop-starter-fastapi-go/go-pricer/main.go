// go:build ignore
package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
	"os"
	"strconv"
)

type QuoteRequest struct {
	WidthCm         float64 `json:"width_cm"`
	HeightCm        float64 `json:"height_cm"`
	Material        string  `json:"material"` // "pvc" or "mesh"
	MagnetSpacingCm *float64 `json:"magnet_spacing_cm"`
}

type QuoteResponse struct {
	TotalPrice           float64 `json:"total_price"`
	AreaSqm              float64 `json:"area_sqm"`
	MaterialRatePerSqm   float64 `json:"material_rate_per_sqm"`
	MagnetCount          int     `json:"magnet_count"`
	MagnetUnitPrice      float64 `json:"magnet_unit_price"`
	MagnetsCost          float64 `json:"magnets_cost"`
	Notes                string  `json:"notes,omitempty"`
}

func getenvFloat(key string, fallback float64) float64 {
	if v := os.Getenv(key); v != "" {
		if f, err := strconv.ParseFloat(v, 64); err == nil {
			return f
		}
	}
	return fallback
}

func quoteHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
	var req QuoteRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte(`{"error":"invalid json"}`))
		return
	}
	if req.WidthCm <= 0 || req.HeightCm <= 0 {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte(`{"error":"width_cm and height_cm must be > 0"}`))
		return
	}

	// Pricing parameters with env overrides (AZN)
	pvcRate := getenvFloat("PVC_RATE_PER_SQM", 25.0)
	meshRate := getenvFloat("MESH_RATE_PER_SQM", 15.0)
	magnetUnit := getenvFloat("MAGNET_UNIT_PRICE", 0.30)

	var rate float64
	switch req.Material {
	case "pvc", "PVC":
		rate = pvcRate
	case "mesh", "Mesh", "tor", "TOR":
		rate = meshRate
	default:
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte(`{"error":"material must be 'pvc' or 'mesh'"}`))
		return
	}

	area := (req.WidthCm / 100.0) * (req.HeightCm / 100.0)
	materialCost := area * rate

	perimeter := 2.0 * (req.WidthCm + req.HeightCm) // cm
	spacing := 10.0
	if req.MagnetSpacingCm != nil && *req.MagnetSpacingCm > 0 {
		spacing = *req.MagnetSpacingCm
	}
	magnetCount := int(math.Ceil(perimeter / spacing))
	magnetsCost := float64(magnetCount) * magnetUnit

	total := materialCost + magnetsCost

	resp := QuoteResponse{
		TotalPrice:         math.Round(total*100) / 100, // 2 decimals
		AreaSqm:            math.Round(area*1000) / 1000,
		MaterialRatePerSqm: rate,
		MagnetCount:        magnetCount,
		MagnetUnitPrice:    magnetUnit,
		MagnetsCost:        math.Round(magnetsCost*100) / 100,
		Notes:              "Prices in AZN; override with env vars PVC_RATE_PER_SQM, MESH_RATE_PER_SQM, MAGNET_UNIT_PRICE",
	}
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	json.NewEncoder(w).Encode(resp)
}

func main() {
	http.HandleFunc("/quote", quoteHandler)
	addr := ":8080"
	log.Println("Go pricer listening on", addr)
	log.Fatal(http.ListenAndServe(addr, nil))
}
