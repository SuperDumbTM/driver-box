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

func (a *App) SelectFile(relative bool) (string, error) {
	if path, err := runtime.OpenFileDialog(a.ctx, runtime.OpenDialogOptions{}); err != nil || path == "" {
		return "", err
	} else if relative {
		if basePath, err := os.Executable(); err != nil {
			return "", err
		} else {
			return filepath.Rel(basePath, path)
		}
	} else {
		return path, nil
	}

}

func (a *App) RunCommand(program string, options []string) (string, error) {
	output, err := exec.Command(program, options...).Output()
	return string(output), err
}
