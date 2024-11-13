<script setup lang="ts">
import * as manager from '@/wailsjs/go/store/DriverManager'
import * as app_manager from '@/wailsjs/go/store/AppSettingManager'
import { store, sysinfo } from '@/wailsjs/go/models'
import { ref, useTemplateRef } from 'vue'
import * as sysinfoqy from '@/wailsjs/go/sysinfo/SysInfo'
import CommandStatueModal from '@/components/home_view/CommandStatusModal.vue'
import { RunCommand } from '@/wailsjs/go/main/App'
import { useToast } from 'vue-toast-notification'

const statusModal = useTemplateRef('statusModal')

const form = useTemplateRef('form')

const $toast = useToast({ position: 'top-right' })

const drivers = ref<Array<store.Driver>>([])

const settings = ref<store.AppSetting>({
  create_partition: false,
  set_password: false,
  password: '',
  parallel_install: false,
  success_action: store.SuccessAction.NOTHING
})

const hwinfos = ref<{
  motherboard: Array<sysinfo.Win32_BaseBoard>
  cpu: Array<sysinfo.Win32_Processor>
  gpu: Array<sysinfo.Win32_VideoController>
  memory: Array<sysinfo.Win32_PhysicalMemory>
  nic: Array<sysinfo.Win32_NetworkAdapter>
  disk: Array<sysinfo.Win32_DiskDrive>
} | null>(null)

manager
  .Read()
  .then(d => (drivers.value = d))
  .catch(() => {
    $toast.error('無法讀取軀動資料')
  })

