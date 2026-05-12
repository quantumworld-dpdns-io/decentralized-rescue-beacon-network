package api

import (
	"slices"
	"strings"
)

func sortedKeys(set map[string]bool) []string {
	keys := make([]string, 0, len(set))
	for k := range set {
		keys = append(keys, k)
	}
	slices.Sort(keys)
	return keys
}

func joinStrings(items []string) string {
	return strings.Join(items, ",")
}
