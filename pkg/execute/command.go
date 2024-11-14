package execute

import (
	"bytes"
	"errors"
	"os/exec"
	"time"

	"github.com/shirou/gopsutil/v3/process"
)

type CommandResult struct {
	Id       string  `json:"id"`
	Lapse    float32 `json:"lapse"`
	ExitCode int     `json:"exitCode"`
	Stdout   string  `json:"stdout"`
	Stderr   string  `json:"stderr"`
	Error    string  `json:"error"`
	Aborted  bool    `json:"aborted"`
}

type Command struct {
	cmd       *exec.Cmd
	startTime time.Time
	stdout    bytes.Buffer
	stderr    bytes.Buffer
	err       error
	aborted   bool
}

func (t *Command) Start() {
	t.startTime = time.Now()
	t.err = t.cmd.Start()
}

func (t *Command) Stop() error {
	if t.cmd.Process == nil {
		panic("execute: called Stop before command started")
	}

	proc, err := process.NewProcess(int32(t.cmd.Process.Pid))
	if err != nil {
		return err
	}

	if children, err := proc.Children(); err != nil {
		return err
	} else {
		var errorChain error = nil
		for _, p := range children {
			if err = p.Kill(); err != nil {
				errorChain = errors.Join(errorChain, err)
			}
		}

		if err := proc.Kill(); err != nil {
			errorChain = errors.Join(errorChain, err)
		}
		t.aborted = errorChain == nil

		return errorChain
	}

}

func (t Command) Lapse() float32 {
	if t.startTime.Year() == 1 {
		return -1.0
	}
	return float32(time.Since(t.startTime).Milliseconds()) / 1000
}
