<script setup lang="ts">
import CrossIcon from '@/components/icons/CrossIcon.vue'
import { porter } from '@/wailsjs/go/models'
import * as programPorter from '@/wailsjs/go/porter/Porter'
import { nextTick, ref, useTemplateRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'vue-toast-notification'
import ProgressBar from './ProgressBar.vue'

defineExpose({
  export: (destination: string) => {
    show.value = true
    progress.value = null
    messages.value = []

    programPorter
      .Export(destination)
      .catch(err => {
        if (!err.includes('canceled')) {
          $toast.error(err)
        }
      })
      .finally(() => {
        clearInterval(interval)
        updateProgress()
      })

    updateProgress()
    interval = setInterval(updateProgress, 300)
  },
  import: (from: 'url' | 'file', source: string, ignoreAS: boolean) => {
    show.value = true
    progress.value = null
    messages.value = []

    if (from == 'url') {
      programPorter
        .ImportFromURL(source, ignoreAS)
        .catch(err => {
          if (!err.includes('canceled')) {
            $toast.error(err)
          }
        })
        .finally(() => {
          clearInterval(interval)
          updateProgress()
        })
    } else {
      programPorter
        .ImportFromFile(source, ignoreAS)
        .catch(err => {
          if (!err.includes('canceled')) {
            $toast.error(err)
          }
        })
        .finally(() => {
          clearInterval(interval)
          updateProgress()
        })
    }

    updateProgress()
    interval = setInterval(updateProgress, 300)
  }
})

const { t } = useI18n()

const $toast = useToast({ position: 'top-right' })

const messageBox = useTemplateRef('message-box')

let interval = -1

const show = ref(false)

const messages = ref<Array<string>>([])

const progress = ref<porter.Progresses | null>(null)

function updateProgress() {
  return programPorter.Progress().then(p => {
    let scroll = false
    if (
      messageBox.value!.scrollTop + messageBox.value!.clientHeight >=
      messageBox.value!.scrollHeight * 0.99
    ) {
      scroll = true
    }

    progress.value = p
    messages.value.push(...p.message.filter(m => m !== ''))

    if (scroll) {
      nextTick(() => {
        messageBox.value!.scrollTop = messageBox.value!.scrollHeight
      })
    }
  })
}
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
      <div class="">
        <!-- Modal content -->
        <div class="bg-white rounded-lg shadow">
          <!-- Modal header -->
          <div class="flex items-center justify-between h-12 px-4 border-b rounded-t">
            <h3 class="font-semibold">
              {{ t('porter.progress') }}
            </h3>

            <button
              v-show="progress?.status.includes('ed')"
              type="button"
              class="p-3 text-sm text-gray-400 hover:text-gray-900 bg-transparent hover:bg-gray-100 rounded-lg"
              @click="
                () => {
                  show = false
                  programPorter.Abort()
                }
              "
            >
              <CrossIcon></CrossIcon>
            </button>
          </div>

          <!-- Modal body -->
          <div class="h-[70vh] w-[70vw] overflow-auto py-2 px-4">
            <div class="flex flex-col gap-y-2 h-full">
              <ProgressBar :progresses="progress"></ProgressBar>

              <div
                class="flex flex-col flex-1 gap-y-2 overflow-y-auto min-h-48 p-1 border rounded"
                ref="message-box"
              >
                <p v-for="(m, i) in messages" :key="i" class="text-xs text-gray-400 break-all">
                  {{ m }}
                </p>
              </div>

              <div class="flex justify-end">
                <button
                  v-show="progress?.status == 'pending' || progress?.status == 'running'"
                  type="button"
                  class="px-2 py-1 text-white bg-rose-600 rounded"
                  @click="
                    () => {
                      programPorter.Abort().catch(err => $toast.error(err))
                    }
                  "
                >
                  {{ t('common.cancel') }}
                </button>
              </div>
            </div>
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
</style>
