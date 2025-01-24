<script setup lang="ts">
import BoxArrowUpRight from '@/components/icons/BoxArrowUpRight.vue'
import { RunAndOutput } from '@/wailsjs/go/execute/CommandExecutor'
import {
  AppBinaryType,
  AppDriverPath,
  AppVersion,
  WebView2Path,
  WebView2Version
} from '@/wailsjs/go/main/App'
import { BrowserOpenURL, Environment } from '@/wailsjs/runtime/runtime'
import * as semver from 'semver'
import { onBeforeMount, ref, useTemplateRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { useLoading } from 'vue-loading-overlay'
import { useToast } from 'vue-toast-notification'
import UpdateModal from './components/UpdateModal.vue'

const { t } = useI18n()

const $toast = useToast({ position: 'top-right' })

const $loading = useLoading({ lockScroll: true })

const modal = useTemplateRef('modal')

const info = ref({
  app: {
    version: 'na',
    buildType: 'na',
    binaryType: 'na',
    pathDriver: 'na'
  },
  webview: {
    version: 'na',
    location: 'na'
  }
})

const onCheck = ref(false)

onBeforeMount(() => {
  Promise.allSettled([
    AppVersion(),
    AppBinaryType(),
    Environment(),
    AppDriverPath(),
    WebView2Version(),
    WebView2Path()
  ]).then(([ver, btype, env, pdri, vwv2, pwv2]) => {
    if (ver.status != 'rejected') {
      info.value.app.version = ver.value
    }

    if (btype.status != 'rejected') {
      info.value.app.binaryType = btype.value
    }

    if (env.status != 'rejected') {
      info.value.app.buildType = env.value.buildType
    }

    if (pdri.status != 'rejected') {
      info.value.app.pathDriver = pdri.value
    }

    if (vwv2.status != 'rejected') {
      info.value.webview.version = vwv2.value
    }

    if (pwv2.status != 'rejected') {
      info.value.webview.location = pwv2.value
    }
  })
})

function checkUpdate() {
  if (Object.values(info.value.app).some(v => v == 'na')) {
    $toast.error(t('checkUpdateFailed'))
    return
  }

  const loader = $loading.show()

  fetch(
    'https://raw.githubusercontent.com/SuperDumbTM/driver-box/refs/heads/main/updater/version.json'
  )
    .then(response => response.json())
    .then(updateInfo => {
      if (semver.compare(info.value.app.version, updateInfo.latestVersion) >= 0) {
        $toast.info(t('noUpdate'))
      } else {
        modal.value?.show(
          { version: info.value.app.version, binaryType: info.value.app.binaryType },
          updateInfo
        )
      }
    })
    .catch(reason => {
      $toast.error(reason)
    })
    .finally(() => {
      loader.hide()
    })
}
</script>

<template>
  <div class="flex flex-col gap-y-6 h-full">
    <h1 class="text-lg font-bold">{{ $t('info.about') }} driver-box</h1>

    <div>
      <h2 class="font-bold">{{ $t('info.thisSoftware') }}</h2>

      <div class="grid grid-cols-7 gap-4">
        <div class="col-span-2">{{ $t('info.version') }}</div>
        <div class="flex col-span-5 gap-x-5">
          <p>
            {{ info.app.version }}
          </p>

          <button class="px-2 bg-gray-200 rounded" @click="checkUpdate()" :disabled="onCheck">
            {{ $t('info.checkUpdate') }}
          </button>
        </div>
      </div>

      <div class="grid grid-cols-7 gap-4">
        <div class="col-span-2">{{ $t('info.buildType') }}</div>
        <div class="col-span-5">{{ $t(`info.${info.app.buildType}`) }}</div>
      </div>

      <div class="grid grid-cols-7 gap-4">
        <div class="col-span-2">{{ $t('info.pathDriver') }}</div>
        <div class="col-span-5 break-all">
          {{ info.app.pathDriver }}

          <button
            type="button"
            class="ml-1"
            @click="RunAndOutput('cmd', ['/c', `explorer.exe ${info.app.pathDriver}`], true)"
          >
            <BoxArrowUpRight></BoxArrowUpRight>
          </button>
        </div>
      </div>
    </div>

    <div>
      <h2 class="font-bold">Microsoft Edge WebView2</h2>

      <div class="grid grid-cols-7 gap-4">
        <div class="col-span-2">{{ $t('info.version') }}</div>
        <div class="col-span-5">{{ info.webview.version }}</div>
      </div>

      <div class="grid grid-cols-7 gap-4">
        <div class="col-span-2">{{ $t('info.path') }}</div>
        <div class="col-span-5">
          {{ info.webview.location || $t('info.usingBuiltInWebView2') }}
        </div>
      </div>
    </div>

    <div>
      <h2 class="font-bold">{{ $t('info.development') }}</h2>

      <div class="grid grid-cols-7 gap-4">
        <div class="col-span-2">{{ $t('info.sourceCode') }}</div>
        <div class="col-span-5">
          <a
            href="https://github.com/SuperDumbTM/driver-box"
            class="text-sky-700 underline"
            @click.prevent="event => BrowserOpenURL((event.target as HTMLAnchorElement).href)"
          >
            https://github.com/SuperDumbTM/driver-box
          </a>
        </div>
      </div>

      <div class="grid grid-cols-7 gap-4">
        <div class="col-span-2">{{ $t('info.reportBug') }}</div>
        <div class="col-span-5">
          <a
            href="https://github.com/SuperDumbTM/driver-box/issues"
            class="text-sky-700 underline"
            @click.prevent="event => BrowserOpenURL((event.target as HTMLAnchorElement).href)"
          >
            https://github.com/SuperDumbTM/driver-box/issues
          </a>
        </div>
      </div>

      <div class="grid grid-cols-7 gap-4">
        <div class="col-span-2">{{ $t('info.license') }}</div>
        <div class="col-span-5">
          <div class="flex">
            <p class="inline font-mono">GNU General Public License v2.0</p>

            <button
              type="button"
              class="ml-2"
              @click="BrowserOpenURL('https://github.com/SuperDumbTM/driver-box/blob/main/LICENSE')"
            >
              <BoxArrowUpRight></BoxArrowUpRight>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <UpdateModal ref="modal"></UpdateModal>
</template>
