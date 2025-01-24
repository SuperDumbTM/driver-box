<script setup lang="ts">
import CrossIcon from '@/components/icons/CrossIcon.vue'
import { Update } from '@/wailsjs/go/main/App'
import { Quit } from '@/wailsjs/runtime/runtime'
// import * as appManager from '@/wailsjs/go/store/AppSettingManager'

import { ref } from 'vue'
import { useLoading } from 'vue-loading-overlay'

defineExpose({
  show: (crrtInfo: typeof currentInfo.value, info: typeof updateInfo.value) => {
    show.value = true

    currentInfo.value = crrtInfo
    updateInfo.value = info
  },
  hide: () => {
    show.value = false
  }
})

const $loading = useLoading({ lockScroll: true })

const show = ref(false)

const currentInfo = ref<{
  version: string
  binaryType: string
}>()

const updateInfo = ref<{
  latestVersion: string
  message: string
}>()
</script>

<template>
  <Transition name="modal">
    <div class="fixed inset-0 z-40 bg-gray-900/50" v-show="show"></div>
  </Transition>

  <Transition name="modal">
    <div
      class="fixed top-0 right-0 left-0 z-50 flex justify-center items-center w-full h-full"
      v-show="show"
    >
      <div class="w-[400px]">
        <!-- Modal content -->
        <div class="bg-white rounded-lg shadow">
          <!-- Modal header -->
          <div class="flex items-center justify-between h-12 px-4 border-b rounded-t">
            <h3 class="font-semibold">
              {{ $t('info.updateInfoTitle') }}
            </h3>

            <button
              type="button"
              class="p-3 text-sm text-gray-400 hover:text-gray-900 bg-transparent hover:bg-gray-100 rounded-lg"
              @click="
                () => {
                  show = false
                }
              "
            >
              <CrossIcon></CrossIcon>
            </button>
          </div>

          <!-- Modal body -->
          <div class="flex flex-col gap-y-3 min-h-40 max-h-96 py-2 px-4">
            <div class="flex flex-col gap-y-2 grow">
              <div class="flex">
                <h1 class="min-w-32 font-medium">
                  {{ $t('info.latestVersion') }}
                </h1>
                <p>{{ updateInfo?.latestVersion }}</p>
              </div>

              <hr />

              <div class="flex flex-col grow">
                <h1 class="min-w-32 mb-1 font-medium">
                  {{ $t('info.updateInfo') }}
                </h1>

                <p
                  v-html="updateInfo?.message || $t('info.noUpdateInfo')"
                  :class="{ italic: !updateInfo?.message }"
                ></p>
              </div>
            </div>

            <button
              class="w-full text-white bg-half-baked-600 hover:bg-half-baked-500 rounded"
              @click="
                () => {
                  if (!currentInfo || !updateInfo) {
                    return
                  }

                  $toast.info($t('toast.downloadingUpdater'), { duration: 60 * 1000 })
                  const loader = $loading.show()

                  Update(currentInfo.version, updateInfo.latestVersion, currentInfo.binaryType)
                    .then(() => Quit())
                    .catch(reason => $toast.error(reason))
                    .finally(() => loader.hide())
                }
              "
            >
              {{ $t('info.update') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.5s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

label:has(+ input:required, + select:required):after,
label:has(+ div > input:required):after {
  content: ' *';
  color: red;
}
</style>
