package execute

import (
	"bytes"
	"os/exec"
	"time"
)

type CommandResult struct {
	Id       string  `json:"id"`
	Lapse    float32 `json:"lapse"`
	ExitCode int     `json:"exitCode"`
	Stdout   string  `json:"stdout"`
	Stderr   string  `json:"stderr"`
}

type Command struct {
	cmd       *exec.Cmd
	startTime time.Time
	stdout    bytes.Buffer
	stderr    bytes.Buffer
	err       error
}

func (t *Command) Start() {
	t.startTime = time.Now()
	t.err = t.cmd.Start()
}

func (t Command) Stop() error {
	return t.cmd.Process.Kill()
}

func (t Command) Lapse() float32 {
	if t.startTime.Year() == 1 {
		return -1.0
	}
	return float32(time.Since(t.startTime).Milliseconds()) / 1000
}
