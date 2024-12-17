<script setup lang="ts">
import { store } from '@/wailsjs/go/models'
import * as appManager from '@/wailsjs/go/store/AppSettingManager'
import { onBeforeMount, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'vue-toast-notification'

const { t } = useI18n()

const $toast = useToast({ position: 'top-right' })

const tabKeys = ['softwareSetting', 'defaultInstallSetting', 'displaySetting'] as const

const currentTab = ref<(typeof tabKeys)[number]>(tabKeys[0])

const settings = ref<store.AppSetting>(new store.AppSetting())

onBeforeMount(() => {
  appManager
    .Read()
    .then(s => (settings.value = s))
    .catch(() => {
      $toast.error(t('toasts.readAppSettingFailed'))
    })
})
</script>

<template>
  <form
    class="flex flex-col h-full gap-y-3"
    @submit.prevent="
      () => {
        appManager.Update(settings).then(() => {
          $i18n.locale = settings.language
          $toast.success($t('toasts.updated'), { duration: 1500, position: 'top-right' })
        })
      }
    "
  >
    <div class="flex items-center border-b-2">
      <button
        v-for="key in tabKeys"
        :key="key"
        type="button"
        class="px-4 py-2"
        :class="
          currentTab == key ? 'font-semibold border-b-2 border-b-kashmir-blue-500 -mb-[2px]' : ''
        "
        @click="currentTab = key"
      >
        {{ $t(`settings.${key}`) }}
      </button>
    </div>

    <div v-show="currentTab == 'softwareSetting'" class="flex flex-col gap-y-3">
      <section>
        <p class="font-bold mb-2">
          {{ $t('settings.softwareSetting') }}
        </p>

        <div class="flex flex-col gap-y-3">
          <div>
            <label class="block mb-2 text-gray-900">
              {{ $t('settings.language') }}
            </label>
            <select
              name="language"
              v-model="settings.language"
              class="w-full max-w-72 min-w-24 p-1.5 text-sm shadow-sm"
            >
              <option value="en">English</option>
              <option value="zh_Hant_HK">繁體中文</option>
            </select>
          </div>
        </div>
      </section>

      <section>
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
              class="w-20 p-1.5 text-sm shadow-sm"
              required
            />
            &nbsp; {{ $t('settings.second') }}
          </div>
        </div>
      </section>
    </div>

    <div v-show="currentTab == 'defaultInstallSetting'" class="flex flex-col gap-y-3">
      <section>
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
                class="w-full min-w-20 p-1.5 text-sm shadow-sm"
                :disabled="!settings.set_password"
              />
            </div>
          </div>
        </div>
      </section>

      <section>
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
              class="w-full max-w-72 min-w-24 p-1.5 text-sm shadow-sm"
            >
              <option v-for="action in store.SuccessAction" :key="action" :value="action">
                {{ $t(`successActions.${action}`) }}
              </option>
            </select>
          </div>
        </div>
      </section>
    </div>

    <div v-show="currentTab == 'displaySetting'" class="flex flex-col gap-y-3">
      <section>
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
      </section>
    </div>

    <div>
      <button
        type="submit"
        class="h-8 mt-3 px-3 text-white text-sm bg-half-baked-600 hover:bg-half-baked-500 rounded"
      >
        {{ $t('save') }}
      </button>
    </div>
  </form>
</template>
