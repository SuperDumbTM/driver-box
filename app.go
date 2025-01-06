package main

import (
	"context"
	"os"
	"os/exec"
	"path/filepath"

	"github.com/wailsapp/wails/v2/pkg/runtime"
)

type App struct {
	ctx context.Context
}

func NewApp() *App {
	return &App{}
}

func (m *App) SetContext(ctx context.Context) {
	m.ctx = ctx
}

func (a *App) Cwd() (string, error) {
	if exePath, err := os.Executable(); err != nil {
		return "", err
	} else {
		return filepath.Dir(exePath), nil
	}
}

func (a *App) SelectFolder(relative bool) (string, error) {
	if path, err := runtime.OpenDirectoryDialog(a.ctx, runtime.OpenDialogOptions{}); err != nil || path == "" {
		return "", err
	} else if relative {
		if exePath, err := os.Executable(); err != nil {
			return "", err
		} else {
			return filepath.Rel(filepath.Dir(exePath), path)
		}
	} else {
		return path, nil
	}

}

func (a *App) SelectFile(relative bool) (string, error) {
	if path, err := runtime.OpenFileDialog(a.ctx, runtime.OpenDialogOptions{}); err != nil || path == "" {
		return "", err
	} else if relative {
		if exePath, err := os.Executable(); err != nil {
			return "", err
		} else {
			return filepath.Rel(filepath.Dir(exePath), path)
		}
	} else {
		return path, nil
	}

}

func (a App) PathExists(path string) bool {
	_, err := os.Stat(path)
	return err != nil
}

func (a App) ExecutableExists(path string) bool {
	_, err := exec.LookPath(path)
	return err == nil
}
