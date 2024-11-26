package store

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"errors"
	"os"
	"os/exec"
	"slices"
)

type DriverManager struct {
	Path    string
	loaded  bool
	drivers []Driver
}

func (m *DriverManager) Read() ([]Driver, error) {
	if !m.loaded {
		var drivers []Driver

		if _, err := os.Stat(m.Path); err != nil {
			os.WriteFile(m.Path, []byte("[]"), os.ModePerm)
		}

		bytes, err := os.ReadFile(m.Path)
		if err != nil {
			return nil, err
		}

		if err := json.Unmarshal(bytes, &drivers); err != nil {
			return nil, err
		}

		m.drivers = drivers
		m.loaded = true
	}
	return m.drivers, nil
}

func (m DriverManager) write() error {
	bytes, err := json.Marshal(m.drivers)
	if err != nil {
		return err
	}

	return os.WriteFile(m.Path, bytes, os.ModePerm)
}

func (m DriverManager) IndexOf(id string) (int, error) {
	index := slices.IndexFunc(m.drivers, func(s Driver) bool {
		return s.Id == id
	})

	if index == -1 {
		return -1, errors.New("store: no driver with the same ID was found")
	}
	return index, nil
}

func (m *DriverManager) Get(id string) (Driver, error) {
	if index, err := m.IndexOf(id); err != nil {
		return Driver{}, err
	} else {
		return m.drivers[index], nil
	}
}

func (m *DriverManager) Add(driver Driver) error {
	driver.Id = ""
	for driver.Id == "" {
		b := make([]byte, 4)
		if _, err := rand.Read(b); err != nil {
			continue // inf loop?
		}
		id := hex.EncodeToString(b)
		if idx, _ := m.IndexOf(id); idx != -1 {
			continue
		}
		driver.Id = id
	}
	m.drivers = append(m.drivers, driver)
	return m.write()
}

func (m *DriverManager) Update(driver Driver) error {
	if index, err := m.IndexOf(driver.Id); err != nil {
		return err
	} else {
		m.drivers[index] = driver
		return m.write()
	}
}

func (m *DriverManager) Remove(driver Driver) error {
	if index, err := m.IndexOf(driver.Id); err != nil {
		return err
	} else {
		m.drivers = append(m.drivers[:index], m.drivers[index+1:]...)

		for i := range m.drivers {
			incompatibles := []string{}
			for _, id := range m.drivers[i].Incompatibles {
				if id == driver.Id {
					continue
				}
				incompatibles = append(incompatibles, id)
			}
			m.drivers[i].Incompatibles = incompatibles
		}

		return m.write()
	}
}

func (m DriverManager) PathExist(id string) (bool, error) {
	if index, err := m.IndexOf(id); err != nil {
		return false, err
	} else {
		_, err = exec.LookPath(m.drivers[index].Path)
		return err == nil, nil
	}
}

func (m *DriverManager) MoveBehind(id string, index int) ([]Driver, error) {
	if srcIndex, err := m.IndexOf(id); err != nil {
		return m.drivers, err
	} else {
		if index < -1 || index >= len(m.drivers)-1 {
			return m.drivers, errors.New("store: target index out of bound")
		}

		if len(m.drivers) == 1 || srcIndex-index == 1 {
			return m.drivers, nil
		}

		if srcIndex <= index {
			for i := srcIndex; i < index+1; i++ {
				m.drivers[i], m.drivers[i+1] = m.drivers[i+1], m.drivers[i]
			}
		} else {
			for i := srcIndex; i > index+1; i-- {
				m.drivers[i-1], m.drivers[i] = m.drivers[i], m.drivers[i-1]
			}
		}

		return m.drivers, m.write()
	}

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
