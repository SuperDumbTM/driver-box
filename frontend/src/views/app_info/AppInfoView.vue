<script setup lang="ts">
import BoxArrowUpRight from '@/components/icons/BoxArrowUpRight.vue'
import { RunAndOutput } from '@/wailsjs/go/execute/CommandExecutor'
import { AppDriverPath, WebView2Path, WebView2Version } from '@/wailsjs/go/main/App'
import { BrowserOpenURL, Environment } from '@/wailsjs/runtime/runtime'
import { onBeforeMount, ref } from 'vue'

const info = ref({
  app: {
    version: '2.2.1',
    buildType: 'production',
    pathDriver: ''
  },
  webview: {
    version: '',
    location: ''
  }
})

onBeforeMount(() => {
  Promise.allSettled([Environment(), AppDriverPath(), WebView2Version(), WebView2Path()]).then(
    ([env, pdri, vwv2, pwv2]) => {
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
    }
  )
})
</script>

<template>
  <div class="flex flex-col gap-y-6 h-full">
    <h1 class="text-lg font-bold">{{ $t('info.about') }} driver-box</h1>

    <div>
      <h2 class="font-bold">{{ $t('info.thisSoftware') }}</h2>

      <div class="grid grid-cols-7 gap-4">
        <div class="col-span-2">{{ $t('info.version') }}</div>
        <div class="col-span-5">{{ info.app.version }}</div>
      </div>

      <div class="grid grid-cols-7 gap-4">
        <div class="col-span-2">{{ $t('info.buildType') }}</div>
        <div class="col-span-5">{{ $t(`info.${info.app.buildType}`) }}</div>
      </div>

      <div class="grid grid-cols-7 gap-4">
        <div class="col-span-2">{{ $t('info.pathDriver') }}</div>
        <div class="col-span-5">
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
</template>
