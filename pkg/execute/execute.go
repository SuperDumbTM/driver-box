package execute

import (
	"crypto/rand"
	"encoding/hex"
	"errors"
)

type CommandExecutor struct {
	commands map[string]*Command
}

func (m *CommandExecutor) Add(t Command) string {
	if m.commands == nil {
		m.commands = make(map[string]*Command)
	}

	cmdId := ""
	for cmdId == "" {
		b := make([]byte, 4)
		if _, err := rand.Read(b); err != nil {
			continue
		}

		id := hex.EncodeToString(b)
		if _, ok := m.commands[id]; ok {
			continue
		}
		cmdId = id
	}

	m.commands[cmdId] = &t
	return cmdId
}

// func (m *CommandExecutor) Commands() []*Command {
// 	return m.tasks
// }

func (m *CommandExecutor) Start(id string) error {
	if task, ok := m.commands[id]; !ok {
		return errors.New("execute: id not found")
	} else {
		task.Start()
		return nil
	}
}

func (m *CommandExecutor) Abort(id string) error {
	if task, ok := m.commands[id]; !ok {
		return errors.New("execute: id not found")
	} else {
		task.Stop()
		return nil
	}
}

func (m *CommandExecutor) Status(id string) (string, error) {
	if task, ok := m.commands[id]; !ok {
		return "", errors.New("execute: id not found")
	} else {
		if task.cmd.ProcessState == nil {
			return "nil", nil
		}
		return id + " " + task.cmd.ProcessState.String(), nil
	}
}
