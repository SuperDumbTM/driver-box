<script setup lang="ts">
import { onBeforeMount, ref } from 'vue'

import { Cwd, SelectFile, SelectFolder } from '@/wailsjs/go/main/App'
import * as appManager from '@/wailsjs/go/store/AppSettingManager'
import { useI18n } from 'vue-i18n'
import DownloadProgressModal from './components/DownloadProgressModal.vue'

const { t } = useI18n()

const exportDirectory = ref('')

const importInput = ref<{
  from: 'file' | 'url'
  filePath: string
  url: string
  ignoreAppSetting: boolean
}>({
  from: 'file',
  filePath: '',
  url: '',
  ignoreAppSetting: false
})

onBeforeMount(() => {
  appManager.Read().then(s => (importInput.value.url = s.driver_download_url))

  Cwd().then(cwd => {
    exportDirectory.value = cwd
  })
})
</script>

<template>
  <div class="flex flex-col h-full gap-y-6">
    <div>
      <h1 class="text-xl font-bold">{{ t('porters.title') }}</h1>
      <p class="text-gray-400">{{ t('porters.titleHint') }}</p>

      <hr class="mt-2 -mb-3" />
    </div>

    <div class="flex flex-col gap-y-3">
      <h2 class="mb-1 text-lg font-medium">{{ t('porters.exportToFile') }}</h2>

      <div class="flex gap-x-6">
        <label class="w-24 content-center text-gray-900">
          {{ t('porters.exportDestination') }}
        </label>

        <div class="flex gap-x-2 w-full">
          <input
            type="url"
            name="export_directory"
            v-model="exportDirectory"
            class="flex-1 px-3 py-2 w-full text-black text-sm border-none rounded bg-gray-100"
          />

          <button
            type="button"
            class="px-3 text-sm font-medium text-white bg-powder-blue-800 hover:bg-powder-blue-600 rounded"
            @click="
              () => {
                SelectFolder(false).then(path => {
                  exportDirectory = path
                })
              }
            "
          >
            {{ t('select') }}
          </button>
        </div>
      </div>

      <div class="flex justify-end">
        <button
          type="button"
          class="mt-3 py-1 w-28 text-white bg-half-baked-600 hover:bg-half-baked-500 rounded"
          @click="
            $refs.progressModal?.export(
              'C:\\Users\\EltonLO(House730)\\Documents\\Repository\\Driver-Box\\build'
            )
          "
        >
          {{ t('porters.export') }}
        </button>
      </div>
    </div>

    <div class="flex flex-col gap-y-3">
      <div class="flex gap-x-4">
        <h2 class="mb-1 text-lg font-medium">
          {{ t('porters.import') }}
        </h2>

        <div class="relative inline-flex p-0.5 border rounded-3xl">
          <button
            class="z-10 px-3 text-center text-xs rounded-3xl select-none"
            @click="importInput.from = 'file'"
          >
            {{ t('porters.importFromFile') }}
          </button>

          <button
            class="z-10 px-3 text-center text-xs rounded-3xl select-none"
            @click="importInput.from = 'url'"
          >
            {{ t('porters.importFromNetwork') }}
          </button>

          <span
            class="absolute top-1 bg-gray-300 rounded-3xl transition duration-200"
            :class="{ 'translate-x-full': importInput.from == 'url' }"
            style="width: calc(50% - 2px); height: calc(100% - 8px)"
          ></span>
        </div>
      </div>

      <!-- from file -->
      <div v-if="importInput.from == 'file'" class="flex gap-x-6">
        <label class="w-24 content-center text-gray-900">
          {{ t('porters.file') }}
        </label>

        <div class="flex gap-x-2 w-full">
          <input
            type="url"
            name="driver_download_url"
            placeholder="driver-box.zip"
            v-model="importInput.filePath"
            class="flex-1 px-3 py-2 w-full text-black text-sm border-none rounded bg-gray-100"
            readonly
          />

          <button
            type="button"
            class="px-3 text-sm font-medium text-white bg-powder-blue-800 hover:bg-powder-blue-600 rounded"
            @click="
              () => {
                SelectFile(false).then(path => {
                  importInput.filePath = path
                })
              }
            "
          >
            {{ t('select') }}
          </button>
        </div>
      </div>

      <!-- from url -->
      <div v-else class="flex gap-x-6">
        <label class="w-24 content-center text-gray-900">
          {{ t('porters.url') }}
        </label>

        <div class="flex gap-x-2 w-full">
          <input
            type="url"
            placeholder="https://..."
            v-model="importInput.url"
            class="flex-1 px-3 py-2 w-full text-black text-sm rounded"
          />
        </div>
      </div>

      <label>
        <input type="checkbox" v-model="importInput.ignoreAppSetting" />
        {{ t('porters.ignoreAppSetting') }}
      </label>

      <div class="flex justify-end">
        <button
          type="button"
          class="mt-3 py-1 w-28 text-white bg-half-baked-600 hover:bg-half-baked-500 rounded"
          @click="
            $refs.progressModal?.import(
              importInput.from,
              importInput.from == 'file' ? importInput.filePath : importInput.url,
              importInput.ignoreAppSetting
            )
          "
        >
          {{ t('porters.import') }}
        </button>
      </div>
    </div>
  </div>

  <DownloadProgressModal ref="progressModal"></DownloadProgressModal>
</template>
