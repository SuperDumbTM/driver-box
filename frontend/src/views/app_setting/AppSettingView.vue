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
  success_action_delay: 5,
  filter_miniport_nic: true,
  filter_microsoft_nic: true,
  language: 'en'
})

app_manager.Read().then(s => (settings.value = s))
</script>

<template>
  <form
    class="flex flex-col h-full gap-y-3 overflow-y-auto"
    @submit.prevent="
      () => {
        app_manager.Update(settings).then(() => {
          $i18n.locale = settings.language
          $toast.success($t('toasts.updated'), { duration: 1500, position: 'top-right' })
        })
      }
    "
  >
    <div>
      <p class="mb-1 text-lg text-kashmir-blue-400 font-bold">
        {{ $t('settings.generalSetting') }}
      </p>
      <hr />
    </div>

    <div>
      <p class="font-bold mb-2">
        {{ $t('settings.softwareSetting') }}
      </p>

      <div>
        <label class="block mb-2 text-gray-900">
          {{ $t('settings.language') }}
        </label>
        <select
          name="language"
          v-model="settings.language"
          class="w-full max-w-72 min-w-24 p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
        >
          <option value="en">English</option>
          <option value="zh_Hant_HK">繁體中文</option>
        </select>
      </div>
    </div>

    <div>
      <p class="font-bold mb-2">
        {{ $t('settings.successActionDelay') }}
      </p>

      <div class="flex flex-col gap-y-3">
        <div class="flex items-center">
          <input
            type="number"
            name="success_action_delay"
            min="0"
            step="0"
            v-model="settings.success_action_delay"
            class="w-20 p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
            required
          />
          &nbsp; {{ $t('settings.second') }}
        </div>
      </div>
    </div>

    <div>
      <p class="mb-1 text-lg text-kashmir-blue-400 font-bold">
        {{ $t('settings.defaultInstallSetting') }}
      </p>
      <hr />
    </div>

    <div>
      <p class="font-bold mb-2">
        {{ $t('settings.task') }}
      </p>

      <div class="flex flex-col gap-y-3">
        <div class="flex items-center">
          <label class="flex item-center w-full select-none cursor-pointer">
            <input
              type="checkbox"
              name="create_partition"
              v-model="settings.create_partition"
              class="me-1.5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            />
            {{ $t('installOptions.createPartition') }}
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
              {{ $t('installOptions.setPassword') }}
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
      <p class="font-bold mb-2">
        {{ $t('settings.installOption') }}
      </p>

      <div class="flex flex-col gap-y-3">
        <div class="flex items-center">
          <label class="flex item-center w-full select-none cursor-pointer">
            <input
              type="checkbox"
              name="parallel_install"
              v-model="settings.parallel_install"
              class="me-1.5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            />
            {{ $t('installOptions.parallelInstall') }}
          </label>
        </div>

        <div>
          <label class="block mb-2 text-gray-900">
            {{ $t('installOptions.successAction') }}
          </label>
          <select
            name="success_action"
            v-model="settings.success_action"
            class="w-full max-w-72 min-w-24 p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
          >
            <option v-for="action in store.SuccessAction" :key="action" :value="action">
              {{ $t(`successActions.${action}`) }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <div>
      <p class="mb-1 text-lg text-kashmir-blue-400 font-bold">
        {{ $t('settings.displaySetting') }}
      </p>
      <hr />
    </div>

    <div>
      <p class="font-bold mb-2">
        {{ $t('settings.hardwareInfo') }}
      </p>

      <div class="flex flex-col gap-y-3">
        <div class="flex items-center">
          <label class="flex item-center w-full select-none cursor-pointer">
            <input
              type="checkbox"
              name="filter_miniport_nic"
              v-model="settings.filter_miniport_nic"
              class="me-1.5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            />
            {{ $t('settings.filterMiniportNic') }}
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
            {{ $t('settings.filterMicorsoftNic') }}
          </label>
        </div>
      </div>
    </div>

    <div class="sticky bottom-0 bg-white shadow-lg shadow-black bg-scroll">
      <button
        type="submit"
        class="h-7 mt-3 px-3 text-white text-sm bg-half-baked-600 hover:bg-half-baked-500 rounded"
      >
        {{ $t('save') }}
      </button>
    </div>
  </form>
</template>
