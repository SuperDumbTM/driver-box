package config

import (
	"os"
	"path/filepath"
)

// Path to /conf
var basePath string

func init() {
	exePath, err := os.Executable()
	if err != nil {
		panic(err)
	}
	
	basePath = filepath.Join(filepath.Dir(exePath), "conf")
	if _, err := os.Stat(basePath); err != nil {
		if err := os.MkdirAll(basePath, os.ModePerm); err != nil {
			panic(err)
		}
	}
}

type DriverType string

const (
	Network       DriverType = "network"
	Display       DriverType = "display"
	Miscellaneous DriverType = "miscellaneous"
)

type DriverConfig struct {
	Id           string
	Name         string
	Type         DriverType
	Path         string
	Flags        []string
	MinExeTime   float32
	AllowRtCodes []int32
}