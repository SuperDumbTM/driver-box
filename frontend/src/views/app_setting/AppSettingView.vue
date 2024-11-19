<script setup lang="ts">
import { store } from '@/wailsjs/go/models'
import * as app_manager from '@/wailsjs/go/store/AppSettingManager'
import { ref } from 'vue'

const settings = ref<store.AppSetting>({
  create_partition: false,
  set_password: false,
  password: '',
  parallel_install: false,
  success_action: store.SuccessAction.NOTHING,
  filter_miniport_nic: true,
  filter_microsoft_nic: true
})

app_manager.Read().then(s => {
  settings.value = s
})
</script>

<template>
  <form
    class="flex flex-col h-full gap-y-3"
    @submit.prevent="
      () => {
        app_manager.Update(settings).then(() => {
          $toast.success('已更新。', { duration: 1500, position: 'top-right' })
        })
      }
    "
  >
    <div>
      <p class="mb-1 text-lg text-kashmir-blue-400 font-bold">預設安裝選項</p>
      <hr />
    </div>

    <div>
      <p class="font-bold mb-2">額外工作</p>

      <div class="flex flex-col gap-y-3">
        <div class="flex items-center">
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

        <div class="flex gap-3">
          <div class="flex items-center">
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

          <div class="flex shrink">
            <input
              type="text"
              name="password"
              v-model="settings.password"
              class="w-full min-w-20 p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
              :disabled="!settings.set_password"
            />
          </div>
        </div>
      </div>
    </div>

    <div>
      <p class="font-bold mb-2">安裝設定</p>

      <div class="flex flex-col gap-y-3">
        <div class="flex items-center">
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

        <div>
          <label class="block mb-2 text-gray-900"> 關機設定 </label>
          <select
            name="success_action"
            v-model="settings.success_action"
            class="w-full max-w-72 min-w-24 p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
          >
            <option :value="store.SuccessAction.NOTHING">沒有動作</option>
            <option :value="store.SuccessAction.SHUTDOWN">關機</option>
            <option :value="store.SuccessAction.REBOOT">重新開機</option>
            <option :value="store.SuccessAction.FIRMWARE">進入 BIOS/UEFI</option>
          </select>
        </div>
      </div>
    </div>

    <div>
      <p class="mb-1 text-lg text-kashmir-blue-400 font-bold">顯示設定</p>
      <hr />
    </div>

    <div>
      <p class="font-bold mb-2">硬件資訊</p>

      <div class="flex flex-col gap-y-3">
        <div class="flex items-center">
          <label class="flex item-center w-full select-none cursor-pointer">
            <input
              type="checkbox"
              name="filter_miniport_nic"
              v-model="settings.filter_miniport_nic"
              class="me-1.5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            />
            過濾 Miniport 網卡
          </label>
        </div>
      </div>

      <div class="flex flex-col gap-y-3">
        <div class="flex items-center">
          <label class="flex item-center w-full select-none cursor-pointer">
            <input
              type="checkbox"
              name="filter_microsoft_nic"
              v-model="settings.filter_microsoft_nic"
              class="me-1.5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            />
            過濾 Microsoft 網卡
          </label>
        </div>
      </div>
    </div>

    <div>
      <button
        type="submit"
        class="h-8 mt-3 px-3 text-white text-sm focus:outline-none bg-half-baked-600 hover:bg-half-baked-500 rounded"
      >
        儲存
      </button>
    </div>
  </form>
</template>
