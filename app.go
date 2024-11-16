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

type CommandResult struct {
	Stdout   string `json:"stdout"`
	ExitCode int    `json:"exitCode"`
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
		if exePath, err := os.Executable(); err != nil {
			return "", err
		} else {
			return filepath.Rel(filepath.Dir(exePath), path)
		}
	} else {
		return path, nil
	}

}

func (a *App) RunCommand(program string, options []string) (CommandResult, error) {
	if stdout, err := exec.Command(program, options...).CombinedOutput(); err == nil {
		return CommandResult{string(stdout), 0}, err
	} else if exterr, ok := err.(*exec.ExitError); ok {
		return CommandResult{string(stdout), exterr.ExitCode()}, nil
	} else {
		return CommandResult{string(stdout), -1}, err
	}
}

func (a App) PathExists(path string) bool {
	_, err := os.Stat(path)
	return err != nil
}
