package store

import (
	"encoding/json"
	"errors"
	"os"
	"os/exec"
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

func (m DriverGroupManager) IndexOf(groupId string) (int, error) {
	index := slices.IndexFunc(m.groups, func(g DriverGroup) bool {
		return g.Id == groupId
	})

	if index == -1 {
		return -1, errors.New("store: no group with the same ID was found")
	}
	return index, nil
}

func (m DriverGroupManager) GroupOf(driverId string) (string, error) {
	for _, group := range m.groups {
		for _, driver := range group.Drivers {
			if driver.Id == driverId {
				return group.Id, nil
			}
		}
	}
	return "", errors.New("store: no driver with the same ID was found in any group")
}

func (m *DriverGroupManager) Get(id string) (DriverGroup, error) {
	if index, err := m.IndexOf(id); err != nil {
		return DriverGroup{}, err
	} else {
		return m.groups[index], nil
	}
}

func (m *DriverGroupManager) Add(group DriverGroup) error {
	for group.Id = ""; group.Id == ""; {
		if id, err := randomString(4); err != nil {
			continue
		} else if idx, _ := m.IndexOf(id); idx != -1 {
			continue
		} else {
			group.Id = id
		}
	}

	for gidx := range group.Drivers {
		for group.Drivers[gidx].Id = ""; group.Drivers[gidx].Id == ""; {
			if id, err := randomString(4); err != nil {
				continue
			} else if _, err := m.GroupOf(id); err == nil {
				continue
			} else {
				group.Drivers[gidx].Id = id
			}
		}
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
		// for _, group := range m.groups {
		// 	for _, driver := range group.Drivers {

		// 	}
		// }
		m.groups = append(m.groups[:index], m.groups[index+1:]...)
		return m.write()
	}
}

func (m DriverGroupManager) PathExist(groupId string, driverId string) (bool, error) {
	if index, err := m.IndexOf(groupId); err != nil {
		return false, err
	} else {
		for _, driver := range m.groups[index].Drivers {
			if driver.Id != driverId {
				continue
			}
			_, err = exec.LookPath(driver.Path)
			return err == nil, nil
		}
		return false, errors.New("store: no driver with the same driver_id was found")
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

type DriverType string

const (
	Network       DriverType = "network"
	Display       DriverType = "display"
	Miscellaneous DriverType = "miscellaneous"
)

type Driver struct {
	Id            string     `json:"id"`
	Name          string     `json:"name"`
	Type          DriverType `json:"type"`
	Path          string     `json:"path"`
	Flags         []string   `json:"flags"`
	MinExeTime    float32    `json:"minExeTime"`
	AllowRtCodes  []int32    `json:"allowRtCodes"`
	Incompatibles []string   `json:"incompatibles"`
}
