package store

import (
	"encoding/json"
	"os"
)

type AppSettingManager struct {
	Path    string
	loaded  bool
	setting AppSetting
}

func (s *AppSettingManager) Read() (AppSetting, error) {
	if !s.loaded {
		var setting AppSetting

		if _, err := os.Stat(s.Path); err != nil {
			s.Update(AppSetting{SuccessAction: Nothing})
		}

		bytes, err := os.ReadFile(s.Path)
		if err != nil {
			return AppSetting{}, err
		}

		if err := json.Unmarshal(bytes, &setting); err != nil {
			return AppSetting{}, err
		}

		if setting.SuccessAction == "" {
			setting.SuccessAction = Nothing
		}

		s.setting = setting
	}
	s.loaded = true
	return s.setting, nil
}

func (s *AppSettingManager) Update(setting AppSetting) error {
	s.setting = setting

	bytes, err := json.Marshal(s.setting)
	if err != nil {
		return err
	}
	return os.WriteFile(s.Path, bytes, os.ModePerm)
}

type AppSetting struct {
	CreatePartition bool          `json:"create_partition"`
	SetPassword     bool          `json:"set_password"`
	Password        string        `json:"password"`
	ParallelInstall bool          `json:"parallel_install"`
	SuccessAction   SuccessAction `json:"success_action"`
}

type SuccessAction string

const (
	Nothing  SuccessAction = "nothing"
	Shutdown SuccessAction = "shutdown"
	Reboot   SuccessAction = "reboot"
	Firmware SuccessAction = "firmware"
)
