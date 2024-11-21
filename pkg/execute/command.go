package execute

import (
	"bytes"
	"errors"
	"os/exec"
	"time"

	"github.com/shirou/gopsutil/v3/process"
)

type Command struct {
	cmd       *exec.Cmd
	startTime time.Time
	stdout    bytes.Buffer
	stderr    bytes.Buffer
	stopped   bool
}

func NewCommand(program string, options []string) *Command {
	wrapper := Command{cmd: exec.Command(program, options...)}
	wrapper.cmd.Stdout = &wrapper.stdout
	wrapper.cmd.Stderr = &wrapper.stderr
	return &wrapper
}

func (t *Command) Start() error {
	t.startTime = time.Now()
	return t.cmd.Start()
}

func (t *Command) Wait() error {
	return t.cmd.Wait()
}

func (t *Command) Run() error {
	t.startTime = time.Now()
	return t.cmd.Run()
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

		t.stopped = errorChain == nil

		return errorChain
	}
}

func (t Command) Lapse() float32 {
	if t.startTime.Year() == 1 {
		return -1.0
	}
	return float32(time.Since(t.startTime).Milliseconds()) / 1000
}
