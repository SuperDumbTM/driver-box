package execute

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"os/exec"
	"time"

	"github.com/puzpuzpuz/xsync/v3"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

type CommandExecutor struct {
	ctx      context.Context
	commands *xsync.MapOf[string, Command]
}

func (ce *CommandExecutor) SetContext(ctx context.Context) {
	ce.ctx = ctx
}

func (ce *CommandExecutor) Run(program string, options []string) string {
	if ce.commands == nil {
		ce.commands = xsync.NewMapOf[string, Command]()
	}

	cmdId := ""
	for cmdId == "" {
		b := make([]byte, 4)
		if _, err := rand.Read(b); err != nil {
			continue
		}

		id := hex.EncodeToString(b)
		if _, ok := ce.commands.Load(id); ok {
			continue
		}
		cmdId = id
	}

	command := Command{
		cmd: exec.Command(program, options...),
	}
	command.cmd.Stdout = &command.stdout
	command.cmd.Stderr = &command.stderr

	ce.commands.Store(cmdId, command)

	go ce.dispatch(cmdId, &command)

	return cmdId
}

func (ce *CommandExecutor) Abort(id string) error {
	if task, ok := ce.commands.Load(id); !ok {
		return errors.New("execute: id not found")
	} else {
		if err := task.Stop(); err != nil {
			return errors.New("execute: abort failed")
		}
		return nil
	}
}

func (ce *CommandExecutor) dispatch(id string, command *Command) CommandResult {
	command.startTime = time.Now()
	command.err = command.cmd.Run()

	result := CommandResult{
		id,
		command.Lapse(),
		command.cmd.ProcessState.ExitCode(),
		command.stdout.String(),
		command.stderr.String(),
		command.err.Error(),
	}

	runtime.EventsEmit(ce.ctx, "execute:exited", result)
	return result
}
