<script setup lang="ts">
import CommandStatueModal from '@/views/home/components/CommandStatusModal.vue'
import * as executor from '@/wailsjs/go/execute/CommandExecutor'
import { ExecutableExists } from '@/wailsjs/go/main/App'
import { store, sysinfo } from '@/wailsjs/go/models'
import * as appManager from '@/wailsjs/go/store/AppSettingManager'
import * as groupManager from '@/wailsjs/go/store/DriverGroupManager'
import * as sysinfoqy from '@/wailsjs/go/sysinfo/SysInfo'
import { onBeforeMount, ref, useTemplateRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'vue-toast-notification'
import type { Command } from './types'

const { t } = useI18n()

const $toast = useToast({ position: 'top-right' })

const statusModal = useTemplateRef('statusModal')

const form = useTemplateRef('form')

const groups = ref<Array<store.DriverGroup>>([])

/** driver ID of drivers that the executable cannot be found */
const notExistDrivers = ref<Array<string>>([])

const settings = ref<store.AppSetting>({
  create_partition: false,
  set_password: false,
  password: '',
  parallel_install: false,
  success_action: store.SuccessAction.NOTHING,
  success_action_delay: 5,
  filter_miniport_nic: true,
  filter_microsoft_nic: true,
  language: 'en'
})

const hwinfos = ref<{
  motherboard: Array<sysinfo.Win32_BaseBoard>
  cpu: Array<sysinfo.Win32_Processor>
  gpu: Array<sysinfo.Win32_VideoController>
  memory: Array<sysinfo.Win32_PhysicalMemory>
  nic: Array<sysinfo.Win32_NetworkAdapter>
  disk: Array<sysinfo.Win32_DiskDrive>
} | null>(null)

onBeforeMount(() => {
  appManager
    .Read()
    .then(s => (settings.value = s))
    .catch(() => {
      $toast.error(t('toasts.readAppSettingFailed'))
    })

  groupManager
    .Read()
    .then(g => {
      groups.value = g

      Promise.all(
        groups.value.flatMap(g =>
          g.drivers.flatMap(d =>
            ExecutableExists(d.path).then(exist => ({ id: g.id, exist: exist }))
          )
        )
      ).then(results => {
        notExistDrivers.value = results
          .map(result => (result.exist ? undefined : result.id))
          .filter(v => v !== undefined)
      })
    })
    .catch(() => {
      $toast.error(t('toasts.readDriverFailed'))
    })

  Promise.all([
    sysinfoqy.MotherboardInfo(),
    sysinfoqy.CpuInfo(),
    sysinfoqy.GpuInfo(),
    sysinfoqy.MemoryInfo(),
    sysinfoqy.NicInfo(),
    sysinfoqy.DiskInfo()
  ]).then(infos => {
    hwinfos.value = ['motherboard', 'cpu', 'gpu', 'memory', 'nic', 'disk'].reduce(
      (obj, key, index) => {
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        obj[key] = infos[index]
        return obj
      },
      {} as typeof hwinfos.value
    )
  })
})

async function handleSubmit() {
  if (!form.value) {
    $toast.error(t('toasts.readInputFailed'))
    return
  }

  const inputs = new FormData(form.value)
  const commands: Array<Command> = []

  if (settings.value.set_password) {
    commands.push({
      id: 'set_password',
      groupName: t('tasks.setPassword'),
      config: {
        program: 'powershell',
        options: [
          '-WindowStyle',
          'Hidden',
          '-Command',
          `Set-LocalUser -Name $Env:UserName -Password ${
            settings.value.password == ''
              ? '(new-object System.Security.SecureString)'
              : `(ConvertTo-SecureString ${settings.value.password} -AsPlainText -Force)`
          }`
        ],
        minExeTime: 0.5,
        allowRtCodes: [0],
        incompatibles: []
      }
    })
  }

  if (settings.value.create_partition) {
    commands.push({
      id: 'create_partition',
      groupName: t('tasks.createPartitions'),
      config: {
        program: 'powershell',
        options: [
          '-WindowStyle',
          'Hidden',
          '-Command',
          'Get-Disk | Where-Object PartitionStyle -Eq "RAW" | Initialize-Disk -PassThru | New-Partition -AssignDriveLetter -UseMaximumSize | Format-Volume'
        ],
        minExeTime: 1,
        allowRtCodes: [0],
        incompatibles: []
      }
    })
  }

  groups.value
    .filter(group =>
      [inputs.get('network'), inputs.get('display'), ...inputs.getAll('miscellaneous')].includes(
        group.id
      )
    )
    .forEach(group => {
      group.drivers.forEach(driver => {
        commands.push({
          id: driver.id,
          name: driver.name,
          groupName: group.name,
          config: {
            program: driver.path,
            options: driver.flags,
            minExeTime: driver.minExeTime,
            allowRtCodes: driver.allowRtCodes,
            incompatibles: driver.incompatibles
          }
        })
      })
    })

  if (commands.length == 0) {
    $toast.warning(t('toasts.noInputWarning'))
    return
  }

  statusModal.value?.show(settings.value.parallel_install, commands)
}
</script>

<template>
  <div class="flex flex-col h-full">
    <div
      id="sysinfo"
      class="flex flex-col grow gap-y-1 min-h-28 overflow-y-auto p-1 border rounded"
      :class="{ loading: hwinfos === null }"
    >
      <template v-if="hwinfos !== null">
        <div>
          <h2 class="text-sm font-bold">{{ $t('motherboard') }}</h2>

          <p v-for="(mb, i) in hwinfos.motherboard" :key="i" class="text-sm">
            {{ `${mb.Manufacturer} ${mb.Product}` }}
          </p>
        </div>

        <div>
          <h2 class="text-sm font-bold">{{ $t('cpu') }}</h2>

          <p v-for="(cpu, i) in hwinfos.cpu" :key="i" class="text-sm">
            {{ cpu.Name }}
          </p>
        </div>

        <div>
          <h2 class="text-sm font-bold">{{ $t('ram') }}</h2>

          <p v-for="(mem, i) in hwinfos.memory" :key="i" class="text-sm">
            {{
              `${mem.Manufacturer} ${mem.PartNumber.trim()} ${mem.Capacity / Math.pow(1024, 3)}GB ${mem.Speed}MHz`
            }}
          </p>
        </div>

        <div>
          <h2 class="text-sm font-bold">{{ $t('gpu') }}</h2>

          <p v-for="(dp, i) in hwinfos.gpu" :key="i" class="text-sm">
            {{ `${dp.Name} (${dp.AdapterRAM / Math.pow(1024, 3)}GB)` }}
          </p>
        </div>

        <div>
          <h2 class="text-sm font-bold">{{ $t('nic') }}</h2>

          <p
            v-for="(dp, i) in hwinfos.nic
              .filter(
                n =>
                  !settings.filter_miniport_nic ||
                  (settings.filter_miniport_nic && !n.Name.includes('Miniport'))
              )
              .filter(
                n =>
                  !settings.filter_microsoft_nic ||
                  (settings.filter_microsoft_nic && !n.Name.includes('Microsoft'))
              )"
            :key="i"
            class="text-sm"
          >
            {{ dp.Name }}
          </p>
        </div>

        <div>
          <h2 class="text-sm font-bold">{{ $t('storage') }}</h2>

          <p v-for="(dp, i) in hwinfos.disk" :key="i" class="text-sm">
            {{ `${dp.Model} (${Math.round(dp.Size / Math.pow(1024, 3))}GB)` }}
          </p>
        </div>
      </template>

      <template v-else>
        <div v-for="i in 6" :key="i">
          <h2 class="h-5 mb-1" :style="{ width: `${Math.random() * (25 - 15) + 15}%` }"></h2>
          <p class="h-5" :style="{ width: `${Math.random() * (85 - 30) + 30}%` }"></p>
        </div>
      </template>
    </div>

    <form class="flex gap-x-3 h-28 mt-3" ref="form">
      <div class="flex flex-col flex-1 justify-between">
        <div class="relative w-full">
          <label
            class="absolute top-0 start-4 h-full translate-y-1 text-xs text-gray-500 pointer-events-none"
          >
            {{ $t('driverCategories.network') }}
          </label>

          <select name="network" class="w-full ps-3 pe-9 pt-5 pb-1 rounded-lg">
            <option>{{ $t('pleaseSelect') }}</option>
            <option
              v-for="d in groups.filter(d => d.type == store.DriverType.NETWORK)"
              :key="d.id"
              :value="d.id"
            >
              {{ `${d.name}${notExistDrivers.includes(d.id) ? ' ⚠' : ''}` }}
            </option>
          </select>
        </div>

        <div class="relative w-full">
          <label
            class="absolute top-0 start-4 h-full translate-y-1 text-xs text-gray-500 pointer-events-none"
          >
            {{ $t('driverCategories.display') }}
          </label>

          <select name="display" class="w-full ps-3 pe-9 pt-5 pb-1 rounded-lg">
            <option>{{ $t('pleaseSelect') }}</option>
            <option
              v-for="d in groups.filter(d => d.type == store.DriverType.DISPLAY)"
              :key="d.id"
              :value="d.id"
            >
              {{ `${d.name}${notExistDrivers.includes(d.id) ? ' ⚠' : ''}` }}
            </option>
          </select>
        </div>
      </div>

      <div class="flex flex-1">
        <div class="relative w-full h-full mb-3">
          <label
            class="absolute left-3 top-1 origin-[0_0] -translate-y-[0.55rem] px-2 bg-white text-xs scale-[0.9] text-gray-500 pointer-events-none"
          >
            {{ $t('driverCategories.miscellaneous') }}
          </label>

          <div class="h-full overflow-y-scroll px-2 pt-3 rounded-lg border border-apple-green-600">
            <template
              v-for="d in groups.filter(d => d.type == store.DriverType.MISCELLANEOUS)"
              :key="d.id"
            >
              <label class="flex items-center w-full select-none cursor-pointer">
                <input type="checkbox" name="miscellaneous" class="me-1.5" :value="d.id" />
                {{ `${d.name}${notExistDrivers.includes(d.id) ? ' ⚠' : ''}` }}
              </label>
            </template>
          </div>
        </div>
      </div>
    </form>

    <hr class="my-3" />

    <div class="flex gap-x-6">
      <div class="flex flex-col">
        <p class="font-semibold">{{ $t('installOptions.title') }}</p>

        <div class="flex flex-col flex-1 justify-around">
          <div class="flex items-center gap-x-4">
            <label class="select-none cursor-pointer">
              <input
                type="checkbox"
                name="create_partition"
                v-model="settings.create_partition"
                class="me-1"
              />
              {{ $t('installOptions.createPartition') }}
            </label>

            <label class="select-none cursor-pointer">
              <input
                type="checkbox"
                name="parallel_install"
                v-model="settings.parallel_install"
                class="me-1"
              />
              {{ $t('installOptions.parallelInstall') }}
            </label>
          </div>

          <div class="flex items-center gap-x-2">
            <label class="select-none cursor-pointer">
              <input
                type="checkbox"
                name="set_password"
                v-model="settings.set_password"
                class="me-1"
              />
              {{ $t('installOptions.setPassword') }}
            </label>

            <input
              type="text"
              name="password"
              v-model="settings.password"
              class="max-w-28 p-1.5 text-xs shadow-sm"
              :disabled="!settings.set_password"
            />
          </div>
        </div>
      </div>

      <div class="flex flex-col grow justify-between">
        <div>
          <label class="block mb-1 text-sm text-gray-900">
            {{ $t('installOptions.successAction') }}
          </label>

          <select
            name="success_action"
            v-model="settings.success_action"
            class="w-full p-1 text-sm text-gray-900"
          >
            <option v-for="action in store.SuccessAction" :key="action" :value="action">
              {{ $t(`successActions.${action}`) }}
            </option>
          </select>
        </div>

        <div class="flex flex-row gap-x-3 justify-end items-center mt-2">
          <button
            type="button"
            class="px-3 py-1.5 text-white text-sm bg-rose-700 hover:bg-rose-600 rounded"
            @click="
              () => {
                $refs.form.reset()
                appManager.Read().then(s => (settings = s))
              }
            "
          >
            {{ $t('installOptions.reset') }}
          </button>
          <button
            class="px-3 py-1.5 text-white text-sm bg-half-baked-600 hover:bg-half-baked-500 rounded"
            @click="handleSubmit"
          >
            {{ $t('installOptions.execute') }}
          </button>
        </div>
      </div>
    </div>
  </div>

  <CommandStatueModal
    ref="statusModal"
    @completed="
      () => {
        switch (settings.success_action) {
          case store.SuccessAction.SHUTDOWN:
            executor.RunAndOutput('cmd', ['/C', `shutdown /s /t ${settings.success_action_delay}`])
            break
          case store.SuccessAction.REBOOT:
            executor.RunAndOutput('cmd', ['/C', `shutdown /r /t ${settings.success_action_delay}`])
            break
          case store.SuccessAction.FIRMWARE:
            executor
              .RunAndOutput('cmd', ['/C', `shutdown /r /fw /t ${settings.success_action_delay}`])
              .then(result => {
                if (result.exitCode != 0) {
                  // sometimes, /fw would resulted in an error: 'The system could not find the environment option that was entered. (203)'
                  // execute again normally solve the error
                  executor.RunAndOutput('cmd', [
                    '/C',
                    `shutdown /r /fw /t ${settings.success_action_delay}`
                  ])
                }
              })
            break
        }
      }
    "
  ></CommandStatueModal>
</template>

<style scoped>
#sysinfo.loading {
  h2,
  p {
    background-color: #e2e2e2;
    animation: skeleton 1.5s infinite;
  }
}

@keyframes skeleton {
  0%,
  100% {
    opacity: 0.5;
  }
  50% {
    opacity: 0.2;
  }
}
</style>
