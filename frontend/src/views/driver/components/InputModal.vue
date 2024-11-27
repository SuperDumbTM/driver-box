<script setup lang="ts">
import CrossIcon from '@/components/icons/CrossIcon.vue'
import { flags } from '@/definitions/flags'
import { SelectFile } from '@/wailsjs/go/main/App'
import { store } from '@/wailsjs/go/models'
import { ref } from 'vue'
import IncompatibleDriverSelector from './IncompatibleDriverSelector.vue'

defineProps<{ drivers: Array<store.Driver> }>()

defineExpose({
  show: (data?: Partial<store.Driver>) => {
    show.value = true
    if (data) {
      dri.value = {
        ...dri.value,
        ...data,
        flags: data.flags?.join(','),
        allowRtCodes: data.allowRtCodes?.join(',')
      }
    }
  },
  hide: () => {
    show.value = false
    dri.value = {}
  }
})

const emit = defineEmits<{
  submit: [dri: store.Driver]
}>()

const show = ref(false)
const dri = ref<{
  id?: string
  name?: string
  type?: store.DriverType
  path?: string
  flags?: string
  minExeTime?: number
  allowRtCodes?: string
  incompatibles?: Array<string>
}>({
  minExeTime: 5
})
</script>

<template>
  <Transition name="modal">
    <div class="bg-gray-900/50 fixed inset-0 z-40" v-show="show"></div>
  </Transition>

  <Transition name="modal">
    <div
      class="fixed top-0 right-0 left-0 z-50 flex justify-center items-center w-full h-full"
      v-show="show"
    >
      <div class="w-[80vw] max-w-[650px] max-h-full p-4">
        <!-- Modal content -->
        <div class="bg-white rounded-lg shadow">
          <!-- Modal header -->
          <div class="flex items-center justify-between px-3 py-1.5 border-b rounded-t bg-white">
            <h3 class="font-semibold">
              {{ dri ? $t('driverForms.editDriver') : $t('driverForms.createDriver') }}
            </h3>
            <button
              type="button"
              class="inline-flex justify-center items-center h-8 w-8 ms-auto text-sm text-gray-400 hover:text-gray-900 bg-transparent hover:bg-gray-200 rounded-lg"
              @click="
                () => {
                  show = false
                  dri = { minExeTime: 5 }
                }
              "
            >
              <CrossIcon></CrossIcon>
            </button>
          </div>

          <!-- Modal body -->
          <div class="max-h-[70vh] overflow-auto py-2 px-4">
            <form
              class="flex flex-col gap-y-3"
              @submit.prevent="
                _ => {
                  emit(
                    'submit',
                    new store.Driver({
                      ...dri,
                      flags: dri.flags ? dri.flags.split(',') : [],
                      allowRtCodes: dri.allowRtCodes
                        ? dri.allowRtCodes
                            ?.split(',')
                            .map(c => parseInt(c))
                            .filter(c => !Number.isNaN(c))
                        : [],
                      incompatibles: dri.incompatibles ?? []
                    })
                  )
                }
              "
            >
              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">
                  {{ $t('driverForms.type') }}
                </label>
                <select
                  name="type"
                  v-model="dri.type"
                  class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                  required
                >
                  <option v-for="type in store.DriverType" :key="type" :value="type">
                    {{ $t(`driverCategories.${type}`) }}
                  </option>
                </select>
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">
                  {{ $t('driverForms.name') }}
                </label>
                <input
                  type="text"
                  name="name"
                  v-model="dri.name"
                  class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                  autocomplete="off"
                  required
                />
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">
                  {{ $t('driverForms.path') }}
                </label>

                <div class="flex">
                  <button
                    type="button"
                    class="inline-flex items-center px-3 text-sm text-gray-900 bg-gray-200 border border-e-0 rounded-s-md rounded-e-0 border-gray-300"
                    @click="
                      SelectFile(true).then(path => {
                        dri.path = path
                      })
                    "
                  >
                    {{ $t('driverForms.selectFile') }}
                  </button>
                  <input
                    type="text"
                    name="path"
                    v-model="dri.path"
                    class="block flex-1 min-w-0 w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 border rounded-none rounded-e-lg shadow-sm"
                    ref="pathInput"
                    autocomplete="off"
                    required
                  />
                </div>
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">
                  {{ $t('driverForms.argument') }}
                </label>

                <div class="flex">
                  <select
                    name="flags"
                    class="inline-flex items-center w-24 text-sm border border-e-0 rounded-e-0 rounded-s-lg border-apple-green-600 outline-none"
                    @change="
                      event => {
                        dri.flags = (event.target as HTMLSelectElement).value
                      }
                    "
                  >
                    <option value="">
                      {{ $t('driverForms.manualInput') }}
                    </option>
                    <option
                      v-for="(flag, name) in flags"
                      :key="name"
                      :value="flag.join(',')"
                      :selected="dri.flags === flag.join()"
                    >
                      {{ name }}
                    </option>
                  </select>
                  <input
                    type="text"
                    name="flags"
                    v-model="dri.flags"
                    class="block flex-1 min-w-0 w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 border rounded-none rounded-e-lg shadow-sm"
                    autocomplete="off"
                  />
                </div>

                <p class="mt-1 text-xs font-light text-apple-green-800">
                  {{ $t('driverForms.commaSeparated') }}
                </p>
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">
                  {{ $t('driverForms.incompatibleWith') }}
                </label>

                <IncompatibleDriverSelector
                  :options="drivers.filter(d => d.id !== dri.id)"
                  v-model="dri.incompatibles"
                ></IncompatibleDriverSelector>
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">
                  {{ $t('driverForms.minExecuteTime') }}
                </label>
                <input
                  type="number"
                  name="minExeTime"
                  v-model="dri.minExeTime"
                  step="0.1"
                  class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                  autocomplete="off"
                  required
                />
                <p class="mt-1 text-xs font-light text-apple-green-800">
                  {{ $t('driverForms.minExecuteTimeHelp') }}
                </p>
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">
                  {{ $t('driverForms.allowedExitCode') }}
                </label>
                <input
                  type="text"
                  name="allowRtCodes"
                  v-model="dri.allowRtCodes"
                  class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                  autocomplete="off"
                />
                <p class="mt-1 text-xs font-light text-apple-green-800">
                  {{ $t('driverForms.allowedExitCodeHelp') }}
                </p>
                <p class="mt-1 text-xs font-light text-apple-green-800">
                  {{ $t('driverForms.commaSeparated') }}
                </p>
              </div>

              <button
                type="submit"
                class="w-full my-1 py-2 text-sm font-medium text-white bg-powder-blue-800 hover:bg-powder-blue-600 rounded-lg"
              >
                {{ $t('save') }}
              </button>
            </form>
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
