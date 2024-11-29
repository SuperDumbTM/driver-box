package store

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"errors"
	"os"
	"slices"
)

type DriverGroupManager struct {
	Path   string
	loaded bool
	groups []DriverGroup
}

func (m *DriverGroupManager) Read() ([]DriverGroup, error) {
	if !m.loaded {
		var groups []DriverGroup

		if _, err := os.Stat(m.Path); err != nil {
			os.WriteFile(m.Path, []byte("[]"), os.ModePerm)
		}

		bytes, err := os.ReadFile(m.Path)
		if err != nil {
			return nil, err
		}

		if err := json.Unmarshal(bytes, &groups); err != nil {
			return nil, err
		}

		m.groups = groups
		m.loaded = true
	}
	return m.groups, nil
}

func (m DriverGroupManager) write() error {
	bytes, err := json.Marshal(m.groups)
	if err != nil {
		return err
	}

	return os.WriteFile(m.Path, bytes, os.ModePerm)
}

func (m DriverGroupManager) IndexOf(id string) (int, error) {
	index := slices.IndexFunc(m.groups, func(s DriverGroup) bool {
		return s.Id == id
	})

	if index == -1 {
		return -1, errors.New("store: no group with the same ID was found")
	}
	return index, nil
}

func (m *DriverGroupManager) Get(id string) (DriverGroup, error) {
	if index, err := m.IndexOf(id); err != nil {
		return DriverGroup{}, err
	} else {
		return m.groups[index], nil
	}
}

func (m *DriverGroupManager) Add(group DriverGroup) error {
	group.Id = ""
	for group.Id == "" {
		b := make([]byte, 4)
		if _, err := rand.Read(b); err != nil {
			continue
		}
		id := hex.EncodeToString(b)
		if idx, _ := m.IndexOf(id); idx != -1 {
			continue
		}
		group.Id = id
	}
	m.groups = append(m.groups, group)
	return m.write()
}

func (m *DriverGroupManager) Update(group DriverGroup) error {
	if index, err := m.IndexOf(group.Id); err != nil {
		return err
	} else {
		m.groups[index] = group
		return m.write()
	}
}

func (m *DriverGroupManager) Remove(id string) error {
	if index, err := m.IndexOf(id); err != nil {
		return err
	} else {
		m.groups = append(m.groups[:index], m.groups[index+1:]...)
		return m.write()
	}
}

func (m *DriverGroupManager) MoveBehind(id string, index int) ([]DriverGroup, error) {
	if srcIndex, err := m.IndexOf(id); err != nil {
		return m.groups, err
	} else {
		if index < -1 || index >= len(m.groups)-1 {
			return m.groups, errors.New("store: target index out of bound")
		}

		if len(m.groups) == 1 || srcIndex-index == 1 {
			return m.groups, nil
		}

		if srcIndex <= index {
			for i := srcIndex; i < index+1; i++ {
				m.groups[i], m.groups[i+1] = m.groups[i+1], m.groups[i]
			}
		} else {
			for i := srcIndex; i > index+1; i-- {
				m.groups[i-1], m.groups[i] = m.groups[i], m.groups[i-1]
			}
		}

		return m.groups, m.write()
	}

}

type DriverGroup struct {
	Id      string     `json:"id"`
	Name    string     `json:"name"`
	Type    DriverType `json:"type"`
	Drivers []Driver   `json:"drivers"`
}
