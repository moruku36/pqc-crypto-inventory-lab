// Offline, single-process ML-KEM-768 microbenchmark; experimental keys only.
package main

import (
	"bytes"
	"crypto/mlkem"
	"encoding/json"
	"fmt"
	"os"
	"runtime"
	"sort"
	"time"
)

const warmupBatches = 2
const batches = 20
const batchSize = 100

type stats struct {
	MedianNS int64 `json:"median_batch_mean_ns"`
	P95NS    int64 `json:"p95_batch_mean_ns"`
}

func summarize(v []int64) stats {
	sort.Slice(v, func(i, j int) bool { return v[i] < v[j] })
	return stats{v[len(v)/2], v[(95*len(v)+99)/100-1]}
}
func run() error {
	kg, enc, dec := []int64{}, []int64{}, []int64{}
	dk, err := mlkem.GenerateKey768()
	if err != nil {
		return err
	}
	ek := dk.EncapsulationKey()
	shared, ct := ek.Encapsulate()
	recovered, err := dk.Decapsulate(ct)
	if err != nil {
		return err
	}
	if !bytes.Equal(shared, recovered) {
		return fmt.Errorf("round trip mismatch")
	}
	if len(ek.Bytes()) != 1184 || len(ct) != 1088 || len(shared) != 32 {
		return fmt.Errorf("unexpected sizes")
	}
	for i := 0; i < warmupBatches+batches; i++ {
		start := time.Now()
		for j := 0; j < batchSize; j++ {
			_, err = mlkem.GenerateKey768()
			if err != nil {
				return err
			}
		}
		a := time.Since(start).Nanoseconds() / batchSize
		start = time.Now()
		for j := 0; j < batchSize; j++ {
			shared, ct = ek.Encapsulate()
		}
		b := time.Since(start).Nanoseconds() / batchSize
		start = time.Now()
		for j := 0; j < batchSize; j++ {
			recovered, err = dk.Decapsulate(ct)
			if err != nil {
				return err
			}
		}
		c := time.Since(start).Nanoseconds() / batchSize
		if !bytes.Equal(shared, recovered) {
			return fmt.Errorf("round trip mismatch at batch %d", i)
		}
		if i >= warmupBatches {
			kg = append(kg, a)
			enc = append(enc, b)
			dec = append(dec, c)
		}
	}
	out := struct {
		Go              string `json:"go"`
		OS              string `json:"os"`
		Arch            string `json:"arch"`
		WarmupBatches   int    `json:"warmup_batches"`
		Batches         int    `json:"batches"`
		BatchSize       int    `json:"batch_size"`
		Keygen          stats  `json:"keygen"`
		Encapsulate     stats  `json:"encapsulate"`
		Decapsulate     stats  `json:"decapsulate"`
		PublicKeyBytes  int    `json:"public_key_bytes"`
		CiphertextBytes int    `json:"ciphertext_bytes"`
		SharedKeyBytes  int    `json:"shared_key_bytes"`
	}{runtime.Version(), runtime.GOOS, runtime.GOARCH, warmupBatches, batches, batchSize, summarize(kg), summarize(enc), summarize(dec), 1184, 1088, 32}
	e := json.NewEncoder(os.Stdout)
	e.SetIndent("", "  ")
	return e.Encode(out)
}
func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
