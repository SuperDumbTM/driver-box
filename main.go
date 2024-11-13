package main

import (
	"context"
	"driver-box/pkg/execute"
	"driver-box/pkg/store"
	"driver-box/pkg/sysinfo"
	"embed"
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
	if exePath, err := os.Executable(); err != nil {
		panic(err)
	} else {
		dirConf = filepath.Join(filepath.Dir(exePath), "conf")
		if _, err := os.Stat(dirConf); err != nil {
			if err := os.MkdirAll(dirConf, os.ModePerm); err != nil {
				panic(err)
			}
		}

		dirDir := filepath.Join(filepath.Dir(exePath), "drivers")
		if _, err := os.Stat(dirDir); err != nil {
			if err := os.MkdirAll(dirDir, os.ModePerm); err != nil {
				panic(err)
			}
		}

		for _, name := range [3]string{"network", "display", "miscellaneous"} {
			os.MkdirAll(filepath.Join(dirDir, name), os.ModePerm)
		}
	}

	app := &App{}
	mgt := &execute.CommandExecutor{}

	err := wails.Run(&options.App{
		Title:  "driver-box",
		Width:  768,
		Height: 576,
		AssetServer: &assetserver.Options{
			Assets: assets,
		},
		BackgroundColour: &options.RGBA{R: 27, G: 38, B: 54, A: 1},
		OnStartup: func(ctx context.Context) {
			app.SetContext(ctx)
			mgt.SetContext(ctx)
		},
		Bind: []interface{}{
			app,
			mgt,
			&store.DriverManager{Path: filepath.Join(dirConf, "drivers.json")},
			&store.AppSettingManager{Path: filepath.Join(dirConf, "setting.json")},
			&sysinfo.SysInfo{},
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