app_manager
  .Read()
  .then(s => (settings.value = s))
  .catch(() => {
    $toast.error('無法讀預設選項資料')
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

async function handleSubmit() {
  if (!form.value) {
    $toast.error('無法出得輸入')
    return
  }

  const inputs = new FormData(form.value)
  const commands: Array<{
    id: string
    name: string
    program: string
    options: Array<string>
    minExeTime: number
    allowRtCodes: Array<number>
    incompatibles: Array<string>
  }> = []

  if (settings.value.set_password) {
    commands.push({
      id: 'set_password',
      name: '設定密碼',
      program: 'powershell',
      options: [
        'Set-LocalUser',
        (await RunCommand('powershell', ['$Env:UserName'])).trim(),
        '-Password',
        settings.value.parallel_install.toString().length > 0
          ? `ConverTo-SecureString ${settings.value.parallel_install} -AsPlainText -Force")`
          : '(new-object System.Security.SecureString)'
      ],
      minExeTime: 1,
      allowRtCodes: [0],
      incompatibles: []
    })
  }

  if (settings.value.create_partition) {
    commands.push({
      id: 'create_partition',
      name: '建立磁碟分區及掛載檔案系統',
      program: 'powershell',
      options: [
        'Get-Disk | Where-Object PartitionStyle -Eq "RAW" | Initialize-Disk -PassThru | New-Partition -AssignDriveLetter -UseMaximumSize | Format-Volume'
      ],
      minExeTime: 1,
      allowRtCodes: [0],
      incompatibles: []
    })
  }

  drivers.value
    .filter(dri =>
      [inputs.get('network'), inputs.get('display'), ...inputs.getAll('miscellaneous')].includes(
        dri.id
      )
    )
    .forEach(dri => {
      commands.push({
        id: dri.id,
        name: dri.name,
        program: dri.path,
        options: dri.flags,
        minExeTime: dri.minExeTime,
        allowRtCodes: dri.allowRtCodes,
        incompatibles: dri.incompatibles
      })
    })

  if (commands.length == 0) {
    $toast.warning('請先選擇軀動或工作')
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
          <h2 class="text-sm font-bold">底板</h2>

          <p v-for="(mb, i) in hwinfos.motherboard" :key="i" class="text-sm">
            {{ `${mb.Manufacturer} ${mb.Product}` }}
          </p>
        </div>

        <div>
          <h2 class="text-sm font-bold">中央處理器</h2>

          <p v-for="(cpu, i) in hwinfos.cpu" :key="i" class="text-sm">
            {{ cpu.Name }}
          </p>
        </div>

        <div>
          <h2 class="text-sm font-bold">記憶體</h2>

          <p v-for="(mem, i) in hwinfos.memory" :key="i" class="text-sm">
            {{
              `${mem.Manufacturer} ${mem.PartNumber}  ${mem.Capacity / Math.pow(1024, 3)}GB ${mem.Speed}MHz`
            }}
          </p>
        </div>

        <div>
          <h2 class="text-sm font-bold">顯示卡</h2>

          <p v-for="(dp, i) in hwinfos.gpu" :key="i" class="text-sm">
            {{ `${dp.Name} (${dp.AdapterRAM / Math.pow(1024, 3)}GB)` }}
          </p>
        </div>

        <div>
          <h2 class="text-sm font-bold">網絡介面卡</h2>

          <p v-for="(dp, i) in hwinfos.nic" :key="i" class="text-sm">
            {{ dp.Name }}
          </p>
        </div>

        <div>
          <h2 class="font-bold">儲存裝置</h2>

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

    <hr class="my-3" />

    <form class="flex gap-x-3 h-28" ref="form">
      <div class="flex flex-col flex-1 gap-y-3 justify-around">
        <div class="relative w-full">
          <select
            name="network"
            class="block w-full peer ps-3 pe-9 pt-4 pb-1 border-2 border-gray-200 rounded-lg focus:border-powder-blue-900"
          >
            <option>請選擇</option>
            <option
              v-for="d in drivers.filter(d => d.type == store.DriverType.NETWORK)"
              :key="d.id"
              :value="d.id"
            >
              {{ d.name }}
            </option>
          </select>
          <label
            class="absolute top-0 start-0 h-full p-4 pt-2.5 -translate-y-1.5 text-xs truncate text-gray-500 pointer-events-none"
          >
            網絡介面卡
          </label>
        </div>

        <div class="relative w-full">
          <select
            name="display"
            class="block w-full peer ps-3 pe-9 pt-4 pb-1 border-2 border-gray-200 rounded-lg focus:border-powder-blue-900"
          >
            <option>請選擇</option>
            <option
              v-for="d in drivers.filter(d => d.type == store.DriverType.DISPLAY)"
              :key="d.id"
              :value="d.id"
            >
              {{ d.name }}
            </option>
          </select>
          <label
            class="absolute top-0 start-0 h-full p-4 pt-2.5 -translate-y-1.5 text-xs truncate text-gray-500 pointer-events-none"
          >
            顯示卡
          </label>
        </div>
      </div>

      <div class="flex flex-1">
        <div class="relative w-full h-full mb-3">
          <div class="h-full overflow-y-scroll ps-2 pt-3 rounded border">
            <template
              v-for="d in drivers.filter(d => d.type == store.DriverType.MISCELLANEOUS)"
              :key="d.id"
            >
              <!-- <label class="ms-2 text-sm text-gray-900"> -->
              <label class="flex items-center w-full my-1 select-none cursor-pointer">
                <input type="checkbox" name="miscellaneous" class="me-1.5" :value="d.id" />
                {{ d.name }}
              </label>
            </template>
          </div>
          <label
            class="absolute left-3 top-0 w-10 origin-[0_0] -translate-y-[0.55rem] bg-white text-primary scale-[0.9] text-center text-neutral-500 truncate pointer-events-none"
          >
            其他
          </label>
        </div>
      </div>
    </form>

    <hr class="my-3" />

    <div class="flex gap-x-6">
      <div class="flex flex-col">
        <fieldset>
          <p class="font-bold">額外工作</p>

          <div class="flex gap-x-3">
            <div class="flex items-center mb-4">
              <label class="flex item-center w-full select-none cursor-pointer">
                <input
                  type="checkbox"
                  name="create_partition"
                  v-model="settings.create_partition"
                  class="me-1.5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                />
                建立磁區
              </label>
            </div>

            <div class="flex items-center mb-4">
              <label class="flex item-center w-full select-none cursor-pointer">
                <input
                  type="checkbox"
                  name="set_password"
                  v-model="settings.set_password"
                  class="me-1.5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                />
                設定密碼
              </label>
            </div>
          </div>
        </fieldset>

        <fieldset>
          <p class="font-bold">安裝設定</p>

          <div class="flex gap-x-3">
            <div class="flex items-center mb-4">
              <!-- <label class="ms-2 text-sm"> -->
              <label class="flex item-center w-full select-none cursor-pointer">
                <input
                  type="checkbox"
                  name="parallel_install"
                  v-model="settings.parallel_install"
                  class="me-1.5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                />
                同步安裝
              </label>
            </div>
          </div>
        </fieldset>
      </div>

      <div class="flex flex-col grow justify-between">
        <fieldset class="w-full">
          <label class="block mb-1 text-sm font-bold text-gray-900">關機設定</label>
          <select
            name="success_action"
            v-model="settings.success_action"
            class="block w-full p-1 text-sm text-gray-900 border border-gray-300 rounded-lg"
          >
            <option :value="store.SuccessAction.NOTHING">沒有動作</option>
            <option :value="store.SuccessAction.SHUTDOWN">關機</option>
            <option :value="store.SuccessAction.REBOOT">重新開機</option>
            <option :value="store.SuccessAction.FIRMWARE">進入 BIOS/UEFI</option>
          </select>
        </fieldset>

        <div class="flex flex-row gap-x-2 justify-end items-center">
          <button
            type="button"
            class="h-8 px-3 text-white text-sm bg-rose-700 hover:bg-rose-600 rounded"
            @click="
              () => {
                $refs.form.reset()
                app_manager.Read().then(s => (settings = s))
              }
            "
          >
            重置輸入
          </button>
          <button
            class="h-8 px-3 text-white text-sm focus:outline-none bg-half-baked-600 hover:bg-half-baked-500 rounded"
            @click="handleSubmit"
          >
            執行
          </button>
        </div>
      </div>
    </div>
  </div>

  <CommandStatueModal
    ref="statusModal"
    @completed="
      () => {
        $toast.success('完成。', { duration: 5000 })

        switch (settings.success_action) {
          case store.SuccessAction.SHUTDOWN:
            RunCommand('cmd', ['/C', 'shutdown /s /t 5'])
          case store.SuccessAction.REBOOT:
            RunCommand('cmd', ['/C', 'shutdown /r /t 5'])
          case store.SuccessAction.FIRMWARE:
            RunCommand('cmd', ['/C', 'shutdown /r /fw /t 5'])
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
