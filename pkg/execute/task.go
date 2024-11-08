package execute

import (
	"bytes"
	"os/exec"
	"time"
)

type Command struct {
	Program   string   `json:"program"`
	Options   []string `json:"options"`
	cmd       *exec.Cmd
	startTime time.Time
	stdout    bytes.Buffer
	stderr    bytes.Buffer
	err       error
}

func (t *Command) Start() {
	t.startTime = time.Now()

	t.cmd = exec.Command(t.Program, t.Options...)
	t.cmd.Stdout = &t.stdout
	t.cmd.Stderr = &t.stderr
	t.err = t.cmd.Run()
}

func (t Command) Stop() error {
	return t.cmd.Process.Kill()
}
