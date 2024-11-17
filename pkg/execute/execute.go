package execute

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"

	"github.com/puzpuzpuz/xsync/v3"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

type CommandExecutor struct {
	ctx      context.Context
	commands *xsync.MapOf[string, *commandWrapper]
}

func (ce *CommandExecutor) SetContext(ctx context.Context) {
	ce.ctx = ctx
	ce.commands = xsync.NewMapOf[string, *commandWrapper]()
}

func (ce *CommandExecutor) Run(program string, options []string) string {
	id := ce.generateId()
	ce.commands.Store(id, newCommandWrapper(program, options))

	go ce.dispatch(id)

	return id
}

func (ce *CommandExecutor) RunAndOutput(program string, options []string) CommandResult {
	var (
		errMsg  string
		command = newCommandWrapper(program, options)
	)

	if err := command.Run(); err != nil {
		errMsg = err.Error()
	}

	return CommandResult{
		command.Lapse(),
		command.cmd.ProcessState.ExitCode(),
		command.stdout.String(),
		command.stderr.String(),
		errMsg,
		command.aborted,
	}
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
		var errMsg string
		if err := command.Run(); err != nil {
			errMsg = err.Error()
		}

		runtime.EventsEmit(ce.ctx, "execute:exited", id, CommandResult{
			command.Lapse(),
			command.cmd.ProcessState.ExitCode(),
			command.stdout.String(),
			command.stderr.String(),
			errMsg,
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
