<script setup lang="ts">
import CrossIcon from '@/components/icons/CrossIcon.vue'
import { ref } from 'vue'

defineExpose({
  show: (cb: typeof callback) => {
    show.value = true
    callback = cb
  },
  hide: () => {
    show.value = false
  }
})

let callback: (answer: 'yes' | 'no') => void

const show = ref(false)
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
      <div class="max-w-[60vw]">
        <!-- Modal content -->
        <div class="bg-white rounded-lg shadow">
          <!-- Modal header -->
          <div class="flex items-center justify-between h-12 px-4 border-b rounded-t">
            <h3 class="font-semibold">
              {{ $t('driverForm.unsaveConfirmTitle') }}
            </h3>

            <button
              type="button"
              class="p-3 text-sm text-gray-400 hover:text-gray-900 bg-transparent rounded-lg"
              @click="
                () => {
                  show = false
                  callback('no')
                }
              "
            >
              <CrossIcon></CrossIcon>
            </button>
          </div>

          <!-- Modal body -->
          <div class="px-3 py-5">
            <p>
              {{ $t('driverForm.unsaveConfirmMessage') }}
            </p>
          </div>

          <div class="flex gap-x-2 h-12 py-2 px-4 border-t">
            <button
              type="button"
              class="flex-1 text-white bg-apple-green-800 hover:bg-apple-green-600 rounded"
              @click="
                () => {
                  show = false
                  callback('yes')
                }
              "
            >
              {{ $t('common.confirm') }}
            </button>
            <button
              type="button"
              class="flex-1 text-white bg-gray-400 hover:bg-gray-300 rounded"
              @click="
                () => {
                  show = false
                  callback('no')
                }
              "
            >
              {{ $t('common.cancel') }}
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
  transition: opacity 0.1s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
