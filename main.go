package main

import (
	"driver-box/pkg/execute"
	"driver-box/pkg/store"
	"driver-box/pkg/sysinfo"
	"embed"
	"fmt"
	"os"
	"path/filepath"

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
)

//go:embed all:frontend/dist
var assets embed.FS

func main() {
	// setup /conf directorys
	var dirConf string
	if dirRoot, err := os.Executable(); err != nil {
		panic(err)
	} else {
		dirConf := filepath.Join(filepath.Dir(dirRoot), "conf")
		fmt.Println(dirConf)
		if _, err := os.Stat(dirConf); err != nil {
			if err := os.MkdirAll(dirConf, os.ModePerm); err != nil {
				panic(err)
			}
		}
	}

	app := NewApp()

	err := wails.Run(&options.App{
		Title:  "driver-box",
		Width:  800,
		Height: 600,
		AssetServer: &assetserver.Options{
			Assets: assets,
		},
		BackgroundColour: &options.RGBA{R: 27, G: 38, B: 54, A: 1},
		OnStartup:        app.startup,
		Bind: []interface{}{
			app,
			&store.DriverManager{Path: filepath.Join(dirConf, "drivers.json")},
			&store.AppSettingManager{Path: filepath.Join(dirConf, "setting.json")},
			&sysinfo.SysInfo{},
			&execute.CommandExecutor{},
		},
		EnumBind: []interface{}{
			[]struct {
				Value  store.DriverType
				TSName string
			}{
				{store.Network, "NETWORK"},
				{store.Display, "DISPLAY"},
				{store.Miscellaneous, "MISCELLANEOUS"},
			},
			[]struct {
				Value  store.SuccessAction
				TSName string
			}{
				{store.Nothing, "NOTHING"},
				{store.Reboot, "REBOOT"},
				{store.Shutdown, "SHUTDOWN"},
				{store.Firmware, "FIRMWARE"},
			},
		},
	})

	if err != nil {
		println("Error:", err.Error())
	}
}
