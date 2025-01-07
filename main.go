package main

import (
	"context"
	"driver-box/pkg/execute"
	"driver-box/pkg/porter"
	"driver-box/pkg/store"
	"driver-box/pkg/sysinfo"
	"embed"
	"os"
	"path/filepath"

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
	"github.com/wailsapp/wails/v2/pkg/options/windows"
)

//go:embed all:frontend/dist
var assets embed.FS

func main() {
	var (
		dirRoot string
		/* Path to the configuration directory */
		dirConf string
		/* Path to the driver directory */
		dirDir string
		/* Path to the WebView2 executable */
		pathWV2 string
	)

	if pathExe, err := os.Executable(); err != nil {
		panic(err)
	} else {
		dirRoot = filepath.Dir(pathExe)

		dirConf = filepath.Join(dirRoot, "conf")
		if _, err := os.Stat(dirConf); err != nil {
			if err := os.MkdirAll(dirConf, os.ModePerm); err != nil {
				panic(err)
			}
		}

		dirDir = filepath.Join(dirRoot, "drivers")
		if _, err := os.Stat(dirDir); err != nil {
			if err := os.MkdirAll(dirDir, os.ModePerm); err != nil {
				panic(err)
			}
		}

		for _, name := range [3]string{"network", "display", "miscellaneous"} {
			os.MkdirAll(filepath.Join(dirDir, name), os.ModePerm)
		}

		// WebView2 binary lookup
		pathWV2 = filepath.Join(dirRoot, "bin", "WebView2")
		if _, err := os.Stat(pathWV2); err != nil {
			pathWV2 = ""
		}
	}

	app := &App{}
	mgt := &execute.CommandExecutor{}

	err := wails.Run(&options.App{
		Title:     "driver-box",
		Width:     768,
		Height:    576,
		MinWidth:  640,
		MinHeight: 480,
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
			&store.DriverGroupManager{Path: filepath.Join(dirConf, "groups.json")},
			&store.AppSettingManager{Path: filepath.Join(dirConf, "setting.json")},
			&porter.Porter{DirRoot: dirRoot, DirConf: dirConf, DirDriver: dirDir},
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
		Windows: &windows.Options{
			WebviewBrowserPath: pathWV2,
		},
	})

	if err != nil {
		println("Error:", err.Error())
	}
}
