package execute

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"os/exec"

	"github.com/puzpuzpuz/xsync/v3"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

type CommandExecutor struct {
	ctx      context.Context
	commands *xsync.MapOf[string, *commandWrapper]
}

func (ce *CommandExecutor) SetContext(ctx context.Context) {
	ce.ctx = ctx
}

func (ce *CommandExecutor) Run(program string, options []string) string {
	if ce.commands == nil {
		ce.commands = xsync.NewMapOf[string, *commandWrapper]()
	}

	command := commandWrapper{cmd: exec.Command(program, options...)}
	command.cmd.Stdout = &command.stdout
	command.cmd.Stderr = &command.stderr

	id := ce.generateId()
	ce.commands.Store(id, &command)

	go ce.dispatch(id)

	return id
}

func (ce *CommandExecutor) Abort(id string) error {
	if task, ok := ce.commands.Load(id); !ok {
		return errors.New("execute: id not found")
	} else {
		if err := task.Stop(); err != nil {
			return errors.Join(errors.New("execute: abort failed"), err)
		}
		return nil
	}
}

func (ce *CommandExecutor) dispatch(id string) {
	if command, ok := ce.commands.Load(id); !ok {
		panic("execute: id not found")
	} else {
		err := command.Run()
		runtime.EventsEmit(ce.ctx, "execute:exited", CommandResult{
			id,
			command.Lapse(),
			command.cmd.ProcessState.ExitCode(),
			command.stdout.String(),
			command.stderr.String(),
			err.Error(),
			command.aborted,
		})
	}
}

func (ce CommandExecutor) generateId() string {
	id := ""
	for id == "" {
		b := make([]byte, 4)
		if _, err := rand.Read(b); err != nil {
			continue
		}

		tmpId := hex.EncodeToString(b)
		if _, ok := ce.commands.Load(tmpId); ok {
			continue
		}

		id = tmpId
	}
	return id
}
