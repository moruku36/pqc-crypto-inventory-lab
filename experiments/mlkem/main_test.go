package main

import "testing"

func TestSummary(t *testing.T) {
	s := summarize([]int64{5, 1, 3, 2, 4})
	if s.MedianNS != 3 || s.P95NS != 5 {
		t.Fatal(s)
	}
}
